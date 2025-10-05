import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.controllers.provider_controller import ProviderController, ProviderDeleteAllController
from app.models.provider_model import Provider
from app.exceptions.custom_exceptions import ValidationError, BusinessLogicError
from werkzeug.datastructures import FileStorage
import io
import json


class TestProviderController:
    """Pruebas unitarias para ProviderController"""
    
    @pytest.fixture
    def app(self):
        """Fixture para aplicación Flask"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app
    
    @pytest.fixture
    def mock_service(self):
        """Fixture para mock del ProviderService"""
        return MagicMock()
    
    @pytest.fixture
    def provider_controller(self, mock_service):
        """Fixture para ProviderController con servicio mockeado"""
        return ProviderController(provider_service=mock_service)
    
    @pytest.fixture
    def sample_provider(self):
        """Fixture para proveedor de muestra"""
        return Provider(
            name="Farmacia Test",
            email="test@farmacia.com",
            phone="3001234567",
            logo_filename="logo.jpg"
        )
    
    @pytest.fixture
    def sample_file_storage(self):
        """Fixture para FileStorage de muestra"""
        file_content = b"fake image content"
        file_storage = FileStorage(
            stream=io.BytesIO(file_content),
            filename="test.jpg",
            content_type="image/jpeg"
        )
        return file_storage
    
    def test_provider_controller_initialization(self, provider_controller):
        """Prueba la inicialización del controlador"""
        assert provider_controller is not None
        assert isinstance(provider_controller, ProviderController)
        assert hasattr(provider_controller, 'provider_service')
    
    @patch('app.controllers.provider_controller.ProviderService')
    def test_get_provider_by_id_success(self, mock_service_class, provider_controller, sample_provider):
        """Prueba la obtención exitosa de un proveedor por ID"""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.get_by_id.return_value = sample_provider

        # Mock del servicio en la instancia del controlador
        provider_controller.provider_service = mock_service

        result = provider_controller.get("test-id")

        mock_service.get_by_id.assert_called_once_with("test-id")
        assert result[0]["message"] == "Proveedor obtenido exitosamente"
        assert result[0]["data"] == sample_provider.to_dict()
        assert result[1] == 200
    
    def test_get_provider_by_id_not_found(self, provider_controller, mock_service):
        """Prueba la obtención de proveedor por ID cuando no se encuentra"""
        mock_service.get_by_id.return_value = None
        
        result = provider_controller.get("test-id")
        
        assert result[0]["error"] == "Proveedor no encontrado"
        assert result[1] == 404
    
    @patch('app.controllers.provider_controller.ProviderService')
    def test_get_provider_by_id_service_error(self, mock_service_class, provider_controller):
        """Prueba la obtención de proveedor por ID con error del servicio"""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.get_by_id.side_effect = Exception("Error de base de datos")
        
        # Mock del servicio en la instancia del controlador
        provider_controller.provider_service = mock_service
        
        with patch.object(provider_controller, 'handle_exception') as mock_handle:
            mock_handle.return_value = ({"error": "Error temporal"}, 500)
            result = provider_controller.get("test-id")
            
            mock_handle.assert_called_once()
            assert result[1] == 500
    
    def test_get_providers_list_success(self, app, provider_controller, mock_service, sample_provider):
        """Prueba la obtención exitosa de la lista de proveedores"""
        mock_service.get_providers_summary.return_value = [sample_provider]
        mock_service.get_providers_count.return_value = 1
        
        with app.test_request_context('/providers?page=1&per_page=10'):
            result = provider_controller.get()
            
            assert result[0]["message"] == "Lista de proveedores obtenida exitosamente"
            assert "providers" in result[0]["data"]
            assert "pagination" in result[0]["data"]
            assert result[1] == 200
    
    @patch('app.controllers.provider_controller.ProviderService')
    def test_get_providers_list_invalid_page(self, mock_service_class, app, provider_controller):
        """Prueba la obtención de lista con página inválida"""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        
        with app.test_request_context('/providers?page=0&per_page=10'):
            result = provider_controller.get()
            
            assert result[0]["error"] == "El parámetro 'page' debe ser mayor a 0"
            assert result[1] == 400
    
    @patch('app.controllers.provider_controller.ProviderService')
    def test_get_providers_list_invalid_per_page(self, mock_service_class, app, provider_controller):
        """Prueba la obtención de lista con per_page inválido"""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        
        with app.test_request_context('/providers?page=1&per_page=150'):
            result = provider_controller.get()
            
            assert result[0]["error"] == "El parámetro 'per_page' debe estar entre 1 y 100"
            assert result[1] == 400
    
    @patch('app.controllers.provider_controller.ProviderService')
    def test_get_providers_list_service_error(self, mock_service_class, app, provider_controller):
        """Prueba la obtención de lista con error del servicio"""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.get_providers_summary.side_effect = Exception("Error de base de datos")

        # Mock del servicio en la instancia del controlador
        provider_controller.provider_service = mock_service

        with app.test_request_context('/providers?page=1&per_page=10'):
            with patch.object(provider_controller, 'handle_exception') as mock_handle:
                mock_handle.return_value = ({"error": "Error temporal"}, 500)
                result = provider_controller.get()

                mock_handle.assert_called_once()
                assert result[1] == 500
    
    @patch('app.controllers.provider_controller.ProviderService')
    def test_post_json_success(self, mock_service_class, app, provider_controller, sample_provider):
        """Prueba la creación exitosa con JSON"""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.create_provider_with_validation.return_value = sample_provider

        # Mock del servicio en la instancia del controlador
        provider_controller.provider_service = mock_service

        with app.test_request_context(json={
            "name": "Farmacia Test",
            "email": "test@farmacia.com",
            "phone": "3001234567"
        }):
            result = provider_controller.post()

            assert result[0]["message"] == "Proveedor registrado exitosamente"
            assert result[0]["data"] == sample_provider.to_dict()
            assert result[1] == 201
    
    @patch('app.controllers.provider_controller.ProviderService')
    def test_post_multipart_success(self, mock_service_class, app, provider_controller, sample_provider, sample_file_storage):
        """Prueba la creación exitosa con multipart"""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.create_provider_with_validation.return_value = sample_provider

        # Mock del servicio en la instancia del controlador
        provider_controller.provider_service = mock_service

        with app.test_request_context():
            with patch('app.controllers.provider_controller.request') as mock_request:
                mock_request.content_type = 'multipart/form-data'
                # Mock form como un objeto que tiene to_dict()
                mock_form = MagicMock()
                mock_form.to_dict.return_value = {
                    "name": "Farmacia Test",
                    "email": "test@farmacia.com",
                    "phone": "3001234567"
                }
                mock_request.form = mock_form
                mock_request.files = {"logo": sample_file_storage}
                
                result = provider_controller.post()

                assert result[0]["message"] == "Proveedor registrado exitosamente"
                assert result[0]["data"] == sample_provider.to_dict()
                assert result[1] == 201
    
    @patch('app.controllers.provider_controller.ProviderService')
    def test_post_validation_error(self, mock_service_class, app, provider_controller):
        """Prueba la creación con error de validación"""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.create_provider_with_validation.side_effect = ValidationError("Error de validación")

        # Mock del servicio en la instancia del controlador
        provider_controller.provider_service = mock_service

        with app.test_request_context(json={
            "name": "Farmacia Test",
            "email": "test@farmacia.com",
            "phone": "3001234567"
        }):
            result = provider_controller.post()

            assert result[0]["error"] == "Error de validación"
            assert result[1] == 400
    
    @patch('app.controllers.provider_controller.ProviderService')
    def test_post_business_logic_error(self, mock_service_class, app, provider_controller):
        """Prueba la creación con error de lógica de negocio"""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.create_provider_with_validation.side_effect = BusinessLogicError("Error de negocio")

        # Mock del servicio en la instancia del controlador
        provider_controller.provider_service = mock_service

        with app.test_request_context(json={
            "name": "Farmacia Test",
            "email": "test@farmacia.com",
            "phone": "3001234567"
        }):
            result = provider_controller.post()

            assert result[0]["error"] == "Error de negocio: Error de negocio"
            assert result[1] == 500
    
    @patch('app.controllers.provider_controller.ProviderService')
    def test_post_generic_error(self, mock_service_class, app, provider_controller):
        """Prueba la creación con error genérico"""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.create_provider_with_validation.side_effect = Exception("Error genérico")

        # Mock del servicio en la instancia del controlador
        provider_controller.provider_service = mock_service

        with app.test_request_context(json={
            "name": "Farmacia Test",
            "email": "test@farmacia.com",
            "phone": "3001234567"
        }):
            result = provider_controller.post()

            assert result[0]["error"] == "Error del sistema: Error genérico"
            assert result[1] == 500
    
    @patch('app.controllers.provider_controller.ProviderService')
    def test_post_invalid_content_type(self, mock_service_class, app, provider_controller):
        """Prueba la creación con tipo de contenido inválido"""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service

        with app.test_request_context():
            result = provider_controller.post()

            assert result[0]["error"] == "Content-Type no soportado. Use application/json o multipart/form-data"
            assert result[1] == 400
    
    @patch('app.controllers.provider_controller.ProviderService')
    def test_post_json_malformed(self, mock_service_class, app, provider_controller):
        """Prueba la creación con JSON malformado"""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service

        with app.test_request_context(headers={'Content-Type': 'application/json'}):
            with patch.object(provider_controller, '_process_json_request') as mock_process:
                mock_process.side_effect = ValidationError("Error al procesar JSON: JSON malformado")

            result = provider_controller.post()

            assert result[0]["error"] == "Error al procesar JSON: 400 Bad Request: The browser (or proxy) sent a request that this server could not understand."
            assert result[1] == 400
    
    def test_process_json_request(self, app, provider_controller):
        """Prueba el procesamiento de request JSON"""
        with app.test_request_context(json={
            "name": "Farmacia Test",
            "email": "test@farmacia.com",
            "phone": "3001234567"
        }):
            result = provider_controller._process_json_request()
            
            assert result["name"] == "Farmacia Test"
            assert result["email"] == "test@farmacia.com"
            assert result["phone"] == "3001234567"
            assert result["logo_file"] is None
    
    def test_process_multipart_request(self, app, provider_controller, sample_file_storage):
        """Prueba el procesamiento de request multipart"""
        with app.test_request_context():
            with patch('app.controllers.provider_controller.request') as mock_request:
                # Mock form como un objeto que tiene to_dict()
                mock_form = MagicMock()
                mock_form.to_dict.return_value = {
                    "name": "Farmacia Test",
                    "email": "test@farmacia.com",
                    "phone": "3001234567"
                }
                mock_request.form = mock_form
                mock_request.files = {"logo": sample_file_storage}
                
                result = provider_controller._process_multipart_request()
                
                assert result["name"] == "Farmacia Test"
                assert result["email"] == "test@farmacia.com"
                assert result["phone"] == "3001234567"
                assert result["logo_file"] == sample_file_storage
    
    def test_process_multipart_request_without_logo(self, app, provider_controller):
        """Prueba el procesamiento de request multipart sin logo"""
        with app.test_request_context():
            with patch('app.controllers.provider_controller.request') as mock_request:
                # Mock form como un objeto que tiene to_dict()
                mock_form = MagicMock()
                mock_form.to_dict.return_value = {
                    "name": "Farmacia Test",
                    "email": "test@farmacia.com",
                    "phone": "3001234567"
                }
                mock_request.form = mock_form
                mock_request.files = {}
                
                result = provider_controller._process_multipart_request()
                
                assert result["name"] == "Farmacia Test"
                assert result["email"] == "test@farmacia.com"
                assert result["phone"] == "3001234567"
                assert result["logo_file"] is None


class TestProviderDeleteAllController:
    """Pruebas unitarias para ProviderDeleteAllController"""
    
    @pytest.fixture
    def delete_controller(self):
        """Fixture para ProviderDeleteAllController"""
        return ProviderDeleteAllController()
    
    @patch('app.controllers.provider_controller.ProviderService')
    def test_delete_all_success(self, mock_service_class, delete_controller):
        """Prueba la eliminación exitosa de todos los proveedores"""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.delete_all.return_value = 5

        # Mock del servicio en la instancia del controlador
        delete_controller.provider_service = mock_service

        result = delete_controller.delete()

        mock_service.delete_all.assert_called_once()
        assert result[0]["message"] == "Se eliminaron 5 proveedores exitosamente"
        assert result[0]["data"]["deleted_count"] == 5
        assert result[1] == 200
    
    @patch('app.controllers.provider_controller.ProviderService')
    def test_delete_all_service_error(self, mock_service_class, delete_controller):
        """Prueba la eliminación con error del servicio"""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.delete_all.side_effect = Exception("Error de base de datos")

        # Mock del servicio en la instancia del controlador
        delete_controller.provider_service = mock_service

        result = delete_controller.delete()

        assert result[0]["error"] == "Error temporal del sistema. Contacte soporte técnico si persiste"
        assert result[1] == 500
    
    @patch('app.controllers.provider_controller.ProviderService')
    def test_delete_all_zero_providers(self, mock_service_class, delete_controller):
        """Prueba la eliminación cuando no hay proveedores"""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.delete_all.return_value = 0

        # Mock del servicio en la instancia del controlador
        delete_controller.provider_service = mock_service

        result = delete_controller.delete()

        assert result[0]["message"] == "Se eliminaron 0 proveedores exitosamente"
        assert result[0]["data"]["deleted_count"] == 0
        assert result[1] == 200
