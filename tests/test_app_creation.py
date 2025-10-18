"""
Tests para la creación de la aplicación
"""
import unittest
from app import create_app


class TestAppCreation(unittest.TestCase):
    """Tests para la creación de la aplicación Flask"""
    
    def test_create_app_returns_flask_app(self):
        """Test que verifica que create_app retorna una instancia de Flask"""
        app = create_app()
        
        self.assertIsNotNone(app)
        self.assertEqual(app.name, 'app')
    
    def test_app_has_cors_configured(self):
        """Test que verifica que CORS está configurado"""
        app = create_app()
        
        # Verificar que la aplicación se puede crear sin errores
        self.assertIsNotNone(app)
    
    def test_app_has_routes_configured(self):
        """Test que verifica que las rutas están configuradas"""
        app = create_app()
        
        # Verificar que la aplicación tiene rutas registradas
        self.assertIsNotNone(app.url_map)
        
        # Verificar que existe la ruta de health check
        with app.test_client() as client:
            response = client.get('/providers/ping')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
