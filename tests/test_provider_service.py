import pytest
from unittest.mock import patch, MagicMock
from app.services.provider_service import ProviderService
from app.models.provider_model import Provider
from app.exceptions.custom_exceptions import ValidationError, BusinessLogicError
from werkzeug.datastructures import FileStorage
from datetime import datetime
import uuid


class TestProviderService:
    """Pruebas unitarias para ProviderService"""
    
    @pytest.fixture
    def mock_repository(self):
        """Fixture para mock del ProviderRepository"""
        return MagicMock()
    
    @pytest.fixture
    def provider_service(self, mock_repository):
        """Fixture para ProviderService con repository mockeado"""
        return ProviderService(provider_repository=mock_repository)
    
    @pytest.fixture
    def sample_provider_data(self):
        """Fixture con datos de proveedor"""
        return {
            'name': 'Farmacia Test',
            'email': 'test@farmacia.com',
            'phone': '3001234567',
            'logo_filename': 'logo.jpg'
        }
    
    @pytest.fixture
    def sample_provider(self, sample_provider_data):
        """Fixture con objeto Provider"""
        return Provider(**sample_provider_data)
    
    @pytest.fixture
    def sample_file_storage(self):
        """Fixture para FileStorage"""
        file_storage = MagicMock()
        file_storage.filename = 'test.jpg'
        file_storage.content_type = 'image/jpeg'
        file_storage.seek.return_value = None
        file_storage.tell.return_value = 1024  # 1KB
        return file_storage
    
    def test_provider_service_initialization(self, provider_service):
        """Prueba la inicialización del servicio"""
        assert provider_service is not None
        assert isinstance(provider_service, ProviderService)
    
    def test_provider_service_inheritance(self, provider_service):
        """Prueba que ProviderService hereda de BaseService"""
        from app.services.base_service import BaseService
        
        assert isinstance(provider_service, BaseService)
    
    def test_create_success(self, provider_service, mock_repository, sample_provider_data):
        """Prueba la creación exitosa de un proveedor"""
        mock_repository.get_by_email.return_value = None
        mock_repository.create.return_value = Provider(**sample_provider_data)

        result = provider_service.create(**sample_provider_data)

        mock_repository.get_by_email.assert_called_once_with(sample_provider_data['email'])
        mock_repository.create.assert_called_once()
        assert isinstance(result, Provider)
    
    def test_create_with_duplicate_email(self, provider_service, mock_repository, sample_provider_data):
        """Prueba la creación con email duplicado"""
        mock_repository.get_by_email.return_value = Provider(**sample_provider_data)
        
        with pytest.raises(ValidationError, match="Ya existe un proveedor con este correo electrónico"):
            provider_service.create(**sample_provider_data)
    
    def test_create_with_validation_error(self, provider_service, mock_repository):
        """Prueba la creación con error de validación"""
        invalid_data = {
            'name': '',  # Nombre vacío
            'email': 'test@farmacia.com',
            'phone': '3001234567'
        }
        
        with pytest.raises(ValidationError, match="El campo 'Nombre' es obligatorio"):
            provider_service.create(**invalid_data)
    
    def test_create_with_logo_file(self, provider_service, mock_repository, sample_file_storage):
        """Prueba la creación con archivo de logo"""
        provider_data = {
            'name': 'Farmacia Test',
            'email': 'test@farmacia.com',
            'phone': '3001234567',
            'logo_file': sample_file_storage
        }
        
        mock_repository.get_by_email.return_value = None
        mock_repository.create.return_value = Provider(**provider_data)
        
        with patch.object(provider_service, '_process_logo_file', return_value="processed_logo.jpg") as mock_process:
            result = provider_service.create(**provider_data)
            
            mock_process.assert_called_once_with(sample_file_storage)
            mock_repository.create.assert_called_once()
            assert isinstance(result, Provider)
    
    def test_create_without_logo_file(self, provider_service, mock_repository):
        """Prueba la creación sin archivo de logo"""
        provider_data = {
            'name': 'Farmacia Test',
            'email': 'test@farmacia.com',
            'phone': '3001234567'
        }
        
        mock_repository.get_by_email.return_value = None
        mock_repository.create.return_value = Provider(**provider_data)
        
        result = provider_service.create(**provider_data)
        
        mock_repository.create.assert_called_once()
        assert isinstance(result, Provider)
    
    def test_get_by_id_success(self, provider_service, mock_repository, sample_provider):
        """Prueba obtener proveedor por ID exitosamente"""
        mock_repository.get_by_id.return_value = sample_provider
        
        result = provider_service.get_by_id("test-id")
        
        mock_repository.get_by_id.assert_called_once_with("test-id")
        assert result == sample_provider
    
    def test_get_by_id_not_found(self, provider_service, mock_repository):
        """Prueba obtener proveedor por ID no encontrado"""
        mock_repository.get_by_id.return_value = None
        
        result = provider_service.get_by_id("non-existent-id")
        
        mock_repository.get_by_id.assert_called_once_with("non-existent-id")
        assert result is None
    
    def test_get_all_success(self, provider_service, mock_repository, sample_provider):
        """Prueba obtener todos los proveedores exitosamente"""
        mock_repository.get_all.return_value = [sample_provider]
        
        result = provider_service.get_all()
        
        mock_repository.get_all.assert_called_once()
        assert result == [sample_provider]
    
    def test_get_providers_summary(self, provider_service, mock_repository, sample_provider):
        """Prueba obtener resumen de proveedores"""
        mock_repository.get_all.return_value = [sample_provider]
        
        result = provider_service.get_providers_summary(limit=10, offset=0)
        
        mock_repository.get_all.assert_called_once_with(limit=10, offset=0)
        # get_providers_summary devuelve diccionarios, no objetos Provider
        expected = [{
            'id': sample_provider.id,
            'name': sample_provider.name,
            'email': sample_provider.email,
            'phone': sample_provider.phone
        }]
        assert result == expected
    
    def test_get_providers_count(self, provider_service, mock_repository):
        """Prueba obtener conteo de proveedores"""
        mock_repository.count_all.return_value = 5
        
        result = provider_service.get_providers_count()
        
        mock_repository.count_all.assert_called_once()
        assert result == 5
    
    def test_delete_all_success(self, provider_service, mock_repository):
        """Prueba eliminar todos los proveedores exitosamente"""
        mock_repository.delete_all.return_value = 3
        
        result = provider_service.delete_all()
        
        mock_repository.delete_all.assert_called_once()
        assert result == 3
    
    def test_validate_business_rules_success(self, provider_service, mock_repository):
        """Prueba la validación exitosa de reglas de negocio"""
        provider_data = {
            'name': 'Farmacia Test',
            'email': 'test@farmacia.com',
            'phone': '3001234567'
        }
        
        mock_repository.get_by_email.return_value = None
        
        # No debería lanzar excepción
        provider_service.validate_business_rules(**provider_data)
        
        mock_repository.get_by_email.assert_called_once_with(provider_data['email'])
    
    def test_validate_business_rules_validation_error(self, provider_service, mock_repository):
        """Prueba la validación con error de validación"""
        invalid_data = {
            'name': '',  # Nombre vacío
            'email': 'test@farmacia.com',
            'phone': '3001234567'
        }
        
        with pytest.raises(ValueError, match="El campo 'Nombre' es obligatorio"):
            provider_service.validate_business_rules(**invalid_data)
    
    def test_process_logo_file_success(self, provider_service, sample_file_storage):
        """Prueba el procesamiento exitoso de archivo de logo"""
        with patch.object(provider_service, '_is_allowed_file', return_value=True):
            result = provider_service._process_logo_file(sample_file_storage)
            
            assert result.startswith('logo_')
            assert result.endswith('.jpg')
            assert len(result) > 10  # Debe tener UUID
    
    def test_process_logo_file_empty_filename(self, provider_service):
        """Prueba el procesamiento con nombre de archivo vacío"""
        file_storage = MagicMock()
        file_storage.filename = ""
        
        result = provider_service._process_logo_file(file_storage)
        
        assert result is None
    
    def test_process_logo_file_none(self, provider_service):
        """Prueba el procesamiento con archivo None"""
        result = provider_service._process_logo_file(None)
        
        assert result is None
    
    def test_process_logo_file_invalid_type(self, provider_service, sample_file_storage):
        """Prueba el procesamiento con tipo de archivo inválido"""
        sample_file_storage.filename = "test.txt"
        
        with pytest.raises(ValidationError, match="El archivo debe ser una imagen válida"):
            provider_service._process_logo_file(sample_file_storage)
    
    def test_process_logo_file_too_large(self, provider_service, sample_file_storage):
        """Prueba el procesamiento con archivo muy grande"""
        sample_file_storage.tell.return_value = 3 * 1024 * 1024  # 3MB
        
        with pytest.raises(ValidationError, match="El archivo no puede exceder 2MB"):
            provider_service._process_logo_file(sample_file_storage)
    
    def test_process_logo_file_empty_file(self, provider_service, sample_file_storage):
        """Prueba el procesamiento con archivo vacío"""
        sample_file_storage.tell.return_value = 0
        
        with pytest.raises(ValidationError, match="El archivo está vacío"):
            provider_service._process_logo_file(sample_file_storage)
    
    def test_is_allowed_file_valid_extensions(self, provider_service):
        """Prueba la validación de extensiones válidas"""
        valid_files = ['test.jpg', 'test.jpeg', 'test.png', 'test.gif']
        
        for filename in valid_files:
            assert provider_service._is_allowed_file(filename) is True
    
    def test_is_allowed_file_invalid_extensions(self, provider_service):
        """Prueba la validación de extensiones inválidas"""
        invalid_files = ['test.txt', 'test.pdf', 'test.doc', 'test']
        
        for filename in invalid_files:
            assert provider_service._is_allowed_file(filename) is False
    
    def test_is_allowed_file_none(self, provider_service):
        """Prueba la validación con archivo None"""
        assert provider_service._is_allowed_file(None) is False
    
    def test_is_allowed_file_empty(self, provider_service):
        """Prueba la validación con archivo vacío"""
        assert provider_service._is_allowed_file("") is False
    
    def test_create_with_repository_exception(self, provider_service, mock_repository, sample_provider_data):
        """Prueba la creación con excepción del repositorio"""
        mock_repository.get_by_email.return_value = None
        mock_repository.create.side_effect = Exception("Database error")
        
        with pytest.raises(BusinessLogicError, match="Error al crear proveedor"):
            provider_service.create(**sample_provider_data)
    
    def test_get_by_id_with_repository_exception(self, provider_service, mock_repository):
        """Prueba obtener por ID con excepción del repositorio"""
        mock_repository.get_by_id.side_effect = Exception("Database error")
        
        with pytest.raises(BusinessLogicError, match="Error al obtener proveedor"):
            provider_service.get_by_id("test-id")
    
    def test_get_all_with_repository_exception(self, provider_service, mock_repository):
        """Prueba obtener todos con excepción del repositorio"""
        mock_repository.get_all.side_effect = Exception("Database error")
        
        with pytest.raises(BusinessLogicError, match="Error al obtener proveedores"):
            provider_service.get_all()
    
    def test_delete_all_with_repository_exception(self, provider_service, mock_repository):
        """Prueba la eliminación de todos con excepción del repositorio"""
        mock_repository.delete_all.side_effect = Exception("Error de base de datos")
        
        with pytest.raises(BusinessLogicError, match="Error al eliminar todos los proveedores"):
            provider_service.delete_all()
    
    def test_get_providers_count_with_repository_exception(self, provider_service, mock_repository):
        """Prueba obtener conteo con excepción del repositorio"""
        mock_repository.count_all.side_effect = Exception("Database error")
        
        with pytest.raises(BusinessLogicError, match="Error al contar proveedores"):
            provider_service.get_providers_count()
    
    def test_validate_business_rules_email_duplicate(self, provider_service, mock_repository):
        """Prueba la validación con email duplicado"""
        provider_data = {
            'name': 'Farmacia Test',
            'email': 'test@farmacia.com',
            'phone': '3001234567'
        }
        
        mock_repository.get_by_email.return_value = Provider(**provider_data)
        
        with pytest.raises(ValueError, match="Ya existe un proveedor con este correo electrónico"):
            provider_service.validate_business_rules(**provider_data)
    
    def test_validate_business_rules_valid_data(self, provider_service, mock_repository):
        """Prueba la validación con datos válidos"""
        provider_data = {
            'name': 'Farmacia Test',
            'email': 'test@farmacia.com',
            'phone': '3001234567'
        }
        
        mock_repository.get_by_email.return_value = None
        
        # No debería lanzar excepción
        provider_service.validate_business_rules(**provider_data)
        
        mock_repository.get_by_email.assert_called_once_with(provider_data['email'])
