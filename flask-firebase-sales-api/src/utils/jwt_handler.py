import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app

def create_token(payload: dict, hours: int = 24):
    exp = datetime.utcnow() + timedelta(hours=hours)
    to_encode = {**payload, 'exp': exp}
    token = jwt.encode(to_encode, current_app.config['JWT_SECRET_KEY'], algorithm=current_app.config['JWT_ALGORITHM'])
    return token

def decode_token(token: str):
    return jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=[current_app.config['JWT_ALGORITHM']])

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'token requerido'}), 401
        token = auth.replace('Bearer ', '').strip()
        try:
            request.user = decode_token(token)
        except Exception:
            return jsonify({'error': 'token inválido'}), 401
        return fn(*args, **kwargs)
    return wrapper