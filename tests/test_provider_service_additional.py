"""
Pruebas adicionales para ProviderService para mejorar coverage
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.provider_service import ProviderService
from app.models.provider_model import Provider
from app.exceptions.custom_exceptions import ValidationError, BusinessLogicError
from werkzeug.datastructures import FileStorage
from datetime import datetime
import uuid

# Los mocks de Google Cloud Storage se manejan en conftest.py


class TestProviderServiceAdditional:
    """Pruebas adicionales para ProviderService"""

    @pytest.fixture
    def provider_service(self):
        """Instancia de ProviderService para pruebas"""
        with patch('app.services.provider_service.ProviderRepository') as mock_repo, \
             patch('app.services.provider_service.CloudStorageService') as mock_cloud:
            return ProviderService()

    def test_validate_business_rules_name_too_long(self, provider_service):
        """Prueba validación con nombre muy largo"""
        invalid_data = {
            'name': 'A' * 256,  # Más de 255 caracteres
            'email': 'test@farmacia.com',
            'phone': '3001234567'
        }
        
        with pytest.raises(ValueError, match="El nombre del proveedor no puede exceder 255 caracteres"):
            provider_service.validate_business_rules(**invalid_data)

    def test_validate_business_rules_name_too_short(self, provider_service):
        """Prueba validación con nombre muy corto"""
        invalid_data = {
            'name': 'A',  # Menos de 2 caracteres
            'email': 'test@farmacia.com',
            'phone': '3001234567'
        }
        
        with pytest.raises(ValueError, match="El nombre del proveedor debe tener al menos 2 caracteres"):
            provider_service.validate_business_rules(**invalid_data)

    def test_validate_business_rules_email_too_long(self, provider_service):
        """Prueba validación con email muy largo"""
        invalid_data = {
            'name': 'Farmacia Test',
            'email': 'a' * 250 + '@test.com',  # Más de 255 caracteres
            'phone': '3001234567'
        }
        
        with pytest.raises(ValueError, match="El correo electrónico no puede exceder 255 caracteres"):
            provider_service.validate_business_rules(**invalid_data)

    def test_validate_business_rules_email_invalid_format(self, provider_service):
        """Prueba validación con formato de email inválido"""
        invalid_data = {
            'name': 'Farmacia Test',
            'email': 'invalid-email',  # Sin @ y dominio
            'phone': '3001234567'
        }
        
        with pytest.raises(ValueError, match="El campo 'Correo electrónico' debe tener un formato válido"):
            provider_service.validate_business_rules(**invalid_data)

    def test_validate_business_rules_phone_too_long(self, provider_service):
        """Prueba validación con teléfono muy largo"""
        invalid_data = {
            'name': 'Farmacia Test',
            'email': 'test@farmacia.com',
            'phone': '1' * 21  # Más de 20 caracteres
        }
        
        with pytest.raises(ValueError, match="El teléfono no puede exceder 20 caracteres"):
            provider_service.validate_business_rules(**invalid_data)

    def test_validate_business_rules_phone_too_short(self, provider_service):
        """Prueba validación con teléfono muy corto"""
        invalid_data = {
            'name': 'Farmacia Test',
            'email': 'test@farmacia.com',
            'phone': '123456'  # Menos de 7 dígitos
        }
        
        with pytest.raises(ValueError, match="El campo 'Teléfono' debe tener al menos 7 dígitos"):
            provider_service.validate_business_rules(**invalid_data)

    def test_validate_business_rules_phone_non_numeric(self, provider_service):
        """Prueba validación con teléfono no numérico"""
        invalid_data = {
            'name': 'Farmacia Test',
            'email': 'test@farmacia.com',
            'phone': '300-123-4567'  # Con guiones
        }
        
        with pytest.raises(ValueError, match="El campo 'Teléfono' debe contener solo números"):
            provider_service.validate_business_rules(**invalid_data)
