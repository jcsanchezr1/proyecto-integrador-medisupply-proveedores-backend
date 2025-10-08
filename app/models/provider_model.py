"""
Modelo de Proveedor - Entidad para gestionar proveedores
"""
import re
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from .base_model import BaseModel


class Provider(BaseModel):
    """Modelo de Proveedor con validaciones específicas"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.name = kwargs.get('name', '')
        self.email = kwargs.get('email', '')
        self.phone = kwargs.get('phone', '')
        self.logo_filename = kwargs.get('logo_filename', '')
        self.logo_url = kwargs.get('logo_url', '')
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'logo_filename': self.logo_filename,
            'logo_url': self.logo_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def validate(self) -> None:
        """Valida los datos del modelo según las reglas de negocio"""
        errors = []
        
        # Validar nombre (obligatorio, solo caracteres alfanuméricos y espacios)
        if not self.name or not self.name.strip():
            errors.append("El campo 'Nombre' es obligatorio")
        elif not re.match(r'^[a-zA-Z0-9\sáéíóúÁÉÍÓÚñÑüÜ]+$', self.name.strip()):
            errors.append("El campo 'Nombre' debe aceptar únicamente caracteres alfabéticos, numéricos y espacios")
        
        # Validar email (obligatorio, formato válido con dominio)
        if not self.email or not self.email.strip():
            errors.append("El campo 'Correo electrónico' es obligatorio")
        elif not self._is_valid_email(self.email.strip()):
            errors.append("El campo 'Correo electrónico' debe validar el formato de email (debe contener '@' y un dominio válido)")
        
        # Validar teléfono (obligatorio, solo números, mínimo 7 dígitos)
        if not self.phone or not self.phone.strip():
            errors.append("El campo 'Teléfono' es obligatorio")
        elif not re.match(r'^\d+$', self.phone.strip()):
            errors.append("El campo 'Teléfono' debe validar que contenga solo números")
        elif len(self.phone.strip()) < 7:
            errors.append("El campo 'Teléfono' debe validar que contenga solo números y una longitud mínima de 7 dígitos")
        
        # Validar logo (opcional, pero si se proporciona debe ser válido)
        if self.logo_filename and not self._is_valid_image_filename(self.logo_filename):
            errors.append("El campo 'Logo' debe aceptar únicamente archivos de imagen (JPG, PNG, GIF) con un tamaño máximo de 2MB")
        
        if errors:
            raise ValueError("; ".join(errors))
    
    def _is_valid_email(self, email: str) -> bool:
        """Valida el formato de email con dominio válido"""
        # Verificar que contenga @
        if '@' not in email:
            return False
        
        # Dividir en usuario y dominio
        parts = email.split('@')
        if len(parts) != 2:
            return False
        
        username, domain = parts
        
        # Verificar que el dominio tenga al menos un punto
        if '.' not in domain:
            return False
        
        # Verificar que el dominio tenga extensión válida
        domain_parts = domain.split('.')
        if len(domain_parts) < 2:
            return False
        
        # Verificar que la extensión tenga al menos 2 caracteres
        extension = domain_parts[-1]
        if len(extension) < 2:
            return False
        
        # Patrón más estricto para validar formato completo
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _is_valid_image_filename(self, filename: str) -> bool:
        """Valida que el nombre del archivo sea de una imagen válida"""
        if not filename:
            return True  # Logo es opcional
        
        # Extensiones permitidas
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
        
        # Obtener extensión del archivo
        if '.' not in filename:
            return False
        
        extension = filename.lower().split('.')[-1]
        return f'.{extension}' in allowed_extensions
    
    def generate_logo_filename(self, original_filename: str) -> str:
        """Genera un nombre único para el archivo de logo"""
        if not original_filename:
            return ''
        
        # Obtener extensión
        if '.' not in original_filename:
            return ''
        
        extension = original_filename.lower().split('.')[-1]
        
        # Generar nombre único con UUID
        unique_id = str(uuid.uuid4())
        return f"logo_{unique_id}.{extension}"
    
    
    def __repr__(self) -> str:
        return f"<Provider(id='{self.id}', name='{self.name}', email='{self.email}')>"