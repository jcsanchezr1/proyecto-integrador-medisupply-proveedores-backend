import pytest
from app.exceptions.custom_exceptions import ValidationError, BusinessLogicError


class TestValidationError:
    """Pruebas unitarias para ValidationError"""
    
    def test_validation_error_creation(self):
        """Prueba la creación de ValidationError"""
        error = ValidationError("Mensaje de error")
        
        assert str(error) == "Mensaje de error"
        assert isinstance(error, Exception)
    
    def test_validation_error_inheritance(self):
        """Prueba que ValidationError hereda de Exception"""
        error = ValidationError("Mensaje de error")
        
        assert isinstance(error, Exception)
    
    def test_validation_error_empty_message(self):
        """Prueba ValidationError con mensaje vacío"""
        error = ValidationError("")
        
        assert str(error) == ""
    
    def test_validation_error_none_message(self):
        """Prueba ValidationError con mensaje None"""
        error = ValidationError(None)
        
        assert str(error) == "None"


class TestBusinessLogicError:
    """Pruebas unitarias para BusinessLogicError"""
    
    def test_business_logic_error_creation(self):
        """Prueba la creación de BusinessLogicError"""
        error = BusinessLogicError("Mensaje de error de negocio")
        
        assert str(error) == "Mensaje de error de negocio"
        assert isinstance(error, Exception)
    
    def test_business_logic_error_inheritance(self):
        """Prueba que BusinessLogicError hereda de Exception"""
        error = BusinessLogicError("Mensaje de error de negocio")
        
        assert isinstance(error, Exception)
    
    def test_business_logic_error_empty_message(self):
        """Prueba BusinessLogicError con mensaje vacío"""
        error = BusinessLogicError("")
        
        assert str(error) == ""
    
    def test_business_logic_error_none_message(self):
        """Prueba BusinessLogicError con mensaje None"""
        error = BusinessLogicError(None)
        
        assert str(error) == "None"
    
    def test_business_logic_error_different_from_validation_error(self):
        """Prueba que BusinessLogicError es diferente de ValidationError"""
        validation_error = ValidationError("Error de validación")
        business_error = BusinessLogicError("Error de negocio")
        
        assert not isinstance(validation_error, BusinessLogicError)
        assert not isinstance(business_error, ValidationError)
    
    def test_exception_handling_validation_error(self):
        """Prueba el manejo de ValidationError en try-except"""
        try:
            raise ValidationError("Error de validación")
        except ValidationError as e:
            assert str(e) == "Error de validación"
        except Exception:
            pytest.fail("ValidationError no fue capturada correctamente")
    
    def test_exception_handling_business_logic_error(self):
        """Prueba el manejo de BusinessLogicError en try-except"""
        try:
            raise BusinessLogicError("Error de negocio")
        except BusinessLogicError as e:
            assert str(e) == "Error de negocio"
        except Exception:
            pytest.fail("BusinessLogicError no fue capturada correctamente")
    
    def test_exception_handling_generic_exception(self):
        """Prueba el manejo de excepciones genéricas"""
        try:
            raise ValidationError("Error de validación")
        except Exception as e:
            assert str(e) == "Error de validación"
    
    def test_exception_handling_specific_exception(self):
        """Prueba el manejo específico de ValidationError vs BusinessLogicError"""
        try:
            raise ValidationError("Error de validación")
        except ValidationError as e:
            assert str(e) == "Error de validación"
        except BusinessLogicError:
            pytest.fail("ValidationError fue capturada como BusinessLogicError")
    
    def test_exception_handling_specific_business_logic_error(self):
        """Prueba el manejo específico de BusinessLogicError vs ValidationError"""
        try:
            raise BusinessLogicError("Error de negocio")
        except BusinessLogicError as e:
            assert str(e) == "Error de negocio"
        except ValidationError:
            pytest.fail("BusinessLogicError fue capturada como ValidationError")
