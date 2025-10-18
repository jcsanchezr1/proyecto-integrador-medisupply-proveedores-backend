import pytest
from unittest.mock import patch, MagicMock
from app.config.settings import Config, DevelopmentConfig, ProductionConfig, TestingConfig
import os


class TestConfig:
    """Pruebas unitarias para la configuración de Config"""
    
    def test_config_initialization(self):
        """Prueba la inicialización de Config"""
        config = Config()
        
        assert config is not None
        assert isinstance(config, Config)
    
    def test_config_attributes(self):
        """Prueba que Config tiene todos los atributos esperados"""
        config = Config()
        
        # Verificar atributos de base de datos
        assert hasattr(config, 'DATABASE_URL')
        assert hasattr(config, 'SQLALCHEMY_DATABASE_URI')
        assert hasattr(config, 'SQLALCHEMY_TRACK_MODIFICATIONS')
        assert hasattr(config, 'SQLALCHEMY_ENGINE_OPTIONS')
        
        # Verificar atributos de Flask
        assert hasattr(config, 'SECRET_KEY')
        assert hasattr(config, 'DEBUG')
        assert hasattr(config, 'HOST')
        assert hasattr(config, 'PORT')
        
        # Verificar atributos de archivos
        assert hasattr(config, 'MAX_CONTENT_LENGTH')
        assert hasattr(config, 'UPLOAD_FOLDER')
        assert hasattr(config, 'ALLOWED_EXTENSIONS')
        
        # Verificar atributos de logging
        assert hasattr(config, 'LOG_LEVEL')
    
    def test_sqlalchemy_track_modifications_false(self):
        """Prueba que SQLALCHEMY_TRACK_MODIFICATIONS está deshabilitado"""
        config = Config()
        
        assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False
        assert config.SQLALCHEMY_TRACK_MODIFICATIONS is not True
    
    def test_database_uri_equals_database_url(self):
        """Prueba que SQLALCHEMY_DATABASE_URI es igual a DATABASE_URL"""
        config = Config()
        
        assert config.SQLALCHEMY_DATABASE_URI == config.DATABASE_URL
    
    def test_max_content_length(self):
        """Prueba que MAX_CONTENT_LENGTH está configurado correctamente"""
        config = Config()
        
        # 2MB en bytes
        expected_size = 2 * 1024 * 1024
        assert config.MAX_CONTENT_LENGTH == expected_size
    
    def test_allowed_extensions(self):
        """Prueba que ALLOWED_EXTENSIONS contiene las extensiones correctas"""
        config = Config()
        
        expected_extensions = {'jpg', 'jpeg', 'png', 'gif'}
        assert config.ALLOWED_EXTENSIONS == expected_extensions
    
    def test_sqlalchemy_engine_options(self):
        """Prueba que SQLALCHEMY_ENGINE_OPTIONS está configurado correctamente"""
        config = Config()
        
        assert isinstance(config.SQLALCHEMY_ENGINE_OPTIONS, dict)
        assert 'pool_pre_ping' in config.SQLALCHEMY_ENGINE_OPTIONS
        assert 'pool_recycle' in config.SQLALCHEMY_ENGINE_OPTIONS
        assert config.SQLALCHEMY_ENGINE_OPTIONS['pool_pre_ping'] is True
        assert config.SQLALCHEMY_ENGINE_OPTIONS['pool_recycle'] == 300


class TestDevelopmentConfig:
    """Pruebas unitarias para DevelopmentConfig"""
    
    def test_development_config_inheritance(self):
        """Prueba que DevelopmentConfig hereda de Config"""
        dev_config = DevelopmentConfig()
        
        assert isinstance(dev_config, Config)
    
    def test_development_config_debug_true(self):
        """Prueba que DevelopmentConfig tiene DEBUG=True"""
        dev_config = DevelopmentConfig()
        
        assert dev_config.DEBUG is True
    
    def test_development_config_sqlalchemy_echo_true(self):
        """Prueba que DevelopmentConfig tiene SQLALCHEMY_ECHO=True"""
        dev_config = DevelopmentConfig()
        
        assert dev_config.SQLALCHEMY_ECHO is True


class TestProductionConfig:
    """Pruebas unitarias para ProductionConfig"""
    
    def test_production_config_inheritance(self):
        """Prueba que ProductionConfig hereda de Config"""
        prod_config = ProductionConfig()
        
        assert isinstance(prod_config, Config)
    
    def test_production_config_debug_false(self):
        """Prueba que ProductionConfig tiene DEBUG=False"""
        prod_config = ProductionConfig()
        
        assert prod_config.DEBUG is False
    
    def test_production_config_sqlalchemy_echo_false(self):
        """Prueba que ProductionConfig tiene SQLALCHEMY_ECHO=False"""
        prod_config = ProductionConfig()
        
        assert prod_config.SQLALCHEMY_ECHO is False


class TestTestingConfig:
    """Pruebas unitarias para TestingConfig"""
    
    def test_testing_config_inheritance(self):
        """Prueba que TestingConfig hereda de Config"""
        test_config = TestingConfig()
        
        assert isinstance(test_config, Config)
    
    def test_testing_config_testing_true(self):
        """Prueba que TestingConfig tiene TESTING=True"""
        test_config = TestingConfig()
        
        assert test_config.TESTING is True
    
    def test_testing_config_sqlite_database(self):
        """Prueba que TestingConfig usa SQLite en memoria"""
        test_config = TestingConfig()
        
        assert test_config.SQLALCHEMY_DATABASE_URI == 'sqlite:///:memory:'
    
    def test_testing_config_csrf_disabled(self):
        """Prueba que TestingConfig tiene WTF_CSRF_ENABLED=False"""
        test_config = TestingConfig()
        
        assert test_config.WTF_CSRF_ENABLED is False


class TestConfigByName:
    """Pruebas unitarias para config_by_name"""
    
    def test_config_by_name_import(self):
        """Prueba que config_by_name se puede importar"""
        from app.config.settings import config_by_name
        
        assert config_by_name is not None
        assert isinstance(config_by_name, dict)
    
    def test_config_by_name_contains_all_configs(self):
        """Prueba que config_by_name contiene todas las configuraciones"""
        from app.config.settings import config_by_name
        
        expected_configs = ['development', 'production', 'testing', 'default']
        
        for config_name in expected_configs:
            assert config_name in config_by_name
    
    def test_config_by_name_development_config(self):
        """Prueba que config_by_name['development'] es DevelopmentConfig"""
        from app.config.settings import config_by_name, DevelopmentConfig
        
        assert config_by_name['development'] == DevelopmentConfig
    
    def test_config_by_name_production_config(self):
        """Prueba que config_by_name['production'] es ProductionConfig"""
        from app.config.settings import config_by_name, ProductionConfig
        
        assert config_by_name['production'] == ProductionConfig
    
    def test_config_by_name_testing_config(self):
        """Prueba que config_by_name['testing'] es TestingConfig"""
        from app.config.settings import config_by_name, TestingConfig
        
        assert config_by_name['testing'] == TestingConfig
    
    def test_config_by_name_default_config(self):
        """Prueba que config_by_name['default'] es DevelopmentConfig"""
        from app.config.settings import config_by_name, DevelopmentConfig
        
        assert config_by_name['default'] == DevelopmentConfig