"""
Tests unitarios para el controlador de health check
"""
import unittest
from app.controllers.health_controller import HealthCheckView


class TestHealthController(unittest.TestCase):
    """Tests para HealthCheckView"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.health_controller = HealthCheckView()
    
    def test_health_check_returns_pong(self):
        """Test que verifica que el health check retorna 'pong'"""
        result, status_code = self.health_controller.get()
        
        self.assertEqual(result, "pong")
        self.assertEqual(status_code, 200)
    
    def test_health_check_status_code(self):
        """Test que verifica el código de estado del health check"""
        result, status_code = self.health_controller.get()
        
        self.assertEqual(status_code, 200)


if __name__ == '__main__':
    unittest.main()
