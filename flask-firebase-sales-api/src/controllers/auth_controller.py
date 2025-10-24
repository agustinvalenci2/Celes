from flask import request, jsonify
from services.jwt_service import JWTService
from services.firebase_service import FirebaseService


class AuthController:
    def __init__(self):
        self.jwt_service = JWTService()
        self.firebase_service = FirebaseService()

    def login(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = self.firebase_service.authenticate_user(email, password)
        if user:
            token = self.jwt_service.create_token(user["uid"])
            return jsonify({"token": token}), 200
        return jsonify({"message": "Invalid credentials"}), 401

    def validate_token(self):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            payload = self.jwt_service.decode_token(token)
            return jsonify({"user_id": payload["sub"]}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 401
