from flask import Blueprint, request, jsonify
from src.utils.jwt_handler import jwt_required
from src.services.firebase_service import fetch_sales_by, aggregate_sales

sales_bp = Blueprint('sales', __name__, url_prefix='/api')

def required_params(*names):
    missing = [n for n in names if not request.args.get(n)]
    if missing:
        return jsonify({'error': f'faltan parámetros: {", ".join(missing)}'}), 400
    return None

# Consultas por periodo
@sales_bp.get('/employee')
@jwt_required
def sales_by_employee():
    err = required_params('key', 'start', 'end')
    if err: return err
    recs = fetch_sales_by('KeyEmployee', request.args['key'], request.args['start'], request.args['end'])
    return jsonify({'filters': {'KeyEmployee': request.args['key'], 'start': request.args['start'], 'end': request.args['end']},
                    'metrics': aggregate_sales(recs),
                    'items': recs})

@sales_bp.get('/product')
@jwt_required
def sales_by_product():
    err = required_params('key', 'start', 'end')
    if err: return err
    recs = fetch_sales_by('KeyProduct', request.args['key'], request.args['start'], request.args['end'])
    return jsonify({'filters': {'KeyProduct': request.args['key'], 'start': request.args['start'], 'end': request.args['end']},
                    'metrics': aggregate_sales(recs),
                    'items': recs})

@sales_bp.get('/store')
@jwt_required
def sales_by_store():
    err = required_params('key', 'start', 'end')
    if err: return err
    recs = fetch_sales_by('KeyStore', request.args['key'], request.args['start'], request.args['end'])
    return jsonify({'filters': {'KeyStore': request.args['key'], 'start': request.args['start'], 'end': request.args['end']},
                    'metrics': aggregate_sales(recs),
                    'items': recs})

# Totales y promedios
@sales_bp.get('/employee/metrics')
@jwt_required
def metrics_employee():
    err = required_params('key', 'start', 'end')
    if err: return err
    recs = fetch_sales_by('KeyEmployee', request.args['key'], request.args['start'], request.args['end'])
    return jsonify({'filters': {'KeyEmployee': request.args['key'], 'start': request.args['start'], 'end': request.args['end']},
                    'metrics': aggregate_sales(recs)})

@sales_bp.get('/product/metrics')
@jwt_required
def metrics_product():
    err = required_params('key', 'start', 'end')
    if err: return err
    recs = fetch_sales_by('KeyProduct', request.args['key'], request.args['start'], request.args['end'])
    return jsonify({'filters': {'KeyProduct': request.args['key'], 'start': request.args['start'], 'end': request.args['end']},
                    'metrics': aggregate_sales(recs)})

@sales_bp.get('/store/metrics')
@jwt_required
def metrics_store():
    err = required_params('key', 'start', 'end')
    if err: return err
    recs = fetch_sales_by('KeyStore', request.args['key'], request.args['start'], request.args['end'])
    return jsonify({'filters': {'KeyStore': request.args['key'], 'start': request.args['start'], 'end': request.args['end']},
                    'metrics': aggregate_sales(recs)})