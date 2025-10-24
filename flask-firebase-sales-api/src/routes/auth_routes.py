from flask import Blueprint, request, jsonify
from src.utils.jwt_handler import create_token

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.post('/login')
def login():
    data = request.get_json(force=True, silent=True) or {}
    username = data.get('username')
    password = data.get('password')
    # Demo: valida que vengan ambos campos (reemplazar por tu lógica real)
    if not username or not password:
        return jsonify({'error': 'credenciales requeridas'}), 400
    token = create_token({'sub': username})
    return jsonify({'access_token': token})