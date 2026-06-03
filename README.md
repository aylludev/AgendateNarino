# AgendateNarino

Sistema de agendamiento de eventos para el departamento de Nariño, Colombia.

## Requisitos

- Python 3.10+
- PostgreSQL 13+
- Django 4.2+

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Configurar variables de entorno:
   ```bash
   cp .env.example .env
   # Editar .env con los valores correctos
   ```
5. Crear la base de datos PostgreSQL:
   ```sql
   CREATE DATABASE agendatenarino;
   ```
6. Ejecutar migraciones:
   ```bash
   python manage.py migrate
   ```
7. Crear superusuario:
   ```bash
   python manage.py createsuperuser
   ```
8. Iniciar servidor:
   ```bash
   python manage.py runserver
   ```

## Estructura del Proyecto

- `agendate_narino/` — Configuración principal de Django
- `usuarios/` — Modelos de usuario y cliente (Gestor Cultural)
- `eventos/` — Modelos de categoría y evento
- `messaging/` — Sistema de mensajería entre usuarios
- `core/` — App principal vacía

## Modelos Principales

- **Usuario**: Usuario personalizado con campos extendidos (Cedula, Nombres, Apellidos, etc.)
- **Cliente**: Gestor Cultural asociado a un Usuario
- **Categoria**: Categorías para clasificar eventos
- **Evento**: Evento con fecha, ubicación, precio y estado
- **EventoFlyer**: Archivos multimedia asociados a eventos
- **Message**: Mensajes entre usuarios
- **Calification**: Calificaciones/ratings de eventos
