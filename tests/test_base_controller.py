import pytest
from unittest.mock import patch, MagicMock
from app.controllers.base_controller import BaseController
from app.exceptions.custom_exceptions import ValidationError, BusinessLogicError
import traceback


class TestBaseController:
    """Pruebas unitarias para BaseController"""
    
    def test_base_controller_initialization(self):
        """Prueba la inicialización del controlador base"""
        controller = BaseController()
        assert controller is not None
        assert isinstance(controller, BaseController)
    
    def test_handle_exception_validation_error(self):
        """Prueba el manejo de ValidationError"""
        controller = BaseController()
        error = ValidationError("Error de validación")
        
        result = controller.handle_exception(error)
        
        assert result[0]["error"] == "Error de validación"
        assert result[1] == 500
    
    def test_handle_exception_business_logic_error(self):
        """Prueba el manejo de BusinessLogicError"""
        controller = BaseController()
        error = BusinessLogicError("Error de negocio")
        
        result = controller.handle_exception(error)
        
        assert result[0]["error"] == "Error de negocio"
        assert result[1] == 500
    
    def test_handle_exception_generic_exception(self):
        """Prueba el manejo de excepción genérica"""
        controller = BaseController()
        error = Exception("Error genérico")
        
        result = controller.handle_exception(error)
        
        assert result[0]["error"] == "Error genérico"
        assert result[1] == 500
    
    def test_success_response_with_data(self):
        """Prueba la respuesta exitosa con datos"""
        controller = BaseController()
        data = {"id": "123", "name": "Test"}
        message = "Operación exitosa"
        
        result = controller.success_response(data=data, message=message)
        
        assert result[0]["message"] == message
        assert result[0]["data"] == data
        assert result[1] == 200
    
    def test_success_response_without_data(self):
        """Prueba la respuesta exitosa sin datos"""
        controller = BaseController()
        message = "Operación exitosa"
        
        result = controller.success_response(message=message)
        
        assert result[0]["message"] == message
        assert "data" not in result[0]
        assert result[1] == 200
    
    def test_success_response_with_custom_status(self):
        """Prueba la respuesta exitosa con status personalizado"""
        controller = BaseController()
        data = {"id": "123"}
        message = "Creado exitosamente"
        
        result = controller.success_response(data=data, message=message, status_code=201)
        
        assert result[0]["message"] == message
        assert result[0]["data"] == data
        assert result[1] == 201
    
    def test_error_response_basic(self):
        """Prueba la respuesta de error básica"""
        controller = BaseController()
        message = "Error de validación"
        
        result = controller.error_response(message)
        
        assert result[0]["error"] == message
        assert result[1] == 400
    
    def test_error_response_with_custom_status(self):
        """Prueba la respuesta de error con status personalizado"""
        controller = BaseController()
        message = "Error interno"
        
        result = controller.error_response(message, status_code=500)
        
        assert result[0]["error"] == message
        assert result[1] == 500
    
    def test_error_response_with_details(self):
        """Prueba la respuesta de error con detalles"""
        controller = BaseController()
        message = "Error de validación"
        
        result = controller.error_response(message, status_code=400)
        
        assert result[0]["error"] == message
        assert result[1] == 400
    
    
    def test_success_response_data_types(self):
        """Prueba que success_response maneja diferentes tipos de datos"""
        controller = BaseController()
        
        # Lista
        data_list = [{"id": "1"}, {"id": "2"}]
        result = controller.success_response(data=data_list, message="Lista obtenida")
        assert result[0]["data"] == data_list
        
        # String
        data_string = "simple string"
        result = controller.success_response(data=data_string, message="String obtenido")
        assert result[0]["data"] == data_string
        
        # None
        result = controller.success_response(data=None, message="None obtenido")
        assert "data" not in result[0]
    
    def test_error_response_message_types(self):
        """Prueba que error_response maneja diferentes tipos de mensajes"""
        controller = BaseController()
        
        # String normal
        result = controller.error_response("Error string")
        assert result[0]["error"] == "Error string"
        
        # String vacío
        result = controller.error_response("")
        assert result[0]["error"] == ""
        
        # None
        result = controller.error_response(None)
        assert result[0]["error"] is None
