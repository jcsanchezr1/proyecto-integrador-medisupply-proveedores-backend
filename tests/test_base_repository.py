import pytest
from unittest.mock import patch, MagicMock
from app.repositories.base_repository import BaseRepository
from app.models.provider_model import Provider


class TestBaseRepository:
    """Pruebas unitarias para BaseRepository"""
    
    def test_base_repository_abstract_methods(self):
        """Prueba que BaseRepository tiene métodos abstractos"""
        assert hasattr(BaseRepository, 'create')
        assert hasattr(BaseRepository, 'get_by_id')
        assert hasattr(BaseRepository, 'get_all')
        assert hasattr(BaseRepository, 'get_by_email')
        assert BaseRepository.create.__isabstractmethod__
        assert BaseRepository.get_by_id.__isabstractmethod__
        assert BaseRepository.get_all.__isabstractmethod__
        assert BaseRepository.get_by_email.__isabstractmethod__
    
    def test_base_repository_cannot_be_instantiated(self):
        """Prueba que BaseRepository no puede ser instanciado directamente"""
        with pytest.raises(TypeError):
            BaseRepository()
    
    def test_base_repository_abstract_methods_exist(self):
        """Prueba que todos los métodos abstractos existen"""
        abstract_methods = ['create', 'get_by_id', 'get_all', 'get_by_email']
        
        for method_name in abstract_methods:
            assert hasattr(BaseRepository, method_name)
            method = getattr(BaseRepository, method_name)
            assert method.__isabstractmethod__
    
    def test_base_repository_inheritance(self):
        """Prueba que BaseRepository es una clase abstracta"""
        assert hasattr(BaseRepository, '__abstractmethods__')
        assert len(BaseRepository.__abstractmethods__) > 0
