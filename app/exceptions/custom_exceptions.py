"""
Excepciones personalizadas del sistema de proveedores
"""
from typing import Optional


class ProviderException(Exception):
    """Excepción base para el sistema de proveedores"""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ValidationError(ProviderException):
    """Excepción para errores de validación"""
    
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")


class BusinessLogicError(ProviderException):
    """Excepción para errores de lógica de negocio"""
    
    def __init__(self, message: str):
        super().__init__(message, "BUSINESS_LOGIC_ERROR")


class DatabaseError(ProviderException):
    """Excepción para errores de base de datos"""
    
    def __init__(self, message: str):
        super().__init__(message, "DATABASE_ERROR")


class FileProcessingError(ProviderException):
    """Excepción para errores de procesamiento de archivos"""
    
    def __init__(self, message: str):
        super().__init__(message, "FILE_PROCESSING_ERROR")


class NotFoundError(ProviderException):
    """Excepción para recursos no encontrados"""
    
    def __init__(self, message: str):
        super().__init__(message, "NOT_FOUND_ERROR")