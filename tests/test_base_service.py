import pytest
from unittest.mock import patch, MagicMock
from app.services.base_service import BaseService
from app.models.provider_model import Provider


class TestBaseService:
    """Pruebas unitarias para BaseService"""
    
    def test_base_service_abstract_methods(self):
        """Prueba que BaseService tiene métodos abstractos"""
        assert hasattr(BaseService, 'create')
        assert hasattr(BaseService, 'get_by_id')
        assert hasattr(BaseService, 'get_all')
        assert hasattr(BaseService, 'validate_business_rules')
        assert BaseService.create.__isabstractmethod__
        assert BaseService.get_by_id.__isabstractmethod__
        assert BaseService.get_all.__isabstractmethod__
        assert BaseService.validate_business_rules.__isabstractmethod__
    
    def test_base_service_cannot_be_instantiated(self):
        """Prueba que BaseService no puede ser instanciado directamente"""
        with pytest.raises(TypeError):
            BaseService()
    
    def test_base_service_abstract_methods_exist(self):
        """Prueba que todos los métodos abstractos existen"""
        abstract_methods = ['create', 'get_by_id', 'get_all', 'validate_business_rules']
        
        for method_name in abstract_methods:
            assert hasattr(BaseService, method_name)
            method = getattr(BaseService, method_name)
            assert method.__isabstractmethod__
    
    def test_base_service_inheritance(self):
        """Prueba que BaseService es una clase abstracta"""
        assert hasattr(BaseService, '__abstractmethods__')
        assert len(BaseService.__abstractmethods__) > 0
