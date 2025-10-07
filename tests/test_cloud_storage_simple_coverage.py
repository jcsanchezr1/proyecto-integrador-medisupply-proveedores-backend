"""
Pruebas simples para mejorar coverage de CloudStorageService
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.cloud_storage_service import CloudStorageService
from app.config.settings import Config
from werkzeug.datastructures import FileStorage
import io

# Los mocks de Google Cloud Storage se manejan en conftest.py


class TestCloudStorageSimpleCoverage:
    """Pruebas simples para mejorar coverage de CloudStorageService"""

    @pytest.fixture
    def mock_config(self):
        """Mock de configuración"""
        config = MagicMock()
        config.BUCKET_NAME = "test-bucket"
        config.BUCKET_FOLDER = "providers"
        config.MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB
        config.ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "gif"]
        config.GCP_PROJECT_ID = "test-project"
        config.GOOGLE_APPLICATION_CREDENTIALS = "/path/to/credentials.json"
        return config

    def test_generate_unique_filename_no_extension(self, mock_config):
        """Prueba generación de nombre único sin extensión - líneas 108-110"""
        with patch('app.services.cloud_storage_service.Config', return_value=mock_config):
            service = CloudStorageService()
            filename = service.generate_unique_filename("test", "logo")
            
            assert filename.startswith("logo_")
            assert filename.endswith(".jpg")
            assert len(filename) > 10

    def test_generate_unique_filename_empty(self, mock_config):
        """Prueba generación de nombre único con archivo vacío - líneas 108-110"""
        with patch('app.services.cloud_storage_service.Config', return_value=mock_config):
            service = CloudStorageService()
            filename = service.generate_unique_filename("", "logo")
            
            assert filename.startswith("logo_")
            assert filename.endswith(".jpg")
            assert len(filename) > 10

    def test_validate_image_file_no_extension(self, mock_config):
        """Prueba validación sin extensión"""
        with patch('app.services.cloud_storage_service.Config', return_value=mock_config):
            service = CloudStorageService()
            file_storage = MagicMock()
            file_storage.filename = "test"
            file_storage.seek.return_value = None
            file_storage.tell.return_value = 1024
            
            is_valid, message = service.validate_image_file(file_storage)
            
            assert is_valid is False
            assert message == "El archivo no tiene extensión"

    def test_validate_image_file_empty_file(self, mock_config):
        """Prueba validación de archivo vacío"""
        with patch('app.services.cloud_storage_service.Config', return_value=mock_config):
            service = CloudStorageService()
            file_storage = MagicMock()
            file_storage.filename = "test.jpg"
            file_storage.seek.return_value = None
            file_storage.tell.return_value = 0
            
            is_valid, message = service.validate_image_file(file_storage)
            
            assert is_valid is False
            assert message == "El archivo está vacío"

    def test_validate_image_file_invalid_image(self, mock_config):
        """Prueba validación de imagen inválida"""
        with patch('app.services.cloud_storage_service.Config', return_value=mock_config):
            service = CloudStorageService()
            file_storage = MagicMock()
            file_storage.filename = "test.jpg"
            file_storage.seek.return_value = None
            file_storage.tell.return_value = 1024
            
            with patch('app.services.cloud_storage_service.Image') as mock_image:
                mock_image.open.side_effect = Exception("Invalid image")
                
                is_valid, message = service.validate_image_file(file_storage)
                
                assert is_valid is False
                assert "El archivo no es una imagen válida" in message

    def test_upload_image_validation_fails(self, mock_config):
        """Prueba subida con validación fallida"""
        with patch('app.services.cloud_storage_service.Config', return_value=mock_config):
            service = CloudStorageService()
            file_storage = MagicMock()
            
            with patch.object(service, 'validate_image_file', return_value=(False, "Invalid file")):
                success, message, url = service.upload_image(file_storage, "test.jpg")
                
                assert success is False
                assert message == "Invalid file"
                assert url is None
