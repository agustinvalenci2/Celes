from functools import wraps
from flask import request, jsonify
from services.jwt_service import JWTService

jwt_service = JWTService()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        try:
            data = jwt_service.decode_token(token)
        except Exception as e:
            return jsonify({"message": "Token is invalid!"}), 403

        return f(data, *args, **kwargs)

    return decorated
