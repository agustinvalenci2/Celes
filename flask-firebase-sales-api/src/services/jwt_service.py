from datetime import datetime, timedelta
import jwt
from flask import current_app

class JWTService:
    def __init__(self):
        self.secret_key = current_app.config['JWT_SECRET_KEY']
        self.algorithm = current_app.config['JWT_ALGORITHM']
        self.expiration = current_app.config['JWT_EXPIRATION']

    def create_token(self, user_id):
        expiration_time = datetime.utcnow() + timedelta(seconds=self.expiration)
        token = jwt.encode({'user_id': user_id, 'exp': expiration_time}, self.secret_key, algorithm=self.algorithm)
        return token

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def validate_token(self, token):
        payload = self.decode_token(token)
        return payload is not None and 'user_id' in payload