import os
import sys
import re
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, date
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

BATCH_SIZE = 200
MAX_WORKERS = 4


def initialize_firebase():
    """Initializes the Firebase connection using FIREBASE_CREDENTIALS_PATH."""
    load_dotenv()
    cred_path = os.getenv(
        "FIREBASE_CREDENTIALS_PATH",
        os.path.join(os.path.dirname(__file__), "..", "firebase-credentials.json"),
    )
    if not os.path.isabs(cred_path):
        cred_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", cred_path)
        )
    if not os.path.exists(cred_path):
        raise FileNotFoundError(
            f"Credentials file not found: {cred_path}"
        )
    cred = credentials.Certificate(cred_path)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    print("Firebase initialized")


def find_parquet_files(data_folder):
    """Lists parquet files in the data folder."""
    return [
        f
        for f in os.listdir(data_folder)
        if f.lower().endswith(".parquet") or f.lower().endswith(".snappy.parquet")
    ]


def sanitize_doc_id(value: str) -> str:
    """Sanitizes the document ID for Firestore."""
    if not value:
        return None
    doc_id = re.sub(r"[^\w\-_.]", "_", str(value))
    return doc_id[:1500]


def to_timestamp(value):
    """Converts to datetime compatible with Firestore."""
    if value is None or pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day)
    if isinstance(value, (int, float, np.integer, np.floating)):
        return None
    try:
        v = pd.to_datetime(value)
        if isinstance(v, pd.Timestamp):
            return v.to_pydatetime()
        if isinstance(v, date):
            return datetime(v.year, v.month, v.day)
        return v
    except Exception:
        return None


def normalize_for_firestore(obj):
    """Recursively normalizes structures for Firestore in an optimized way."""

    if obj is None or (isinstance(obj, float) and np.isnan(obj)):
        return None


    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (pd.Timestamp, datetime, date)):
        return to_timestamp(obj)


    if isinstance(obj, dict):
        return {k: normalize_for_firestore(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [normalize_for_firestore(v) for v in obj]

    return obj


def extract_top_keys(rec: dict) -> dict:
    """Ensures top keys and normalizes dates and types for Firestore."""
    out = {}

    for key, value in rec.items():
        if key in ("KeyDate", "Datetime") or (
            key == "Time" and isinstance(value, dict)
        ):
            if key == "Time":
                t = {}
                for k, v in value.items():
                    if k in ("Datetime", "KeyDate"):
                        t[k] = to_timestamp(v)
                    else:
                        t[k] = normalize_for_firestore(v)
                out[key] = t
            else:
                out[key] = to_timestamp(value)
        else:
            out[key] = normalize_for_firestore(value)

    return out


def process_batch(batch_records, collection_name, batch_num):
    """Processes a batch of records."""
    db = firestore.client()
    batch = db.batch()

    for rec, doc_id in batch_records:
        doc_ref = db.collection(collection_name).document(doc_id)
        batch.set(doc_ref, rec)

    batch.commit()
    return len(batch_records), batch_num


def load_to_firestore(df: pd.DataFrame, collection_name: str = "sales"):
    """Loads a DataFrame to Firestore in parallel batches."""
    records = df.to_dict("records")
    total = len(records)


    batches = []
    current_batch = []

    for idx, rec in enumerate(records):
        clean = extract_top_keys(rec)
        key_sale = clean.get("KeySale")
        doc_id = (
            sanitize_doc_id(key_sale)
            if key_sale
            else sanitize_doc_id(
                f"{clean.get('KeyStore','')}_{clean.get('KeyProduct','')}_{clean.get('KeyEmployee','')}_{clean.get('KeyDate','')}_{idx}"
            )
        )
        current_batch.append((clean, doc_id))

        if len(current_batch) >= BATCH_SIZE:
            batches.append(current_batch)
            current_batch = []

    if current_batch:
        batches.append(current_batch)

    print(f"  Processing {len(batches)} batches in parallel...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(process_batch, batch, collection_name, i)
            for i, batch in enumerate(batches)
        ]

        completed = 0
        for future in as_completed(futures):
            count, batch_num = future.result()
            completed += count
            print(
                f"  Progress: {completed}/{total} documents ({(completed/total)*100:.1f}%)"
            )


def show_data_preview(data_folder):
    """Shows first rows and columns of each file in data."""
    files = find_parquet_files(data_folder)
    if not files:
        print("No .parquet files found in the data folder")
        return
    print("\n=== DATA PREVIEW ===")
    for fname in files:
        fpath = os.path.join(data_folder, fname)
        df = pd.read_parquet(fpath)
        print(f"\nFile: {fname}")
        print(f"  Records: {len(df)}")
        print(f"  Columns: {list(df.columns)}")
        print("  First rows:")
        print(df.head(3))
        print("=" * 60)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.normpath(os.path.join(script_dir, "..", "data"))
    collection = "sales"

    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print("Usage:")
        print("  python scripts\\load_data.py --preview")
        print("  python scripts\\load_data.py [--collection sales]")
        sys.exit(0)

    if "--preview" in args:
        show_data_preview(data_folder)
        sys.exit(0)

    if "--collection" in args:
        try:
            collection = args[args.index("--collection") + 1]
        except Exception:
            print("Invalid value for --collection, using 'sales'.")

    print("=== STARTING DATA LOAD TO FIRESTORE ===")
    initialize_firebase()

    files = find_parquet_files(data_folder)
    if not files:
        print("No .parquet files found in the data folder")
        sys.exit(1)

    for fname in files:
        fpath = os.path.join(data_folder, fname)
        print(f"\nLoading: {fname}")
        df = pd.read_parquet(fpath)
        print(f"  Records: {len(df)}  |  Columns: {len(df.columns)}")
        load_to_firestore(df, collection_name=collection)
        print(f"File {fname} loaded to collection '{collection}'")

    print("\nProcess completed")


if __name__ == "__main__":
    main()
