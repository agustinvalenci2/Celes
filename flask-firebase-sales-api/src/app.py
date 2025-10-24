from flask import Flask
from flask_cors import CORS
from src.config import Config
from src.routes.auth_routes import auth_bp  # Importar blueprint específico
from src.routes.sales_routes import sales_bp  # Importar blueprint específico


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    @app.route("/")
    def index():
        return {"message": "Flask Firebase Sales API", "status": "running"}

    @app.route("/routes")
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(
                {
                    "endpoint": rule.endpoint,
                    "methods": list(rule.methods),
                    "rule": str(rule),
                }
            )
        return {"routes": routes}

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(sales_bp, url_prefix="/api/sales")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
