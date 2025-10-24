from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configurations
    app.config.from_object('config.Config')

    # Register routes
    from .routes import sales_routes, auth_routes
    app.register_blueprint(sales_routes.bp)
    app.register_blueprint(auth_routes.bp)

    return app