# File: /flask-firebase-sales-api/flask-firebase-sales-api/src/routes/__init__.py

from flask import Blueprint

# Initialize the routes blueprint
routes_bp = Blueprint("routes", __name__)

from .auth_routes import auth_bp
from .sales_routes import sales_bp

__all__ = ["auth_bp", "sales_bp"]
