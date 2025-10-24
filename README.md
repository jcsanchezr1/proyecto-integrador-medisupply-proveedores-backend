# MediSupply Providers Backend

Sistema de gestión de proveedores para MediSupply - Backend API REST

## Descripción

Este servicio proporciona una API REST para la gestión de proveedores del sistema MediSupply. Incluye funcionalidades para crear, listar y eliminar proveedores con validaciones robustas y paginación eficiente.

## Características Principales

- API REST con Flask y Flask-RESTful
- Arquitectura en capas (Controller, Service, Repository, Model)
- Validaciones de datos robustas
- Paginación eficiente con ordenamiento
- Soporte para archivos de imagen (logos) con Google Cloud Storage
- URLs firmadas con expiración de 3 meses
- Manejo de excepciones personalizado
- Base de datos PostgreSQL con SQLAlchemy
- Contenedorización con Docker

## Estructura del Proyecto

```
proyecto-integrador-medisupply-proveedores-backend/
├── app/
│   ├── __init__.py                 # Configuración de Flask y rutas
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py             # Configuración de la aplicación
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── base_controller.py     # Controlador base con utilidades
│   │   ├── health_controller.py    # Health check
│   │   └── provider_controller.py # Endpoints de proveedores
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── custom_exceptions.py   # Excepciones personalizadas
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py          # Modelo base abstracto
│   │   └── provider_model.py      # Modelo de proveedor
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base_repository.py     # Repositorio base abstracto
│   │   └── provider_repository.py # Repositorio de proveedores
│   ├── services/
│   │   ├── __init__.py
│   │   ├── base_service.py        # Servicio base abstracto
│   │   └── provider_service.py    # Lógica de negocio de proveedores
│   └── utils/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_app_creation.py
│   ├── test_health_controller.py
│   └── test_health_endpoint.py
├── app.py                          # Punto de entrada de la aplicación
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── MediSupply-Providers.postman_collection.json
└── README.md
```

## Arquitectura

El proyecto sigue una arquitectura en capas bien definida:

- **Controllers**: Manejan las peticiones HTTP, validan entrada y formatean respuestas
- **Services**: Contienen la lógica de negocio y orquestan operaciones
- **Repositories**: Gestionan el acceso a datos y abstraen la fuente de datos
- **Models**: Definen las entidades del dominio con validaciones
- **Exceptions**: Manejo de excepciones personalizadas para diferentes tipos de errores
- **Utils**: Utilidades y helpers comunes

## Parámetros de API

### Resumen de Parámetros Disponibles

| Endpoint | Método | Parámetros de URL | Parámetros de Query | Body |
|----------|--------|-------------------|---------------------|------|
| `/providers/ping` | GET | - | - | - |
| `/providers` | GET | - | `page`, `per_page` | - |
| `/providers/{id}` | GET | `id` | - | - |
| `/providers` | POST | - | - | JSON o FormData |
| `/providers/all` | DELETE | - | - | - |

### Detalle de Parámetros de Query

| Parámetro | Tipo | Obligatorio | Default | Mínimo | Máximo | Descripción |
|-----------|------|-------------|---------|--------|--------|-------------|
| `page` | Integer | No | 1 | 1 | Sin límite | Número de página a consultar |
| `per_page` | Integer | No | 10 | 1 | 100 | Elementos por página |

### Combinaciones de Parámetros Válidas

| Combinación | Ejemplo | Resultado |
|-------------|---------|-----------|
| Sin parámetros | `GET /providers` | Página 1, 10 elementos |
| Solo página | `GET /providers?page=2` | Página 2, 10 elementos |
| Solo per_page | `GET /providers?per_page=25` | Página 1, 25 elementos |
| Ambos parámetros | `GET /providers?page=3&per_page=15` | Página 3, 15 elementos |

## Almacenamiento de Imágenes

### Google Cloud Storage
El servicio utiliza Google Cloud Storage para almacenar los logos de los proveedores:

- **Bucket**: `medisupply-images-bucket`
- **Carpeta**: `providers/`
- **Acceso**: Privado con URLs firmadas
- **Expiración**: 3 meses (2160 horas)

### Campos de Imagen
Cada proveedor puede tener asociado un logo con los siguientes campos:

- **`logo_filename`**: Nombre único del archivo (ej: `logo_uuid.png`)
- **`logo_url`**: URL firmada para acceder a la imagen (generada dinámicamente)

### Generación de URLs
- Las URLs se generan automáticamente al crear un proveedor
- Las URLs se regeneran en cada consulta para mantenerlas válidas
- Formato: `https://storage.googleapis.com/medisupply-images-bucket/providers/logo_uuid.png?Expires=...&GoogleAccessId=...&Signature=...`

### Configuración
Las credenciales se configuran mediante variables de entorno:
```bash
GCP_PROJECT_ID=soluciones-cloud-2024-02
BUCKET_NAME=medisupply-images-bucket
BUCKET_FOLDER=providers
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/gcp-credentials.json
```

## Endpoints Disponibles

### Health Check

**GET** `/providers/ping`

Verifica el estado del servicio.

**Respuesta:**
```json
{
  "message": "Servicio de proveedores funcionando correctamente",
  "data": {
    "service": "providers",
    "status": "healthy",
    "version": "1.0.0"
  }
}
```

### Listar Proveedores

**GET** `/providers`

Obtiene la lista de proveedores con paginación y ordenamiento por nombre.

**Parámetros de consulta:**
- `page` (opcional): Número de página 
  - **Valor por defecto**: 1
  - **Valor mínimo**: 1
  - **Valor máximo**: Sin límite (limitado por el total de páginas disponibles)
- `per_page` (opcional): Elementos por página
  - **Valor por defecto**: 10
  - **Valor mínimo**: 1
  - **Valor máximo**: 100
  - **Recomendado**: Entre 10-50 para mejor performance

**Ejemplos:**
```bash
# Página por defecto (página 1, 10 elementos)
GET /providers

# Página específica con 5 elementos
GET /providers?page=2&per_page=5

# Primera página con 3 elementos
GET /providers?page=1&per_page=3
```

**Respuesta:**
```json
{
  "message": "Lista de proveedores obtenida exitosamente",
  "data": {
    "providers": [
      {
        "id": "uuid-generado",
        "name": "Farmacia San José",
        "email": "ventas@farmacia.com",
        "phone": "3001234567",
        "logo_filename": "logo_uuid.png",
        "logo_url": "https://storage.googleapis.com/medisupply-images-bucket/providers/logo_uuid.png?Expires=..."
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 25,
      "total_pages": 3,
      "has_next": true,
      "has_prev": false,
      "next_page": 2,
      "prev_page": null
    }
  }
}
```

### Obtener Proveedor por ID

**GET** `/providers/{id}`

Obtiene un proveedor específico por su ID.

**Respuesta exitosa:**
```json
{
  "message": "Proveedor obtenido exitosamente",
  "data": {
    "id": "uuid-generado",
    "name": "Farmacia San José",
    "email": "ventas@farmacia.com",
    "phone": "3001234567",
    "logo_filename": "logo_uuid.png",
    "logo_url": "https://storage.googleapis.com/medisupply-images-bucket/providers/logo_uuid.png?Expires=...",
    "created_at": "2025-10-05T19:10:36.311869",
    "updated_at": "2025-10-05T19:10:36.311870"
  }
}
```

**Respuesta de error (404):**
```json
{
  "error": "Proveedor no encontrado"
}
```

### Crear Proveedor

**POST** `/providers`

Crea un nuevo proveedor. Soporta tanto JSON como multipart/form-data.

#### Crear Proveedor con JSON

**Content-Type:** `application/json`

**Cuerpo de la petición:**
```json
{
  "name": "Farmacia San José",
  "email": "ventas@farmacia.com",
  "phone": "3001234567"
}
```

#### Crear Proveedor con Archivo (Multipart)

**Content-Type:** `multipart/form-data`

**Campos del formulario:**
- `name`: Nombre del proveedor (obligatorio)
- `email`: Correo electrónico (obligatorio)
- `phone`: Teléfono (obligatorio)
- `logo`: Archivo de imagen (opcional)

**Respuesta exitosa:**
```json
{
  "message": "Proveedor registrado exitosamente",
  "data": {
    "id": "uuid-generado",
    "name": "Farmacia San José",
    "email": "ventas@farmacia.com",
    "phone": "3001234567",
    "logo_filename": "logo_uuid.png",
    "logo_url": "https://storage.googleapis.com/medisupply-images-bucket/providers/logo_uuid.png?Expires=...",
    "created_at": "2025-10-05T19:10:36.311869",
    "updated_at": "2025-10-05T19:10:36.311870"
  }
}
```

### Eliminar Todos los Proveedores

**DELETE** `/providers/all`

Elimina todos los proveedores de la base de datos.

**Respuesta:**
```json
{
  "message": "Se eliminaron 15 proveedores exitosamente",
  "data": {
    "deleted_count": 15
  }
}
```

## Paginación

### Cómo Funciona la Paginación

La paginación está implementada para manejar eficientemente grandes volúmenes de datos. Los proveedores se ordenan automáticamente por nombre (A-Z) y se dividen en páginas.

### Parámetros de Paginación

#### Parámetro `page`
- **Descripción**: Número de página a consultar
- **Tipo**: Entero
- **Obligatorio**: No
- **Valor por defecto**: 1
- **Valor mínimo**: 1
- **Valor máximo**: Sin límite (limitado por el total de páginas disponibles)
- **Ejemplo**: `?page=3`

#### Parámetro `per_page`
- **Descripción**: Cantidad de elementos por página
- **Tipo**: Entero
- **Obligatorio**: No
- **Valor por defecto**: 10
- **Valor mínimo**: 1
- **Valor máximo**: 100
- **Recomendado**: Entre 10-50 para mejor performance
- **Ejemplo**: `?per_page=25`

#### Límites de Elementos por Página

| Cantidad | Descripción | Uso Recomendado |
|----------|-------------|-----------------|
| 1-10 | Páginas pequeñas | Navegación móvil, listas compactas |
| 10-25 | Páginas estándar | Uso general, tablas de datos |
| 25-50 | Páginas grandes | Dashboards, reportes |
| 50-100 | Páginas muy grandes | Exportación de datos, análisis |
| >100 | **NO PERMITIDO** | Error 400 - Parámetro inválido |

### Límites y Recomendaciones

#### Límites Técnicos
- **Máximo por página**: 100 elementos
- **Mínimo por página**: 1 elemento
- **Página por defecto**: 1
- **Elementos por defecto**: 10

#### Recomendaciones de Performance
- **1-10 elementos**: Ideal para navegación móvil y listas compactas
- **10-25 elementos**: Uso general recomendado para la mayoría de casos
- **25-50 elementos**: Para dashboards y reportes con muchos datos
- **50-100 elementos**: Solo para exportación de datos o análisis

#### Consideraciones de Uso
- **Navegación web**: Usar 10-25 elementos por página
- **Aplicaciones móviles**: Usar 5-15 elementos por página
- **Exportación de datos**: Usar 50-100 elementos por página
- **Búsquedas en tiempo real**: Usar 10-20 elementos por página

### Información de Paginación

La respuesta incluye información completa de paginación:

```json
{
  "pagination": {
    "page": 2,           // Página actual
    "per_page": 5,       // Elementos por página
    "total": 25,          // Total de registros
    "total_pages": 5,     // Total de páginas
    "has_next": true,     // Hay página siguiente
    "has_prev": true,     // Hay página anterior
    "next_page": 3,       // Número de página siguiente
    "prev_page": 1        // Número de página anterior
  }
}
```

### Ejemplos de Paginación

#### Página por defecto (10 elementos)
```bash
curl "http://localhost:8082/providers"
# Retorna: página 1, 10 elementos, ordenados por nombre
```

#### Paginación pequeña (5 elementos)
```bash
curl "http://localhost:8082/providers?page=1&per_page=5"
# Retorna: página 1, 5 elementos, ordenados por nombre
```

#### Paginación estándar (25 elementos)
```bash
curl "http://localhost:8082/providers?page=2&per_page=25"
# Retorna: página 2, 25 elementos, ordenados por nombre
```

#### Paginación grande (50 elementos)
```bash
curl "http://localhost:8082/providers?page=1&per_page=50"
# Retorna: página 1, 50 elementos, ordenados por nombre
```

#### Paginación máxima (100 elementos)
```bash
curl "http://localhost:8082/providers?page=1&per_page=100"
# Retorna: página 1, 100 elementos, ordenados por nombre
```

#### Validaciones de Parámetros

**Página inválida (menor a 1):**
```bash
curl "http://localhost:8082/providers?page=0"
# Error: "El parámetro 'page' debe ser mayor a 0"
```

**Per_page inválido (mayor a 100):**
```bash
curl "http://localhost:8082/providers?per_page=150"
# Error: "El parámetro 'per_page' debe estar entre 1 y 100"
```

**Per_page inválido (menor a 1):**
```bash
curl "http://localhost:8082/providers?per_page=0"
# Error: "El parámetro 'per_page' debe estar entre 1 y 100"
```

**Página fuera de rango:**
```bash
curl "http://localhost:8082/providers?page=999&per_page=10"
# Retorna: página vacía con información de paginación correcta
```

## Validaciones

### Campos Obligatorios

- **name**: Nombre del proveedor (obligatorio)
- **email**: Correo electrónico (obligatorio)
- **phone**: Teléfono (obligatorio)
- **logo**: Archivo de imagen (opcional)

### Validaciones de Nombre

- No puede estar vacío
- Solo acepta caracteres alfabéticos, numéricos y espacios
- Soporta caracteres especiales en español (á, é, í, ó, ú, ñ, ü)

**Regex:** `^[a-zA-Z0-9\sáéíóúÁÉÍÓÚñÑüÜ]+$`

### Validaciones de Email

- No puede estar vacío
- Debe contener '@'
- Debe tener un dominio válido (al menos un punto)
- La extensión debe tener al menos 2 caracteres
- Formato válido de email

**Regex:** `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

### Validaciones de Teléfono

- No puede estar vacío
- Solo debe contener números
- Mínimo 7 dígitos
- Máximo 20 caracteres

**Regex:** `^\d+$`

### Validaciones de Archivo de Logo

- **Tipos permitidos**: JPG, JPEG, PNG, GIF
- **Tamaño mínimo**: 1KB
- **Tamaño máximo**: 2MB
- **Archivo vacío**: Rechazado

### Validaciones de Unicidad

- **Email**: Debe ser único en el sistema

### Mensajes de Error Específicos

#### Validaciones de Campos
```json
{
  "error": "El campo 'Nombre' es obligatorio"
}
```

```json
{
  "error": "El campo 'Correo electrónico' debe tener un formato válido"
}
```

```json
{
  "error": "El campo 'Teléfono' debe contener solo números y tener al menos 7 dígitos"
}
```

#### Validaciones de Archivos
```json
{
  "error": "El archivo debe ser una imagen válida (JPG, PNG, GIF)"
}
```

```json
{
  "error": "El archivo no puede exceder 2MB"
}
```

```json
{
  "error": "El archivo está vacío"
}
```

#### Validaciones de Unicidad
```json
{
  "error": "Ya existe un proveedor con este correo electrónico"
}
```

#### Validaciones de Paginación
```json
{
  "error": "El parámetro 'page' debe ser mayor a 0"
}
```

```json
{
  "error": "El parámetro 'per_page' debe estar entre 1 y 100"
}
```

## Casos de Uso

### Caso 1: Listar Proveedores con Paginación

**Escenario:** Un usuario necesita ver todos los proveedores paginados.

**Pasos:**
1. Realizar petición GET a `/providers`
2. El sistema retorna los primeros 10 proveedores ordenados por nombre
3. Si hay más páginas, usar `next_page` para navegar

**Ejemplo:**
```bash
# Primera página
curl "http://localhost:8082/providers"

# Segunda página
curl "http://localhost:8082/providers?page=2"
```

### Caso 2: Crear Proveedor con Datos Básicos

**Escenario:** Un usuario quiere registrar un nuevo proveedor sin logo.

**Pasos:**
1. Preparar datos JSON con nombre, email y teléfono
2. Enviar petición POST con Content-Type: application/json
3. El sistema valida los datos y crea el proveedor

**Ejemplo:**
```bash
curl -X POST "http://localhost:8082/providers" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Farmacia San José",
    "email": "ventas@farmacia.com",
    "phone": "3001234567"
  }'
```

### Caso 3: Crear Proveedor con Logo

**Escenario:** Un usuario quiere registrar un proveedor con su logo.

**Pasos:**
1. Preparar formulario multipart con datos y archivo
2. Enviar petición POST con Content-Type: multipart/form-data
3. El sistema valida datos y archivo, genera nombre único para el logo

**Ejemplo:**
```bash
curl -X POST "http://localhost:8082/providers" \
  -F "name=Farmacia San José" \
  -F "email=ventas@farmacia.com" \
  -F "phone=3001234567" \
  -F "logo=@logo.jpg"
```

### Caso 4: Validación de Errores

**Escenario:** Un usuario envía datos inválidos.

**Casos de error:**
- Nombre vacío o con caracteres especiales
- Email sin formato válido
- Teléfono con letras o muy corto
- Archivo de tipo no permitido
- Email duplicado

**Ejemplo de error:**
```bash
curl -X POST "http://localhost:8082/providers" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "",
    "email": "email-invalido",
    "phone": "123"
  }'
```

**Respuesta:**
```json
{
  "error": "El campo 'Nombre' es obligatorio; El campo 'Correo electrónico' debe tener un formato válido; El campo 'Teléfono' debe tener al menos 7 dígitos"
}
```

### Caso 5: Búsqueda de Proveedor Específico

**Escenario:** Un usuario necesita obtener información de un proveedor específico.

**Pasos:**
1. Obtener el ID del proveedor
2. Realizar petición GET a `/providers/{id}`
3. El sistema retorna los datos completos del proveedor

**Ejemplo:**
```bash
curl "http://localhost:8082/providers/uuid-del-proveedor"
```

### Caso 6: Limpieza de Datos

**Escenario:** Un administrador necesita eliminar todos los proveedores.

**Pasos:**
1. Realizar petición DELETE a `/providers/all`
2. El sistema elimina todos los registros
3. Retorna el número de registros eliminados

**Ejemplo:**
```bash
curl -X DELETE "http://localhost:8082/providers/all"
```

### Caso 7: Navegación Móvil (Páginas Pequeñas)

**Escenario:** Una aplicación móvil necesita mostrar proveedores en una lista compacta.

**Configuración recomendada:**
- `per_page=5` para pantallas pequeñas
- `per_page=10` para pantallas medianas

**Ejemplo:**
```bash
# Lista compacta para móvil
curl "http://localhost:8082/providers?per_page=5"

# Lista estándar para tablet
curl "http://localhost:8082/providers?per_page=10"
```

### Caso 8: Dashboard Empresarial (Páginas Grandes)

**Escenario:** Un dashboard empresarial necesita mostrar muchos proveedores para análisis.

**Configuración recomendada:**
- `per_page=25` para vista general
- `per_page=50` para análisis detallado

**Ejemplo:**
```bash
# Vista general del dashboard
curl "http://localhost:8082/providers?per_page=25"

# Análisis detallado
curl "http://localhost:8082/providers?per_page=50"
```

### Caso 9: Exportación de Datos (Páginas Máximas)

**Escenario:** Un usuario necesita exportar todos los proveedores para análisis externo.

**Configuración recomendada:**
- `per_page=100` para máxima eficiencia
- Iterar por todas las páginas disponibles

**Ejemplo:**
```bash
# Primera página de exportación
curl "http://localhost:8082/providers?page=1&per_page=100"

# Segunda página de exportación
curl "http://localhost:8082/providers?page=2&per_page=100"
```

### Caso 10: Búsqueda en Tiempo Real

**Escenario:** Un sistema de búsqueda necesita mostrar resultados rápidamente.

**Configuración recomendada:**
- `per_page=15` para balance entre velocidad y cantidad
- Navegación rápida entre páginas

**Ejemplo:**
```bash
# Resultados de búsqueda rápida
curl "http://localhost:8082/providers?per_page=15"
```

## Instalación y Configuración

### Requisitos

- Python 3.9+
- Docker y Docker Compose
- PostgreSQL (si se ejecuta localmente)

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

4. Configurar variables de entorno:
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
   export DEBUG=true
   ```

5. Ejecutar la aplicación:
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

### Variables de Entorno

- `HOST`: Host del servidor (default: 0.0.0.0)
- `PORT`: Puerto del servidor (default: 8080)
- `DEBUG`: Modo debug (default: True)
- `DATABASE_URL`: URL de conexión a PostgreSQL
- `SECRET_KEY`: Clave secreta de Flask (default: dev-secret-key)

## Testing

### Ejecutar Tests

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con información detallada
pytest -v

# Ejecutar pruebas específicas
pytest tests/test_provider_model.py
```

### Ejecutar con Coverage

```bash
# Ejecutar pruebas con coverage
pytest --cov=app --cov-report=term-missing

# Generar reporte HTML de coverage
pytest --cov=app --cov-report=html

# Verificar 100% de coverage
pytest --cov=app --cov-fail-under=100
```


### Colección de Postman

El proyecto incluye una colección de Postman completa con casos de prueba:

- Casos exitosos con datos aleatorios
- Validaciones de campos obligatorios
- Validaciones de formato de datos
- Validaciones de archivos
- Casos de paginación
- Casos de error

**Archivo:** `MediSupply-Providers.postman_collection.json`

## Desarrollo

### Agregar Nuevas Funcionalidades

1. Crear el modelo en `app/models/`
2. Crear el repositorio en `app/repositories/`
3. Crear el servicio en `app/services/`
4. Crear el controlador en `app/controllers/`
5. Registrar la ruta en `app/__init__.py`
6. Agregar tests correspondientes

### Estructura de Respuestas

#### Respuesta Exitosa
```json
{
  "message": "Mensaje descriptivo",
  "data": { ... }
}
```

#### Respuesta de Error
```json
{
  "error": "Descripción del error"
}
```

### Códigos de Estado HTTP

- **200**: Operación exitosa
- **201**: Recurso creado exitosamente
- **400**: Error de validación o parámetros inválidos
- **404**: Recurso no encontrado
- **500**: Error interno del servidor

## Docker

### Construir Imagen

```bash
docker build -t proveedores .
```

### Ejecutar Contenedor

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

# Reconstruir
docker-compose up --build
```

## Base de Datos

### Modelo de Datos

**Tabla: providers**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | VARCHAR(36) | Identificador único (UUID) |
| name | VARCHAR(255) | Nombre del proveedor |
| email | VARCHAR(255) | Correo electrónico (único) |
| phone | VARCHAR(20) | Número de teléfono |
| logo_filename | VARCHAR(255) | Nombre del archivo de logo |
| created_at | TIMESTAMP | Fecha de creación |
| updated_at | TIMESTAMP | Fecha de última actualización |


## Seguridad

### Validaciones de Entrada

- Sanitización de datos de entrada
- Validación de tipos de archivo
- Límites de tamaño de archivo
- Validación de parámetros de paginación.