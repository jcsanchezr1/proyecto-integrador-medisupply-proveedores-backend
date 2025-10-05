"""
Controlador de Proveedores - Endpoints REST para gestión de proveedores
"""
from flask import request
from flask_restful import Resource
from typing import Dict, Any, Tuple
from werkzeug.datastructures import FileStorage

from .base_controller import BaseController
from ..services.provider_service import ProviderService
from ..exceptions.custom_exceptions import ValidationError, BusinessLogicError, NotFoundError


class ProviderController(BaseController):
    """Controlador para operaciones REST de proveedores"""
    
    def __init__(self):
        self.provider_service = ProviderService()
    
    def get(self, provider_id: str = None) -> Tuple[Dict[str, Any], int]:
        """GET /providers o GET /providers/{id}"""
        try:
            if provider_id:
                # Obtener un proveedor específico
                provider = self.provider_service.get_by_id(provider_id)
                if not provider:
                    return self.error_response("Proveedor no encontrado", 404)
                
                return self.success_response(
                    data=provider.to_dict(),
                    message="Proveedor obtenido exitosamente"
                )
            else:
                # Obtener lista de proveedores con paginación
                page = request.args.get('page', 1, type=int)
                per_page = request.args.get('per_page', 10, type=int)
                
                # Validar parámetros de paginación
                if page < 1:
                    return self.error_response("El parámetro 'page' debe ser mayor a 0", 400)
                
                if per_page < 1 or per_page > 100:
                    return self.error_response("El parámetro 'per_page' debe estar entre 1 y 100", 400)
                
                offset = (page - 1) * per_page
                
                # Obtener proveedores y total
                providers = self.provider_service.get_providers_summary(
                    limit=per_page,
                    offset=offset
                )
                total = self.provider_service.get_providers_count()
                
                # Calcular información de paginación
                total_pages = (total + per_page - 1) // per_page  # Ceiling division
                has_next = page < total_pages
                has_prev = page > 1
                
                return self.success_response(
                    data={
                        'providers': providers,
                        'pagination': {
                            'page': page,
                            'per_page': per_page,
                            'total': total,
                            'total_pages': total_pages,
                            'has_next': has_next,
                            'has_prev': has_prev,
                            'next_page': page + 1 if has_next else None,
                            'prev_page': page - 1 if has_prev else None
                        }
                    },
                    message="Lista de proveedores obtenida exitosamente"
                )
                
        except BusinessLogicError as e:
            return self.error_response(str(e), 500)
        except Exception as e:
            return self.handle_exception(e)
    
    def post(self) -> Tuple[Dict[str, Any], int]:
        """POST /providers - Crear nuevo proveedor (soporta JSON y multipart)"""
        try:
            # Detectar el tipo de contenido
            content_type = request.content_type or ''
            
            if 'application/json' in content_type:
                # Manejar JSON
                provider_data = self._process_json_request()
            elif 'multipart/form-data' in content_type:
                # Manejar formulario multipart
                provider_data = self._process_multipart_request()
            else:
                return self.error_response("Content-Type no soportado. Use application/json o multipart/form-data", 400)
            
            # Crear proveedor
            provider = self.provider_service.create_provider_with_validation(**provider_data)
            
            return self.success_response(
                data=provider.to_dict(),
                message="Proveedor registrado exitosamente",
                status_code=201
            )
            
        except ValidationError as e:
            return self.error_response(str(e), 400)
        except BusinessLogicError as e:
            return self.error_response(f"Error de negocio: {str(e)}", 500)
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"Error en crear proveedor: {error_trace}")  # Log para debugging
            return self.error_response(f"Error del sistema: {str(e)}", 500)
    
    def _process_json_request(self) -> Dict[str, Any]:
        """Procesa una petición JSON"""
        try:
            json_data = request.get_json()
            if not json_data:
                raise ValidationError("El cuerpo de la petición JSON está vacío")
            
            # Validar campos requeridos
            required_fields = ['name', 'email', 'phone']
            for field in required_fields:
                if field not in json_data or not json_data[field]:
                    raise ValidationError(f"El campo '{field}' es obligatorio")
            
            return {
                'name': json_data['name'].strip(),
                'email': json_data['email'].strip(),
                'phone': json_data['phone'].strip(),
                'logo_file': None  # JSON no soporta archivos
            }
            
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Error al procesar JSON: {str(e)}")
    
    def _process_multipart_request(self) -> Dict[str, Any]:
        """Procesa una petición multipart/form-data"""
        try:
            # Obtener datos del formulario
            form_data = request.form.to_dict()
            
            # Validar campos requeridos
            required_fields = ['name', 'email', 'phone']
            for field in required_fields:
                if field not in form_data or not form_data[field]:
                    raise ValidationError(f"El campo '{field}' es obligatorio")
            
            # Obtener archivo de logo si existe
            logo_file = None
            if 'logo' in request.files:
                logo_file = request.files['logo']
                if logo_file.filename == '':
                    logo_file = None
            
            return {
                'name': form_data['name'].strip(),
                'email': form_data['email'].strip(),
                'phone': form_data['phone'].strip(),
                'logo_file': logo_file
            }
            
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Error al procesar formulario: {str(e)}")


class ProviderHealthController(BaseController):
    """Controlador para health check de proveedores"""
    
    def get(self) -> Tuple[Dict[str, Any], int]:
        """GET /providers/ping - Health check"""
        try:
            return self.success_response(
                data={
                    'service': 'providers',
                    'status': 'healthy',
                    'version': '1.0.0'
                },
                message="Servicio de proveedores funcionando correctamente"
            )
        except Exception as e:
            return self.handle_exception(e)


class ProviderDeleteAllController(BaseController):
    """Controlador para eliminar todos los proveedores"""
    
    def __init__(self):
        self.provider_service = ProviderService()
    
    def delete(self) -> Tuple[Dict[str, Any], int]:
        """DELETE /providers/all - Eliminar todos los proveedores"""
        try:
            # Eliminar todos los proveedores
            deleted_count = self.provider_service.delete_all()
            
            return self.success_response(
                data={
                    'deleted_count': deleted_count
                },
                message=f"Se eliminaron {deleted_count} proveedores exitosamente"
            )
            
        except BusinessLogicError as e:
            return self.error_response("Error temporal del sistema. Contacte soporte técnico si persiste", 500)
        except Exception as e:
            return self.error_response("Error temporal del sistema. Contacte soporte técnico si persiste", 500)