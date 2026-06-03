# Spec: Frontend AdminLTE + Landing Dinámica

**Change**: adminlte-frontend
**Date**: 2026-05-25
**Mode**: hybrid (engram + openspec/)

---

## 1. Overview

Reemplazar el frontend actual de AgendateNarino con **AdminLTE v4.0.0** vía CDN, manteniendo los templates originales intactos. La landing page (`/`) será dinámica y pública, mostrando eventos en cards + mapa interactivo. Los accesos posteriores dependen del rol del usuario (Cliente, Moderador, Admin).

---

## 2. Stack

- **AdminLTE**: v4.0.0 vía CDN (sin jQuery, Bootstrap 5.3)
- **Mapa**: Leaflet + OpenStreetMap (gratis, sin API key)
- **Template base**: `templates/base_adminlte.html` (nuevo)
- **Login**: `templates/adminLTE/login.html` (nuevo)
- **Dashboards**: `templates/adminLTE/dashboard.html`, `client_dashboard.html`
- **Landing**: `eventos/templates/eventos/home.html` (nuevo)

---

## 3. Páginas y URLs

| URL | Template | Auth | Descripción |
|-----|----------|------|-------------|
| `/` | `eventos/home.html` | No | Landing dinámica + eventos |
| `/eventos/` | `eventos/evento_list.html` | No | Lista pública eventos |
| `/eventos/<id>/` | `eventos/evento_detail.html` | No | Detalle evento público |
| `/usuarios/login/` | `adminLTE/login.html` | No | Login con diseño AdminLTE |
| `/admin/` | `adminLTE/dashboard.html` | Sí | Dashboard Moderador/Admin |
| `/cliente/` | `adminLTE/client_dashboard.html` | Sí | Dashboard Cliente |
| `/messaging/inbox/` | `messaging/inbox.html` | Sí | Mensajes |

---

## 4. Landing Page (`/`)

### Header (sticky)
- Logo "Agéndate Nariño" a la izquierda
- Nav: Ingresar (si no auth), o nombre + menú contextual (si auth)
- Colores: verde oscuro (#1a4a2e) + amarillo (#f5c842) como en el diseño existente

### Hero Section
- Título: "Agéndate Nariño"
- Subtítulo: "Agenda de eventos culturales y artísticos del departamento"
- CTAs: "Ver Eventos" | "Conocer más"

### Eventos Destacados (grid 3 columnas)
- Cards con: imagen flyer, título, fecha, municipio, badge categoría
- Máximo 6 eventos (los más cercanos con `activo=True`)
- Link "Ver todos los eventos →" lleva a `/eventos/`

### Mapa Interactivo (Leaflet + OSM)
- Centrado en Nariño (lat 1.2, lon -77.3)
- Markers circulares por categoría (colores distintos)
- Popup: nombre evento + fecha + "Ver detalle"
- Solo eventos con `activo=True` y `fecha >= hoy`

### Sección Info
- "¿Qué es Agendate Nariño?" — texto corto
- Stats: número de eventos, municipios, organizadores

### Footer
- Copyright + links

---

## 5. Navegación — Sidebar según rol

### Sin login (público)
- No sidebar, solo header

### Cliente
- Dashboard (resumen de sus eventos)
- Mis Eventos (create/edit/delete)
- Mi Perfil
- Salir

### Moderador
- Dashboard (métricas globales)
- Eventos (lista completa + approve/reject)
- Clientes
- Usuarios
- Mensajes
- Calificaciones
- Salir

### Admin (superuser)
- Todo lo de Moderador
- Configuración

---

## 6. Login Page (`/usuarios/login/`)

- Diseño AdminLTE (starter login page)
- Logo Agendate Nariño
- Campos: username + password
- Error de autenticación inline
- "¿Olvidó su contraseña?" (opcional, disabled por ahora)

---

## 7. Dashboards

### Dashboard Moderador/Admin (`/admin/`)
- KPI cards: total eventos, clientes, mensajes, visitas
- Tabla de últimos eventos
- Tabla de últimos mensajes

### Dashboard Cliente (`/cliente/`)
- KPI cards: mis eventos activos, total eventos, próxima fecha
- Lista de mis eventos recientes

---

## 8. CDN AdminLTE

```html
<!-- <head> -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/admin-lte@4.0.0/dist/css/adminlte.min.css" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.min.css" />

<!-- antes </body> -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/admin-lte@4.0.0/dist/js/adminlte.min.js"></script>
```

---

## 9. No modificar

- `templates/base.html` (original, se mantiene intacto)
- `templates/*.html` en `usuarios/`, `eventos/`, `messaging/` (originales)
- Archivos CSS/JS originales del proyecto

---

## 10. Archivos a crear

1. `templates/base_adminlte.html` — base con estructura AdminLTE
2. `templates/adminLTE/login.html` — login page
3. `templates/adminLTE/dashboard.html` — dashboard admin/moderador
4. `templates/adminLTE/client_dashboard.html` — dashboard cliente
5. `eventos/templates/eventos/home.html` — landing dinámica
6. `eventos/views.py` — agregar `home` view
7. `agendate_narino/urls.py` — agregar ruta `/`
8. `eventos/urls.py` — agregar ruta home

---

## 11. Modelos usados

- `Evento`: título, fecha, municipio, geolocalización, categoria, cliente, activo
- `Categoria`: nombre, color (para marker del mapa)
- `Cliente`: nombre_comercial, usuario

---

## 12. Tech

- Leaflet CDN: `https://unpkg.com/leaflet@1.9.4/dist/leaflet.css` + `.js`
- OpenStreetMap tiles: sin API key