# MediSupply Providers Backend

Sistema de gestión de proveedores para MediSupply - Backend API

## Estructura del Proyecto

```
proyecto-integrador-medisupply-proveedores-backend/
├── app/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── base_controller.py
│   │   ├── health_controller.py
│   │   └── provider_controller.py
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── custom_exceptions.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   └── provider_model.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base_repository.py
│   │   └── provider_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── base_service.py
│   │   └── provider_service.py
│   └── utils/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_app_creation.py
│   ├── test_health_controller.py
│   └── test_health_endpoint.py
├── app.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Arquitectura

El proyecto sigue una arquitectura en capas:

- **Controllers**: Manejan las peticiones HTTP y respuestas
- **Services**: Contienen la lógica de negocio
- **Repositories**: Gestionan el acceso a datos
- **Models**: Definen las entidades del dominio
- **Exceptions**: Manejo de excepciones personalizadas
- **Utils**: Utilidades y helpers

## Instalación y Configuración

### Requisitos

- Python 3.9+
- Docker y Docker Compose

### Instalación Local

1. Clonar el repositorio
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecutar la aplicación:
   ```bash
   python app.py
   ```

### Instalación con Docker

1. Construir y ejecutar con Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. O construir y ejecutar manualmente:
   ```bash
   docker build -t proveedores .
   docker run -p 8080:8080 proveedores
   ```

## Uso

### Health Check

El servicio incluye un endpoint de health check:

```bash
curl http://localhost:8080/providers/ping
```

Respuesta esperada:
```
pong
```

## Testing

Ejecutar los tests:

```bash
python -m unittest discover -s tests
```

Ejecutar con coverage:

```bash
coverage run -m unittest discover -s tests
coverage report -m
```

## Desarrollo

### Estructura de Capas

- **Controllers**: Reciben peticiones HTTP, validan entrada, llaman a servicios
- **Services**: Implementan lógica de negocio, orquestan operaciones
- **Repositories**: Acceso a datos, abstracción de la fuente de datos
- **Models**: Entidades del dominio, validaciones de datos

### Agregar Nuevas Funcionalidades

1. Crear el modelo en `app/models/`
2. Crear el repositorio en `app/repositories/`
3. Crear el servicio en `app/services/`
4. Crear el controlador en `app/controllers/`
5. Registrar la ruta en `app/__init__.py`
6. Agregar tests correspondientes

## Variables de Entorno

- `HOST`: Host del servidor (default: 0.0.0.0)
- `PORT`: Puerto del servidor (default: 8080)
- `DEBUG`: Modo debug (default: True)
- `SECRET_KEY`: Clave secreta de Flask (default: dev-secret-key)

## Docker

### Construir imagen

```bash
docker build -t proveedores .
```

### Ejecutar contenedor

```bash
docker run -p 8080:8080 proveedores
```

### Docker Compose

```bash
# Ejecutar
docker-compose up

# Ejecutar en background
docker-compose up -d

# Detener
docker-compose down
```