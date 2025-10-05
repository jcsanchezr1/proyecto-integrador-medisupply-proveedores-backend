"""
Configuraciones del sistema de proveedores
"""
import os
from decouple import config


class Config:
    """Configuración base"""
    
    # Configuración de la base de datos
    DATABASE_URL = config(
        'DATABASE_URL', 
        default='postgresql://medisupply_local_user:medisupply_local_password@localhost:5432/medisupply_local_db'
    )
    
    # Configuración de Flask
    SECRET_KEY = config('SECRET_KEY', default='dev-secret-key-change-in-production')
    DEBUG = config('DEBUG', default=True, cast=bool)
    HOST = config('HOST', default='0.0.0.0')
    PORT = config('PORT', default=8080, cast=int)
    
    # Configuración de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Configuración de archivos
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB máximo para archivos
    UPLOAD_FOLDER = config('UPLOAD_FOLDER', default='uploads')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    
    # Configuración de logging
    LOG_LEVEL = config('LOG_LEVEL', default='INFO')


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuración por defecto
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}