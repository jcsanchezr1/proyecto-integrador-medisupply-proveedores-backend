import pytest
from unittest.mock import patch, MagicMock, call
from app.repositories.provider_repository import ProviderRepository, ProviderDB
from app.models.provider_model import Provider
from app.exceptions.custom_exceptions import ValidationError, BusinessLogicError
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import uuid


class TestProviderRepository:
    """Pruebas unitarias para ProviderRepository"""
    
    @pytest.fixture
    def mock_session(self):
        """Fixture para mock de sesión SQLAlchemy"""
        return MagicMock()
    
    @pytest.fixture
    def provider_repository(self, mock_session):
        """Fixture para ProviderRepository con sesión mockeada"""
        with patch('app.repositories.provider_repository.Session') as mock_session_class:
            mock_session_class.return_value = mock_session
            with patch('app.repositories.provider_repository.create_engine'):
                with patch('app.repositories.provider_repository.sessionmaker'):
                    with patch('app.repositories.provider_repository.Base.metadata.create_all'):
                        return ProviderRepository()
    
    @pytest.fixture
    def provider_data(self):
        """Fixture con datos de proveedor"""
        return {
            'id': str(uuid.uuid4()),
            'name': 'Farmacia Test',
            'email': 'test@farmacia.com',
            'phone': '3001234567',
            'logo_filename': 'logo.jpg',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
    
    @pytest.fixture
    def provider(self, provider_data):
        """Fixture para Provider"""
        return Provider(**provider_data)
    
    def test_provider_repository_initialization(self, provider_repository):
        """Prueba la inicialización de ProviderRepository"""
        assert provider_repository is not None
        assert isinstance(provider_repository, ProviderRepository)
    
    def test_provider_repository_inheritance(self, provider_repository):
        """Prueba que ProviderRepository hereda de BaseRepository"""
        from app.repositories.base_repository import BaseRepository
        
        assert isinstance(provider_repository, BaseRepository)
    
    def test_provider_db_table_name(self):
        """Prueba que la tabla tiene el nombre correcto"""
        assert ProviderDB.__tablename__ == 'providers'
    
    def test_provider_db_attributes(self):
        """Prueba que ProviderDB tiene todos los atributos esperados"""
        provider_db = ProviderDB()
        
        # Verificar que tiene todos los atributos
        assert hasattr(provider_db, 'id')
        assert hasattr(provider_db, 'name')
        assert hasattr(provider_db, 'email')
        assert hasattr(provider_db, 'phone')
        assert hasattr(provider_db, 'logo_filename')
        assert hasattr(provider_db, 'created_at')
        assert hasattr(provider_db, 'updated_at')
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_create_success(self, mock_get_session, provider_repository, provider_data):
        """Prueba creación exitosa de proveedor"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock del query para verificar email único (retorna None = no existe)
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_session.query.return_value = mock_query
        
        # Mock del add y commit
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None
        
        # Mock de los métodos de conversión
        with patch.object(provider_repository, '_model_to_db') as mock_model_to_db:
            with patch.object(provider_repository, '_db_to_model') as mock_db_to_model:
                mock_db_provider = MagicMock()
                mock_model_to_db.return_value = mock_db_provider
                
                expected_provider = Provider(**provider_data)
                mock_db_to_model.return_value = expected_provider
                
                result = provider_repository.create(**provider_data)
                
                # Verificar que se llamó add, commit y refresh
                mock_session.add.assert_called_once_with(mock_db_provider)
                mock_session.commit.assert_called_once()
                mock_session.refresh.assert_called_once_with(mock_db_provider)
                mock_session.close.assert_called_once()
                
                # Verificar que se retornó el proveedor
                assert result == expected_provider
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_create_email_already_exists(self, mock_get_session, provider_repository, provider_data):
        """Prueba creación con email duplicado"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock del query para simular email existente
        mock_query = MagicMock()
        mock_existing_provider = MagicMock()
        mock_existing_provider.email = provider_data['email']
        mock_query.filter.return_value.first.return_value = mock_existing_provider
        mock_session.query.return_value = mock_query
        
        with pytest.raises(ValueError) as exc_info:
            provider_repository.create(**provider_data)
        
        assert "Ya existe un proveedor con este correo electrónico" in str(exc_info.value)
        mock_session.close.assert_called_once()
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_create_database_error(self, mock_get_session, provider_repository, provider_data):
        """Prueba creación con error de base de datos"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock del query para verificar email único
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_session.query.return_value = mock_query
        
        # Mock del add para lanzar excepción
        mock_session.add.side_effect = SQLAlchemyError("Database error")
        
        with pytest.raises(Exception) as exc_info:
            provider_repository.create(**provider_data)
        
        assert "Error al crear proveedor" in str(exc_info.value)
        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_get_by_id_success(self, mock_get_session, provider_repository, provider_data):
        """Prueba obtención exitosa por ID"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock del query
        mock_query = MagicMock()
        mock_db_provider = MagicMock()
        mock_db_provider.id = provider_data['id']
        mock_db_provider.name = provider_data['name']
        mock_db_provider.email = provider_data['email']
        mock_db_provider.phone = provider_data['phone']
        mock_db_provider.logo_filename = provider_data['logo_filename']
        mock_db_provider.created_at = provider_data['created_at']
        mock_db_provider.updated_at = provider_data['updated_at']
        
        mock_query.filter.return_value.first.return_value = mock_db_provider
        mock_session.query.return_value = mock_query
        
        # Mock del método de conversión
        with patch.object(provider_repository, '_db_to_model') as mock_db_to_model:
            expected_provider = Provider(**provider_data)
            mock_db_to_model.return_value = expected_provider
            
            result = provider_repository.get_by_id(provider_data['id'])
            
            # Verificar que se llamó query con el ID correcto
            mock_session.query.assert_called_once()
            mock_query.filter.assert_called_once()
            mock_session.close.assert_called_once()
            
            # Verificar que se retornó un Provider
            assert result == expected_provider
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_get_by_id_not_found(self, mock_get_session, provider_repository):
        """Prueba obtención por ID cuando no existe"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock del query para retornar None
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_session.query.return_value = mock_query
        
        result = provider_repository.get_by_id("non-existent-id")
        
        assert result is None
        mock_session.close.assert_called_once()
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_get_by_id_database_error(self, mock_get_session, provider_repository):
        """Prueba obtención por ID con error de base de datos"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock del query para lanzar excepción
        mock_session.query.side_effect = SQLAlchemyError("Database error")
        
        with pytest.raises(Exception) as exc_info:
            provider_repository.get_by_id("some-id")
        
        assert "Error al obtener proveedor" in str(exc_info.value)
        mock_session.close.assert_called_once()
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_get_by_email_success(self, mock_get_session, provider_repository, provider_data):
        """Prueba obtención exitosa por email"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock del query
        mock_query = MagicMock()
        mock_db_provider = MagicMock()
        mock_db_provider.id = provider_data['id']
        mock_db_provider.name = provider_data['name']
        mock_db_provider.email = provider_data['email']
        mock_db_provider.phone = provider_data['phone']
        mock_db_provider.logo_filename = provider_data['logo_filename']
        mock_db_provider.created_at = provider_data['created_at']
        mock_db_provider.updated_at = provider_data['updated_at']
        
        mock_query.filter.return_value.first.return_value = mock_db_provider
        mock_session.query.return_value = mock_query
        
        # Mock del método de conversión
        with patch.object(provider_repository, '_db_to_model') as mock_db_to_model:
            expected_provider = Provider(**provider_data)
            mock_db_to_model.return_value = expected_provider
            
            result = provider_repository.get_by_email(provider_data['email'])
            
            # Verificar que se llamó query con el email correcto
            mock_session.query.assert_called_once()
            mock_query.filter.assert_called_once()
            mock_session.close.assert_called_once()
            
            # Verificar que se retornó un Provider
            assert result == expected_provider
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_get_by_email_not_found(self, mock_get_session, provider_repository):
        """Prueba obtención por email cuando no existe"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock del query para retornar None
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_session.query.return_value = mock_query
        
        result = provider_repository.get_by_email("non-existent@email.com")
        
        assert result is None
        mock_session.close.assert_called_once()
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_get_by_email_database_error(self, mock_get_session, provider_repository):
        """Prueba obtención por email con error de base de datos"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock del query para lanzar excepción
        mock_session.query.side_effect = SQLAlchemyError("Database error")
        
        with pytest.raises(Exception) as exc_info:
            provider_repository.get_by_email("test@email.com")
        
        assert "Error al obtener proveedor" in str(exc_info.value)
        mock_session.close.assert_called_once()
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_get_all_success(self, mock_get_session, provider_repository):
        """Prueba obtención exitosa de todos los proveedores"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock de proveedores de base de datos
        mock_db_providers = [
            MagicMock(id="1", name="Provider 1", email="p1@test.com", phone="3001111111", 
                     logo_filename="logo1.jpg", created_at=datetime.now(), updated_at=datetime.now()),
            MagicMock(id="2", name="Provider 2", email="p2@test.com", phone="3002222222", 
                     logo_filename="logo2.jpg", created_at=datetime.now(), updated_at=datetime.now())
        ]
        
        # Mock del query
        mock_query = MagicMock()
        mock_ordered_query = MagicMock()
        mock_offset_query = MagicMock()
        mock_limit_query = MagicMock()
        
        mock_query.order_by.return_value = mock_ordered_query
        mock_ordered_query.offset.return_value = mock_offset_query
        mock_offset_query.limit.return_value = mock_limit_query
        mock_limit_query.all.return_value = mock_db_providers
        mock_session.query.return_value = mock_query
        
        # Mock del método de conversión
        with patch.object(provider_repository, '_db_to_model') as mock_db_to_model:
            expected_providers = [Provider(name="Provider 1", email="p1@test.com", phone="3001111111"),
                                Provider(name="Provider 2", email="p2@test.com", phone="3002222222")]
            mock_db_to_model.side_effect = expected_providers
            
            result = provider_repository.get_all(limit=10, offset=0)
            
            # Verificar que se llamó query con los parámetros correctos
            mock_session.query.assert_called_once()
            mock_query.order_by.assert_called_once()
            mock_ordered_query.offset.assert_called_once_with(0)
            mock_offset_query.limit.assert_called_once_with(10)
            mock_session.close.assert_called_once()
            
            # Verificar que se retornó una lista de Providers
            assert isinstance(result, list)
            assert len(result) == 2
            assert all(isinstance(p, Provider) for p in result)
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_get_all_without_limit(self, mock_get_session, provider_repository):
        """Prueba obtención de todos los proveedores sin límite"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock de proveedores de base de datos
        mock_db_providers = [MagicMock(id="1", name="Provider 1", email="p1@test.com", 
                                     phone="3001111111", logo_filename="logo1.jpg", 
                                     created_at=datetime.now(), updated_at=datetime.now())]
        
        # Mock del query
        mock_query = MagicMock()
        mock_query.order_by.return_value.offset.return_value.all.return_value = mock_db_providers
        mock_session.query.return_value = mock_query
        
        # Mock del método de conversión
        with patch.object(provider_repository, '_db_to_model') as mock_db_to_model:
            expected_provider = Provider(name="Provider 1", email="p1@test.com", phone="3001111111")
            mock_db_to_model.return_value = expected_provider
            
            result = provider_repository.get_all(offset=0)
            
            # Verificar que no se llamó limit
            mock_query.limit.assert_not_called()
            mock_session.close.assert_called_once()
            
            # Verificar que se retornó una lista de Providers
            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], Provider)
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_get_all_database_error(self, mock_get_session, provider_repository):
        """Prueba obtención de todos los proveedores con error de base de datos"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock del query para lanzar excepción
        mock_session.query.side_effect = SQLAlchemyError("Database error")
        
        with pytest.raises(Exception) as exc_info:
            provider_repository.get_all()
        
        assert "Error al obtener proveedores" in str(exc_info.value)
        mock_session.close.assert_called_once()
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_delete_all_success(self, mock_get_session, provider_repository):
        """Prueba eliminación exitosa de todos los proveedores"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock del query
        mock_query = MagicMock()
        mock_query.count.return_value = 5  # Simular que hay 5 proveedores antes de eliminar
        mock_query.delete.return_value = 5  # Simular que se eliminaron 5 proveedores
        mock_session.query.return_value = mock_query
        mock_session.commit.return_value = None
        
        result = provider_repository.delete_all()
        
        # Verificar que se llamó count, delete y commit
        # El método delete_all llama a query dos veces: una para count y otra para delete
        assert mock_session.query.call_count == 2
        mock_query.count.assert_called_once()
        mock_query.delete.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()
        
        # Verificar que se retornó el número de registros que había antes de eliminar
        assert result == 5
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_delete_all_database_error(self, mock_get_session, provider_repository):
        """Prueba eliminación de todos los proveedores con error de base de datos"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock del query para lanzar excepción
        mock_session.query.side_effect = SQLAlchemyError("Database error")
        
        with pytest.raises(Exception) as exc_info:
            provider_repository.delete_all()
        
        assert "Error al eliminar todos los proveedores" in str(exc_info.value)
        mock_session.close.assert_called_once()
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_count_all_success(self, mock_get_session, provider_repository):
        """Prueba conteo exitoso de todos los proveedores"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock del query
        mock_query = MagicMock()
        mock_query.count.return_value = 10
        mock_session.query.return_value = mock_query
        
        result = provider_repository.count_all()
        
        # Verificar que se llamó query y count
        mock_session.query.assert_called_once()
        mock_query.count.assert_called_once()
        mock_session.close.assert_called_once()
        
        # Verificar que se retornó el conteo correcto
        assert result == 10
    
    @patch('app.repositories.provider_repository.ProviderRepository._get_session')
    def test_count_all_database_error(self, mock_get_session, provider_repository):
        """Prueba conteo de todos los proveedores con error de base de datos"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        # Mock del query para lanzar excepción
        mock_session.query.side_effect = SQLAlchemyError("Database error")
        
        with pytest.raises(Exception) as exc_info:
            provider_repository.count_all()
        
        assert "Error al contar proveedores" in str(exc_info.value)
        mock_session.close.assert_called_once()
    
    def test_db_to_model_conversion(self, provider_repository, provider_data):
        """Prueba la conversión de ProviderDB a Provider"""
        # Mock de ProviderDB
        mock_db_provider = MagicMock()
        mock_db_provider.id = provider_data['id']
        mock_db_provider.name = provider_data['name']
        mock_db_provider.email = provider_data['email']
        mock_db_provider.phone = provider_data['phone']
        mock_db_provider.logo_filename = provider_data['logo_filename']
        mock_db_provider.created_at = provider_data['created_at']
        mock_db_provider.updated_at = provider_data['updated_at']
        
        # Llamar al método privado _db_to_model
        result = provider_repository._db_to_model(mock_db_provider)
        
        # Verificar que se retornó un Provider con los datos correctos
        assert isinstance(result, Provider)
        assert result.id == mock_db_provider.id
        assert result.name == mock_db_provider.name
        assert result.email == mock_db_provider.email
        assert result.phone == mock_db_provider.phone
        assert result.logo_filename == mock_db_provider.logo_filename
        assert result.created_at == mock_db_provider.created_at
        assert result.updated_at == mock_db_provider.updated_at