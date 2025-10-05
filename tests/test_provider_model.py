import pytest
from unittest.mock import patch, MagicMock
from app.models.provider_model import Provider
from datetime import datetime
import uuid


class TestProvider:
    """Pruebas unitarias para Provider (modelo de dominio)"""
    
    @pytest.fixture
    def provider_data(self):
        """Fixture con datos válidos de proveedor"""
        return {
            'id': str(uuid.uuid4()),
            'name': 'Farmacia Test',
            'email': 'test@farmacia.com',
            'phone': '3001234567',
            'logo_filename': 'logo.jpg',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
    
    @pytest.fixture
    def provider(self, provider_data):
        """Fixture para Provider de muestra"""
        return Provider(**provider_data)
    
    def test_provider_initialization(self, provider_data):
        """Prueba la inicialización de Provider"""
        provider = Provider(**provider_data)
        
        assert provider.id == provider_data['id']
        assert provider.name == provider_data['name']
        assert provider.email == provider_data['email']
        assert provider.phone == provider_data['phone']
        assert provider.logo_filename == provider_data['logo_filename']
        assert provider.created_at == provider_data['created_at']
        assert provider.updated_at == provider_data['updated_at']
    
    def test_provider_initialization_with_defaults(self):
        """Prueba la inicialización de Provider con valores por defecto"""
        provider = Provider()
        
        assert provider.id is not None
        assert isinstance(provider.id, str)
        assert provider.name == ''
        assert provider.email == ''
        assert provider.phone == ''
        assert provider.logo_filename == ''
        assert provider.created_at is not None
        assert provider.updated_at is not None
        assert isinstance(provider.created_at, datetime)
        assert isinstance(provider.updated_at, datetime)
    
    def test_provider_to_dict(self, provider):
        """Prueba la conversión a diccionario"""
        result = provider.to_dict()
        
        assert isinstance(result, dict)
        assert result['id'] == provider.id
        assert result['name'] == provider.name
        assert result['email'] == provider.email
        assert result['phone'] == provider.phone
        assert result['logo_filename'] == provider.logo_filename
        assert result['created_at'] == provider.created_at.isoformat()
        assert result['updated_at'] == provider.updated_at.isoformat()
    
    def test_provider_to_dict_with_none_dates(self):
        """Prueba to_dict con fechas None"""
        provider = Provider()
        provider.created_at = None
        provider.updated_at = None
        
        result = provider.to_dict()
        
        assert result['created_at'] is None
        assert result['updated_at'] is None
    
    def test_provider_validate_success(self, provider):
        """Prueba validación exitosa con datos válidos"""
        # No debería lanzar excepción
        provider.validate()
    
    def test_provider_validate_empty_name(self):
        """Prueba validación con nombre vacío"""
        provider = Provider(name='', email='test@test.com', phone='3001234567')
        
        with pytest.raises(ValueError) as exc_info:
            provider.validate()
        
        assert "El campo 'Nombre' es obligatorio" in str(exc_info.value)
    
    def test_provider_validate_none_name(self):
        """Prueba validación con nombre None"""
        provider = Provider(name=None, email='test@test.com', phone='3001234567')
        
        with pytest.raises(ValueError) as exc_info:
            provider.validate()
        
        assert "El campo 'Nombre' es obligatorio" in str(exc_info.value)
    
    def test_provider_validate_invalid_name_characters(self):
        """Prueba validación con caracteres inválidos en nombre"""
        provider = Provider(name='Test@#$', email='test@test.com', phone='3001234567')
        
        with pytest.raises(ValueError) as exc_info:
            provider.validate()
        
        assert "El campo 'Nombre' debe aceptar únicamente caracteres alfabéticos, numéricos y espacios" in str(exc_info.value)
    
    def test_provider_validate_name_with_accents(self):
        """Prueba validación con nombre que contiene acentos (debería ser válido)"""
        provider = Provider(name='José María', email='test@test.com', phone='3001234567')
        
        # No debería lanzar excepción
        provider.validate()
    
    def test_provider_validate_empty_email(self):
        """Prueba validación con email vacío"""
        provider = Provider(name='Test', email='', phone='3001234567')
        
        with pytest.raises(ValueError) as exc_info:
            provider.validate()
        
        assert "El campo 'Correo electrónico' es obligatorio" in str(exc_info.value)
    
    def test_provider_validate_invalid_email_no_at(self):
        """Prueba validación con email sin @"""
        provider = Provider(name='Test', email='testtest.com', phone='3001234567')
        
        with pytest.raises(ValueError) as exc_info:
            provider.validate()
        
        assert "El campo 'Correo electrónico' debe validar el formato de email" in str(exc_info.value)
    
    def test_provider_validate_invalid_email_no_domain(self):
        """Prueba validación con email sin dominio"""
        provider = Provider(name='Test', email='test@', phone='3001234567')
        
        with pytest.raises(ValueError) as exc_info:
            provider.validate()
        
        assert "El campo 'Correo electrónico' debe validar el formato de email" in str(exc_info.value)
    
    def test_provider_validate_invalid_email_short_extension(self):
        """Prueba validación con email con extensión muy corta"""
        provider = Provider(name='Test', email='test@test.c', phone='3001234567')
        
        with pytest.raises(ValueError) as exc_info:
            provider.validate()
        
        assert "El campo 'Correo electrónico' debe validar el formato de email" in str(exc_info.value)
    
    def test_provider_validate_valid_emails(self):
        """Prueba validación con emails válidos"""
        valid_emails = [
            'test@test.com',
            'user@domain.co',
            'test.email@domain.org',
            'user+tag@domain.net'
        ]
        
        for email in valid_emails:
            provider = Provider(name='Test', email=email, phone='3001234567')
            # No debería lanzar excepción
            provider.validate()
    
    def test_provider_validate_empty_phone(self):
        """Prueba validación con teléfono vacío"""
        provider = Provider(name='Test', email='test@test.com', phone='')
        
        with pytest.raises(ValueError) as exc_info:
            provider.validate()
        
        assert "El campo 'Teléfono' es obligatorio" in str(exc_info.value)
    
    def test_provider_validate_phone_with_letters(self):
        """Prueba validación con teléfono que contiene letras"""
        provider = Provider(name='Test', email='test@test.com', phone='300abc4567')
        
        with pytest.raises(ValueError) as exc_info:
            provider.validate()
        
        assert "El campo 'Teléfono' debe validar que contenga solo números" in str(exc_info.value)
    
    def test_provider_validate_phone_too_short(self):
        """Prueba validación con teléfono muy corto"""
        provider = Provider(name='Test', email='test@test.com', phone='123456')
        
        with pytest.raises(ValueError) as exc_info:
            provider.validate()
        
        assert "El campo 'Teléfono' debe validar que contenga solo números y una longitud mínima de 7 dígitos" in str(exc_info.value)
    
    def test_provider_validate_valid_phones(self):
        """Prueba validación con teléfonos válidos"""
        valid_phones = ['3001234567', '1234567', '1234567890']
        
        for phone in valid_phones:
            provider = Provider(name='Test', email='test@test.com', phone=phone)
            # No debería lanzar excepción
            provider.validate()
    
    def test_provider_validate_invalid_logo_extension(self):
        """Prueba validación con logo con extensión inválida"""
        provider = Provider(name='Test', email='test@test.com', phone='3001234567', logo_filename='logo.txt')
        
        with pytest.raises(ValueError) as exc_info:
            provider.validate()
        
        assert "El campo 'Logo' debe aceptar únicamente archivos de imagen (JPG, PNG, GIF) con un tamaño máximo de 2MB" in str(exc_info.value)
    
    def test_provider_validate_valid_logo_extensions(self):
        """Prueba validación con logos con extensiones válidas"""
        valid_logos = ['logo.jpg', 'logo.jpeg', 'logo.png', 'logo.gif', 'LOGO.JPG', 'logo.PNG']
        
        for logo in valid_logos:
            provider = Provider(name='Test', email='test@test.com', phone='3001234567', logo_filename=logo)
            # No debería lanzar excepción
            provider.validate()
    
    def test_provider_validate_empty_logo(self):
        """Prueba validación con logo vacío (debería ser válido)"""
        provider = Provider(name='Test', email='test@test.com', phone='3001234567', logo_filename='')
        
        # No debería lanzar excepción (logo es opcional)
        provider.validate()
    
    def test_provider_validate_none_logo(self):
        """Prueba validación con logo None (debería ser válido)"""
        provider = Provider(name='Test', email='test@test.com', phone='3001234567', logo_filename=None)
        
        # No debería lanzar excepción (logo es opcional)
        provider.validate()
    
    def test_provider_validate_multiple_errors(self):
        """Prueba validación con múltiples errores"""
        provider = Provider(name='', email='invalid', phone='abc')
        
        with pytest.raises(ValueError) as exc_info:
            provider.validate()
        
        error_message = str(exc_info.value)
        assert "El campo 'Nombre' es obligatorio" in error_message
        assert "El campo 'Correo electrónico' debe validar el formato de email" in error_message
        assert "El campo 'Teléfono' debe validar que contenga solo números" in error_message
    
    def test_provider_is_valid_email(self, provider):
        """Prueba el método _is_valid_email"""
        # Emails válidos
        assert provider._is_valid_email('test@test.com') is True
        assert provider._is_valid_email('user@domain.co') is True
        assert provider._is_valid_email('test.email@domain.org') is True
        
        # Emails inválidos
        assert provider._is_valid_email('testtest.com') is False
        assert provider._is_valid_email('test@') is False
        assert provider._is_valid_email('@test.com') is False
        assert provider._is_valid_email('test@test.c') is False
        assert provider._is_valid_email('test@test') is False
    
    def test_provider_is_valid_image_filename(self, provider):
        """Prueba el método _is_valid_image_filename"""
        # Nombres válidos
        assert provider._is_valid_image_filename('logo.jpg') is True
        assert provider._is_valid_image_filename('logo.jpeg') is True
        assert provider._is_valid_image_filename('logo.png') is True
        assert provider._is_valid_image_filename('logo.gif') is True
        assert provider._is_valid_image_filename('LOGO.JPG') is True
        
        # Nombres inválidos
        assert provider._is_valid_image_filename('logo.txt') is False
        assert provider._is_valid_image_filename('logo.pdf') is False
        assert provider._is_valid_image_filename('logo') is False
        assert provider._is_valid_image_filename('') is True  # Vacío es válido (opcional)
        assert provider._is_valid_image_filename(None) is True  # None es válido (opcional)
    
    def test_provider_generate_logo_filename(self, provider):
        """Prueba el método generate_logo_filename"""
        # Con extensión válida
        result = provider.generate_logo_filename('logo.jpg')
        assert result.startswith('logo_')
        assert result.endswith('.jpg')
        assert len(result) > 10  # Debe tener UUID
        
        # Con extensión inválida - debería generar nombre con la extensión original
        result = provider.generate_logo_filename('logo.txt')
        assert result.startswith('logo_')
        assert result.endswith('.txt')
        assert len(result) > 10  # Debe tener UUID
        
        # Con nombre vacío
        result = provider.generate_logo_filename('')
        assert result == ''
        
        # Con None
        result = provider.generate_logo_filename(None)
        assert result == ''
    
    def test_provider_generate_logo_filename_unique(self, provider):
        """Prueba que generate_logo_filename genera nombres únicos"""
        filename1 = provider.generate_logo_filename('logo.jpg')
        filename2 = provider.generate_logo_filename('logo.jpg')
        
        assert filename1 != filename2
        assert filename1.startswith('logo_')
        assert filename2.startswith('logo_')
        assert filename1.endswith('.jpg')
        assert filename2.endswith('.jpg')
    
    def test_provider_repr(self, provider):
        """Prueba el método __repr__"""
        repr_str = repr(provider)
        
        assert 'Provider' in repr_str
        assert provider.id in repr_str
        assert provider.name in repr_str
        assert provider.email in repr_str
    
    def test_provider_inheritance(self, provider):
        """Prueba que Provider hereda de BaseModel"""
        from app.models.base_model import BaseModel
        
        assert isinstance(provider, BaseModel)
    
    def test_provider_abstract_methods_implemented(self, provider):
        """Prueba que Provider implementa los métodos abstractos de BaseModel"""
        # to_dict debe estar implementado
        assert hasattr(provider, 'to_dict')
        assert callable(getattr(provider, 'to_dict'))
        
        # validate debe estar implementado
        assert hasattr(provider, 'validate')
        assert callable(getattr(provider, 'validate'))