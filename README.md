# AgendateNarino

Sistema de agendamiento de eventos culturales y artísticos para el
departamento de Nariño, Colombia. Los gestores culturales crean y publican
eventos; los moderadores los revisan; el público los descubre en una
landing con carrusel y mapa.

## Stack

- **Backend**: Django 4.2+, Python 3.10+
- **ASGI / WebSocket**: Daphne + Django Channels
- **Base de datos**: PostgreSQL 13+
- **Frontend**: Bootstrap 5.3 (CDN) + AdminLTE 4 (CDN) en el dashboard
  autenticado
- **Mapa**: Leaflet + OpenStreetMap
- **Auth**: `Usuario` custom (extiende `AbstractUser`), `AUTH_USER_MODEL =
  'usuarios.Usuario'`
- **Estáticos en dev**: WhiteNoise (sirve `/static/` cuando el server es
  Daphne o runserver, evita el 404 que Daphne da por defecto)

## Requisitos

- Python 3.10+
- PostgreSQL 13+
- Las dependencias de `requirements.txt` (Django, Channels, Daphne,
  whitenoise, psycopg2, Pillow, python-decouple, django-ratelimit)

## Instalación

1. Clonar el repositorio
2. Crear y activar entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate     # Linux/Mac
   venv\Scripts\activate        # Windows
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

## Ejecución

> **Importante**: usar **Daphne** (no `runserver`) porque el chat usa
> WebSocket y `runserver` no lo soporta. `runserver` solo serviria HTTP
> y romperia silenciosamente el WebSocket del chat.

```bash
source venv/bin/activate
daphne -b 127.0.0.1 -p 8000 agendate_narino.asgi:application
```

Entrar a **http://localhost:8000/**.

### Windows (cmd)

```cmd
venv\Scripts\activate
daphne -b 127.0.0.1 -p 8000 agendate_narino.asgi:application
```

Si querés liberar la terminal y dejarlo en background:

```cmd
start /b "" daphne -b 127.0.0.1 -p 8000 agendate_narino.asgi:application > daphne.log 2>&1
```

### Windows (PowerShell)

```powershell
venv\Scripts\Activate.ps1
daphne -b 127.0.0.1 -p 8000 agendate_narino.asgi:application
```

## Estructura del Proyecto

```
agendate_narino/   Configuración Django + ASGI (Channels routing)
usuarios/           Modelo Usuario (Cedula, Nombres, Apellidos) y auth
eventos/            Categoria, Evento, EventoFlyer (modelos + CRUD + explorar)
messaging/          Chat 1:1 con WebSocket (consumers.py + routing.py)
core/               Dashboards (admin/mod y gestor cultural)
templates/          Layouts base + includes (navbar marketing, auth, theme)
static/             Assets locales (CSS, imágenes, íconos)
```

## Modelos Principales

- **Usuario** (`usuarios.Usuario`): extiende `AbstractUser` con `Cedula`
  (única), `Nombres`, `Apellidos`, `telefono`, `direccion`, `is_moderador`
- **Categoria** (`eventos.Categoria`): clasificación de eventos
- **Evento** (`eventos.Evento`): `titulo`, `descripcion`, `categoria`,
  `gestor`, `municipio`, `direccion`, `geolocalizacion` (formato
  `lat,lng`), `fecha`, `horario`, `precio`, `estado`, `link_formulario`,
  `activo`
- **EventoFlyer** (`eventos.EventoFlyer`): imágenes/videos asociados al
  evento (related_name `flyers`)
- **Message** (`messaging.Message`): `remitente`, `destinatario`,
  `descripcion`, `room_identifier` (formato `chat_<idMenor>_<idMayor>`),
  `leido`
- **Calification** (`messaging.Calification`): puntuación 1-5 de gestores
  sobre eventos (unique por gestor+evento)

## Roles

- **Visitante** (no autenticado): landing, explorar eventos, login, registro
- **Gestor Cultural**: su dashboard, crear/editar SUS eventos, explorar,
  mensajería
- **Moderador** (grupo `Moderador` + flag `is_moderador`): ver/editar TODOS
  los eventos, dashboard con métricas
- **Superuser/Staff**: además de lo anterior, Django admin

## Páginas Principales

| URL | Vista | Descripción |
|---|---|---|
| `/` | `eventos.views.home` | Landing (templates/home/index.html) |
| `/events/explore/` | `eventos.views.evento_explore` | Carrusel + mapa Leaflet de eventos activos |
| `/events/events/` | `eventos.EventoListView` | CRUD/listado (autenticado) |
| `/events/events/<id>/` | `eventos.EventoDetailView` | Detalle de un evento |
| `/messaging/chat/<id>/` | `messaging.views.chat_room` | Chat 1:1 con WebSocket |
| `/messaging/inbox/` | `messaging.views.inbox` | Lista de conversaciones |
| `/core/dashboard/` | `core.views.dashboard` | Dashboard admin/moderador |
| `/core/cliente/` | `core.views.client_dashboard` | Dashboard gestor |
| `/usuarios/login/` | `usuarios.LoginView` | Login |
| `/usuarios/registro/` | `usuarios.registro` | Registro (auto-asigna grupo Gestor) |
| `/usuarios/perfil/` | `usuarios.perfil` | Perfil del usuario logueado |

## Chat 1:1 (WebSocket)

- URL del WebSocket: `ws://<host>/ws/chat/<user_id>/`
- Sala: `chat_<idMenor>_<idMayor>` (independiente de quién inicia)
- Protocolo:
  - Cliente → server: `{"message": "...", "destinatario_id": <int>}`
  - Server → cliente (al conectar): `{"type": "history", "messages": [...]}`
  - Server → cliente (broadcast): `{"type": "message", "message": "...",
    "sender_id": <int>, "sender_nombre": "...", "destinatario_id": <int>,
    "created_at": "ISO-8601", "message_id": <int>}`
- Persistencia: cada mensaje se guarda en `Message` con
  `room_identifier` para que el history se filtre correctamente
- Reconexión: el cliente reintenta cada 3s si el socket se cierra

## Tema Visual (Color de Marca)

- Verde primario: `--agendate-green: #1a4a2e`
- Verde hover: `--agendate-green-dark: #0f3020`
- Verde claro: `--agendate-green-light: #2c7a4d`
- Dorado acento: `--agendate-gold: #f5c842`

`--bs-primary` se override en `templates/includes/theme.html`, así que
**todos** los `btn-primary`, `text-primary`, `bg-primary`,
`btn-outline-primary` y links se renderizan en verde automáticamente.
Para cambiar el tema, editar las variables en ese único archivo.

## Navbars

- `templates/includes/marketing_navbar.html`: navbar completo con links a
  secciones y CTAs según `user.is_authenticated` (home + explore)
- `templates/includes/auth_navbar.html`: navbar mínimo con "Volver al
  inicio" + CTA opuesto (login + registro)

## Notas

- **Static files**: WhiteNoise está en `MIDDLEWARE` para que Daphne
  sirva `/static/...` correctamente. Sin esto, los estilos no cargan.
- **CSRF y WebSocket**: la cookie de sesión se envía en el header
  `Cookie` del handshake; Channels la pasa al `scope['user']`.
- **AllowedHosts en WebSocket**: el `Origin` debe estar en
  `ALLOWED_HOSTS` (default `localhost,127.0.0.1`).
