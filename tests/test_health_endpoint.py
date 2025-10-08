"""
Tests de integración para el endpoint de health check
"""
import unittest
import json
from app import create_app


class TestHealthEndpoint(unittest.TestCase):
    """Tests para el endpoint de health check"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_health_endpoint_returns_pong(self):
        """Test que verifica que el endpoint /providers/ping retorna 'pong'"""
        response = self.client.get('/providers/ping')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8').strip(), '"pong"')
    
    def test_health_endpoint_content_type(self):
        """Test que verifica el content type de la respuesta"""
        response = self.client.get('/providers/ping')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)


if __name__ == '__main__':
    unittest.main()
