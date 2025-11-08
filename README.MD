# Biblioteca API

API REST desarrollada con FastAPI y PostgreSQL para la gestión de libros.  
Permite crear, listar, buscar, actualizar y eliminar libros en una base de datos relacional.

---

# Tecnologías utilizadas

- Python 3.10+
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL
- Pydantic v2
- Pytest

---

# Instalación y configuración

Clonar el repositoriO

git clone https://github.com/alejandrouribea/Biblioteca_API.git
cd Biblioteca_API


# Crear y activar entorno virtual

python -m venv venv
# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno

Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

DB_USER=postgres
DB_PASS=contraseña
DB_HOST=localhost
DB_PORT=5432
DB_NAME=biblioteca

# Ejecución del servidor

uvicorn app.main:app --reload

Documentación interactiva Swagger:
http://127.0.0.1:8000/docs

# Pruebas

Ejecutar pruebas unitarias e integración
pytest -v
