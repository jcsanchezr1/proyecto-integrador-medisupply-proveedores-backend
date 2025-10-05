"""
Servicio de Proveedores - Lógica de negocio para proveedores
"""
from typing import List, Optional
from werkzeug.datastructures import FileStorage
import os
import uuid

from .base_service import BaseService
from ..repositories.provider_repository import ProviderRepository
from ..models.provider_model import Provider
from ..exceptions.custom_exceptions import ValidationError, BusinessLogicError


class ProviderService(BaseService):
    """Servicio para operaciones de negocio de proveedores"""
    
    def __init__(self):
        self.provider_repository = ProviderRepository()
    
    def create(self, **kwargs) -> Provider:
        """Crea un nuevo proveedor con validaciones de negocio"""
        try:
            # Validar reglas de negocio
            self.validate_business_rules(**kwargs)
            
            # Procesar archivo de logo si se proporciona
            logo_file = kwargs.get('logo_file')
            if logo_file is not None:
                logo_filename = self._process_logo_file(logo_file)
                if logo_filename:
                    kwargs['logo_filename'] = logo_filename
            
            # Crear proveedor
            provider = self.provider_repository.create(**kwargs)
            
            return provider
            
        except ValueError as e:
            raise ValidationError(str(e))
        except Exception as e:
            raise BusinessLogicError(f"Error al crear proveedor: {str(e)}")
    
    def get_by_id(self, provider_id: str) -> Optional[Provider]:
        """Obtiene un proveedor por ID"""
        try:
            return self.provider_repository.get_by_id(provider_id)
        except Exception as e:
            raise BusinessLogicError(f"Error al obtener proveedor: {str(e)}")
    
    def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[Provider]:
        """Obtiene todos los proveedores con paginación"""
        try:
            return self.provider_repository.get_all(limit=limit, offset=offset)
        except Exception as e:
            raise BusinessLogicError(f"Error al obtener proveedores: {str(e)}")
    
    def delete_all(self) -> int:
        """Elimina todos los proveedores de la base de datos"""
        try:
            return self.provider_repository.delete_all()
        except Exception as e:
            raise BusinessLogicError(f"Error al eliminar todos los proveedores: {str(e)}")
    
    
    def validate_business_rules(self, **kwargs) -> None:
        """Valida las reglas de negocio específicas para proveedores"""
        errors = []
        
        # Validar campos obligatorios
        if 'name' in kwargs:
            name = kwargs['name'].strip() if kwargs['name'] else ''
            if not name:
                errors.append("El campo 'Nombre' es obligatorio")
            elif len(name) > 255:
                errors.append("El nombre del proveedor no puede exceder 255 caracteres")
            elif len(name) < 2:
                errors.append("El nombre del proveedor debe tener al menos 2 caracteres")
        
        if 'email' in kwargs:
            email = kwargs['email'].strip() if kwargs['email'] else ''
            if not email:
                errors.append("El campo 'Correo electrónico' es obligatorio")
            elif len(email) > 255:
                errors.append("El correo electrónico no puede exceder 255 caracteres")
            elif '@' not in email or '.' not in email.split('@')[-1]:
                errors.append("El campo 'Correo electrónico' debe tener un formato válido")
        
        if 'phone' in kwargs:
            phone = kwargs['phone'].strip() if kwargs['phone'] else ''
            if not phone:
                errors.append("El campo 'Teléfono' es obligatorio")
            elif len(phone) > 20:
                errors.append("El teléfono no puede exceder 20 caracteres")
            elif len(phone) < 7:
                errors.append("El campo 'Teléfono' debe tener al menos 7 dígitos")
            elif not phone.isdigit():
                errors.append("El campo 'Teléfono' debe contener solo números")
        
        # Validar email único
        if 'email' in kwargs and kwargs['email']:
            existing_provider = self.provider_repository.get_by_email(kwargs['email'].strip())
            if existing_provider:
                errors.append("Ya existe un proveedor con este correo electrónico")
        
        if errors:
            raise ValueError("; ".join(errors))
    
    def _process_logo_file(self, logo_file: Optional[FileStorage]) -> Optional[str]:
        """Procesa el archivo de logo y retorna el nombre del archivo"""
        if not logo_file or not logo_file.filename:
            return None
        
        # Validar que el archivo tenga nombre
        if not logo_file.filename.strip():
            raise ValidationError("El campo 'Logo' debe aceptar únicamente archivos de imagen (JPG, PNG, GIF) con un tamaño máximo de 2MB")
        
        # Validar tipo de archivo (JPG, PNG, GIF)
        if not self._is_allowed_file(logo_file.filename):
            raise ValidationError("El archivo debe ser una imagen válida (JPG, PNG, GIF)")
        
        # Validar tamaño del archivo (2MB máximo)
        logo_file.seek(0, 2)  # Ir al final del archivo
        file_size = logo_file.tell()
        logo_file.seek(0)  # Volver al inicio
        
        if file_size == 0:
            raise ValidationError("El archivo está vacío")
        
        if file_size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError("El archivo no puede exceder 2MB")
        
        # Generar nombre único para el archivo
        provider_model = Provider()
        unique_filename = provider_model.generate_logo_filename(logo_file.filename)
        
        # TODO: Aquí se implementaría la subida al storage y publicación al tópico
        # Por ahora solo retornamos el nombre del archivo
        
        return unique_filename
    
    def _is_allowed_file(self, filename: str) -> bool:
        """Verifica si el archivo está permitido"""
        if '.' not in filename:
            return False
        
        extension = filename.lower().split('.')[-1]
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
        
        return extension in allowed_extensions
    
    def get_providers_summary(self, limit: Optional[int] = None, offset: int = 0) -> List[dict]:
        """Obtiene un resumen de proveedores para listado"""
        try:
            providers = self.get_all(limit=limit, offset=offset)
            
            return [
                {
                    'id': provider.id,
                    'name': provider.name,
                    'email': provider.email,
                    'phone': provider.phone
                }
                for provider in providers
            ]
            
        except Exception as e:
            raise BusinessLogicError(f"Error al obtener resumen de proveedores: {str(e)}")
    
    def get_providers_count(self) -> int:
        """Obtiene el total de proveedores"""
        try:
            return self.provider_repository.count_all()
        except Exception as e:
            raise BusinessLogicError(f"Error al contar proveedores: {str(e)}")
    
    def create_provider_with_validation(self, **kwargs) -> Provider:
        """Crea un proveedor con validaciones completas"""
        try:
            # Crear modelo temporal para validar
            temp_provider = Provider(**kwargs)
            temp_provider.validate()
            
            # Crear proveedor usando el servicio
            return self.create(**kwargs)
            
        except ValueError as e:
            raise ValidationError(str(e))
        except Exception as e:
            raise BusinessLogicError(f"Error al crear proveedor: {str(e)}")