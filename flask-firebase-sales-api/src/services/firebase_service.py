import os
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
from flask import current_app


def init_firebase():
    cred_path = current_app.config["FIREBASE_CREDENTIALS_PATH"]
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)


def get_db():
    return firestore.client()


def parse_date(d: str):
    # Espera YYYY-MM-DD
    return datetime.strptime(d, "%Y-%m-%d")


def date_range_filter(query, start: str, end: str):
    start_dt = parse_date(start)
    # end inclusive hasta 23:59:59
    end_dt = parse_date(end) + timedelta(days=1) - timedelta(seconds=1)
    return query.where("KeyDate", ">=", start_dt).where("KeyDate", "<=", end_dt)


def fetch_sales_by(field: str, value: str, start: str, end: str, limit: int = 20000):
    init_firebase()
    db = get_db()
    q = db.collection("sales").where(field, "==", value)
    q = date_range_filter(q, start, end)
    # Stream completo (considerar paginación para >20k docs)
    docs = q.stream()
    out = []
    for d in docs:
        rec = d.to_dict()
        out.append(rec)
    return out


def aggregate_sales(records):
    total_amount = 0.0
    total_qty = 0.0
    n = 0
    for r in records:
        amount = r.get("Amount") or 0
        qty = r.get("Qty") or 0
        try:
            total_amount += float(amount)
        except Exception:
            pass
        try:
            total_qty += float(qty)
        except Exception:
            pass
        n += 1
    avg_amount = (total_amount / n) if n else 0.0
    return {
        "count": n,
        "total_qty": total_qty,
        "total_amount": total_amount,
        "avg_amount": avg_amount,
    }
