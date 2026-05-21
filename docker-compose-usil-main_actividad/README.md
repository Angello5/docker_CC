# Mini App Docker + Streamlit + Supabase

Este proyecto es una aplicación sencilla de gestión de tareas construida con:

- Docker Compose
- Streamlit
- Supabase PostgreSQL
- Python

La app permite crear, listar, actualizar y eliminar tareas usando una tabla `tasks` en Supabase.

## 1. Crear proyecto en Supabase

Entra a Supabase, crea un proyecto nuevo y copia estos datos desde Project Settings > API:

- Project URL
- anon public key

## 2. Crear la tabla en Supabase

Abre Supabase SQL Editor y ejecuta el script:

```sql
-- Ver archivo app/schema.sql
```

El script completo está en:

```bash
app/schema.sql
```

## 3. Configurar variables de entorno

Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

Edita `.env` y coloca tus credenciales:

```env
SUPABASE_URL=https://TU-PROYECTO.supabase.co
SUPABASE_ANON_KEY=TU_SUPABASE_ANON_KEY
```

## 4. Levantar la aplicación

Desde la raíz del proyecto ejecuta:

```bash
docker compose up --build
```

Luego abre en el navegador:

```text
http://localhost:8501
```

## 5. Detener la aplicación

```bash
docker compose down
```

## Estructura del proyecto

```text
.
├── app
│   ├── app.py
│   ├── requirements.txt
│   └── schema.sql
├── docker-compose.yml
├── .env.example
└── README.md
```

## Nota de seguridad

Este ejemplo usa la llave `anon` y políticas RLS abiertas para fines educativos. Para producción, debes usar autenticación real, políticas por usuario y evitar operaciones públicas sin control.
