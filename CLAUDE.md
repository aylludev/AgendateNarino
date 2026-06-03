# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AgendateNarino is a Django-based event scheduling system for Nariño, Colombia. Cultural event managers (Clientes) create and publish events; moderators review them.

## Stack

- **Backend**: Django 4.2+, Python 3.10+
- **Database**: PostgreSQL (configured via `.env`)
- **Frontend**: Separate Vite build in `templates/home/` — used for landing page. AdminLTE templates in `templates/adminLTE/` — serves as reference
- **Auth**: Custom `Usuario` model extending `AbstractUser` (AUTH_USER_MODEL = `usuarios.Usuario`)

## Commands

```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit with DB credentials
python manage.py migrate
python manage.py createsuperuser

# Run
python manage.py runserver

# Frontend dev (templates/home/)
cd templates/home && npm install && npm run dev
```

## Architecture

- `agendate_narino/` — Django project settings, root URLs
- `usuarios/` — Custom user model, Cliente (Gestor Cultural)
- `eventos/` — Event and Category models
- `messaging/` — User-to-user messaging
- `core/` — Dashboard and main views
- `templates/adminLTE/` — AdminLTE template reference (static HTML)
- `templates/home/` — Vite-based landing page project

## Key Conventions

- Custom user model `Usuario` uses `Cedula` (ID number) as unique identifier
- Role detection: `is_moderador` flag on Usuario distinguishes moderator from regular user
- Language: Spanish (`LANGUAGE_CODE = 'es-co'`)
- Timezone: `America/Bogota`

## DB Config

Environment variables (from `.env`): `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

## Database

```sql
CREATE DATABASE agendatenarino;
```
