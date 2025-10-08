"""
Aplicación principal del sistema de proveedores MediSupply
"""
import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS


def create_app():
    """Factory function para crear la aplicación Flask"""
    
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Configurar CORS
    cors = CORS(app)
    
    # Configurar rutas
    configure_routes(app)
    
    return app


def configure_routes(app):
    """Configura las rutas de la aplicación"""
    from .controllers.health_controller import HealthCheckView
    from .controllers.provider_controller import ProviderController, ProviderHealthController, ProviderDeleteAllController
    
    api = Api(app)
    
    # Health check endpoints
    api.add_resource(HealthCheckView, '/providers/ping')
    api.add_resource(ProviderHealthController, '/providers/health')
    
    # Provider endpoints
    api.add_resource(ProviderController, '/providers', '/providers/<string:provider_id>')
    api.add_resource(ProviderDeleteAllController, '/providers/all')
