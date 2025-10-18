import pytest
from unittest.mock import patch, MagicMock
from app.models.base_model import BaseModel


class TestBaseModel:
    """Pruebas unitarias para BaseModel"""
    
    def test_to_dict_abstract_method(self):
        """Prueba que to_dict es un método abstracto"""
        with pytest.raises(TypeError):
            BaseModel()
    
    def test_validate_abstract_method(self):
        """Prueba que validate es un método abstracto"""
        with pytest.raises(TypeError):
            BaseModel()
    
    def test_abstract_methods_exist(self):
        """Prueba que los métodos abstractos existen en la clase"""
        assert hasattr(BaseModel, 'to_dict')
        assert hasattr(BaseModel, 'validate')
        assert BaseModel.to_dict.__isabstractmethod__
        assert BaseModel.validate.__isabstractmethod__
