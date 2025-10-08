"""
Repositorio de Proveedores - Implementación con SQLAlchemy
"""
from typing import List, Optional
from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import uuid

from .base_repository import BaseRepository
from ..models.provider_model import Provider
from ..config.settings import Config

# Configuración de SQLAlchemy
Base = declarative_base()


class ProviderDB(Base):
    """Modelo de base de datos para proveedores"""
    __tablename__ = 'providers'
    
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)
    logo_filename = Column(String(255), nullable=True)
    logo_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProviderRepository(BaseRepository):
    """Repositorio para operaciones CRUD de proveedores"""
    
    def __init__(self):
        self.engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._create_tables()
    
    def _create_tables(self):
        """Crea las tablas si no existen"""
        try:
            Base.metadata.create_all(bind=self.engine)
        except SQLAlchemyError as e:
            print(f"Error creando tablas: {e}")
    
    def _get_session(self) -> Session:
        """Obtiene una sesión de base de datos"""
        return self.SessionLocal()
    
    def _db_to_model(self, db_provider: ProviderDB) -> Provider:
        """Convierte un modelo de DB a modelo de dominio"""
        return Provider(
            id=db_provider.id,
            name=db_provider.name,
            email=db_provider.email,
            phone=db_provider.phone,
            logo_filename=db_provider.logo_filename,
            logo_url=db_provider.logo_url,
            created_at=db_provider.created_at,
            updated_at=db_provider.updated_at
        )
    
    def _model_to_db(self, provider: Provider) -> ProviderDB:
        """Convierte un modelo de dominio a modelo de DB"""
        return ProviderDB(
            id=provider.id,
            name=provider.name,
            email=provider.email,
            phone=provider.phone,
            logo_filename=provider.logo_filename,
            logo_url=provider.logo_url,
            created_at=provider.created_at,
            updated_at=provider.updated_at
        )
    
    def create(self, **kwargs) -> Provider:
        """Crea un nuevo proveedor"""
        session = self._get_session()
        try:
            # Crear modelo de dominio
            provider = Provider(**kwargs)
            provider.validate()  # Validar antes de guardar
            
            # Verificar que el email no exista
            existing = session.query(ProviderDB).filter(ProviderDB.email == provider.email).first()
            if existing:
                raise ValueError("Ya existe un proveedor con este correo electrónico")
            
            # Convertir a modelo de DB y guardar
            db_provider = self._model_to_db(provider)
            session.add(db_provider)
            session.commit()
            session.refresh(db_provider)
            
            return self._db_to_model(db_provider)
            
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Error al crear proveedor: {str(e)}")
        finally:
            session.close()
    
    def get_by_id(self, provider_id: str) -> Optional[Provider]:
        """Obtiene un proveedor por ID"""
        session = self._get_session()
        try:
            db_provider = session.query(ProviderDB).filter(ProviderDB.id == provider_id).first()
            if db_provider:
                return self._db_to_model(db_provider)
            return None
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener proveedor: {str(e)}")
        finally:
            session.close()
    
    def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[Provider]:
        """Obtiene todos los proveedores ordenados por nombre"""
        session = self._get_session()
        try:
            query = session.query(ProviderDB).order_by(ProviderDB.name.asc()).offset(offset)
            if limit:
                query = query.limit(limit)
            
            db_providers = query.all()
            return [self._db_to_model(db_provider) for db_provider in db_providers]
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener proveedores: {str(e)}")
        finally:
            session.close()
    
    def count_all(self) -> int:
        """Cuenta el total de proveedores"""
        session = self._get_session()
        try:
            return session.query(ProviderDB).count()
        except SQLAlchemyError as e:
            raise Exception(f"Error al contar proveedores: {str(e)}")
        finally:
            session.close()
    
    
    def get_by_email(self, email: str) -> Optional[Provider]:
        """Obtiene un proveedor por email"""
        session = self._get_session()
        try:
            db_provider = session.query(ProviderDB).filter(ProviderDB.email == email).first()
            if db_provider:
                return self._db_to_model(db_provider)
            return None
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener proveedor por email: {str(e)}")
        finally:
            session.close()
    
    def delete_all(self) -> int:
        """Elimina todos los proveedores de la base de datos"""
        session = self._get_session()
        try:
            # Contar registros antes de eliminar
            count = session.query(ProviderDB).count()
            
            # Eliminar todos los registros
            session.query(ProviderDB).delete()
            session.commit()
            
            return count
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Error al eliminar todos los proveedores: {str(e)}")
        finally:
            session.close()