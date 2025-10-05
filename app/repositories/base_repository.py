"""
Repositorio base - Estructura para implementar operaciones CRUD
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any


class BaseRepository(ABC):
    """Repositorio base con operaciones CRUD comunes"""
    
    @abstractmethod
    def create(self, **kwargs) -> Any:
        """Crea una nueva entidad"""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[Any]:
        """Obtiene una entidad por ID"""
        pass
    
    @abstractmethod
    def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[Any]:
        """Obtiene todas las entidades"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Any]:
        """Obtiene una entidad por email"""
        pass