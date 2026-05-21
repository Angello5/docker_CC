import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

st.set_page_config(
    page_title="Mini App Supabase + Streamlit",
    page_icon="✅",
    layout="wide",
)

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
TABLE_NAME = "tasks"


@st.cache_resource(show_spinner=False)
def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise RuntimeError(
            "Faltan variables de entorno: SUPABASE_URL y/o SUPABASE_ANON_KEY. "
            "Crea un archivo .env usando .env.example como referencia."
        )
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def fetch_tasks():
    client = get_supabase_client()
    response = (
        client.table(TABLE_NAME)
        .select("id,title,description,status,priority,created_at")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data or []


def create_task(title: str, description: str, status: str, priority: str):
    client = get_supabase_client()
    payload = {
        "title": title.strip(),
        "description": description.strip(),
        "status": status,
        "priority": priority,
    }
    return client.table(TABLE_NAME).insert(payload).execute()


def update_task(task_id: int, title: str, description: str, status: str, priority: str):
    client = get_supabase_client()
    payload = {
        "title": title.strip(),
        "description": description.strip(),
        "status": status,
        "priority": priority,
    }
    return client.table(TABLE_NAME).update(payload).eq("id", task_id).execute()


def delete_task(task_id: int):
    client = get_supabase_client()
    return client.table(TABLE_NAME).delete().eq("id", task_id).execute()


def format_date(value: str) -> str:
    if not value:
        return "-"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return value


st.title("✅ Mini gestor de tareas")
st.caption("Aplicación sencilla con Docker, Streamlit y Supabase.")

with st.sidebar:
    st.header("Configuración")
    st.write("Estado de conexión:")
    if SUPABASE_URL and SUPABASE_ANON_KEY:
        st.success("Variables Supabase cargadas")
    else:
        st.error("Faltan variables Supabase")

    st.divider()
    st.markdown(
        """
        **Antes de usar:**
        1. Crea un proyecto en Supabase.
        2. Ejecuta `app/schema.sql` en SQL Editor.
        3. Copia `.env.example` como `.env`.
        4. Coloca `SUPABASE_URL` y `SUPABASE_ANON_KEY`.
        """
    )

try:
    tasks = fetch_tasks()
except Exception as exc:
    st.error("No se pudo conectar o consultar Supabase.")
    st.code(str(exc))
    st.stop()

col_metric_1, col_metric_2, col_metric_3, col_metric_4 = st.columns(4)
col_metric_1.metric("Total", len(tasks))
col_metric_2.metric("Pendientes", sum(1 for t in tasks if t.get("status") == "Pendiente"))
col_metric_3.metric("En progreso", sum(1 for t in tasks if t.get("status") == "En progreso"))
col_metric_4.metric("Completadas", sum(1 for t in tasks if t.get("status") == "Completada"))

st.divider()

left, right = st.columns([1, 1.5])

with left:
    st.subheader("Crear nueva tarea")
    with st.form("create_task_form", clear_on_submit=True):
        title = st.text_input("Título", placeholder="Ejemplo: Preparar demo de Docker")
        description = st.text_area("Descripción", placeholder="Detalle breve de la tarea")
        status = st.selectbox("Estado", ["Pendiente", "En progreso", "Completada"])
        priority = st.selectbox("Prioridad", ["Baja", "Media", "Alta"], index=1)
        submitted = st.form_submit_button("Guardar tarea")

        if submitted:
            if not title.strip():
                st.warning("El título es obligatorio.")
            else:
                create_task(title, description, status, priority)
                st.success("Tarea creada correctamente.")
                st.rerun()

with right:
    st.subheader("Listado de tareas")

    if not tasks:
        st.info("Todavía no hay tareas registradas.")
    else:
        selected_status = st.selectbox(
            "Filtrar por estado",
            ["Todos", "Pendiente", "En progreso", "Completada"],
            key="status_filter",
        )

        filtered_tasks = [
            task for task in tasks
            if selected_status == "Todos" or task.get("status") == selected_status
        ]

        for task in filtered_tasks:
            with st.expander(f"#{task['id']} · {task['title']} · {task['status']}"):
                st.write(task.get("description") or "Sin descripción")
                st.caption(
                    f"Prioridad: {task.get('priority', '-')} | "
                    f"Creado: {format_date(task.get('created_at', ''))}"
                )

                edit_col, delete_col = st.columns([3, 1])

                with edit_col:
                    with st.form(f"edit_form_{task['id']}"):
                        edited_title = st.text_input("Título", value=task.get("title", ""))
                        edited_description = st.text_area(
                            "Descripción",
                            value=task.get("description") or "",
                        )
                        edited_status = st.selectbox(
                            "Estado",
                            ["Pendiente", "En progreso", "Completada"],
                            index=["Pendiente", "En progreso", "Completada"].index(task.get("status", "Pendiente")),
                        )
                        edited_priority = st.selectbox(
                            "Prioridad",
                            ["Baja", "Media", "Alta"],
                            index=["Baja", "Media", "Alta"].index(task.get("priority", "Media")),
                        )
                        if st.form_submit_button("Actualizar"):
                            if not edited_title.strip():
                                st.warning("El título no puede quedar vacío.")
                            else:
                                update_task(
                                    task["id"],
                                    edited_title,
                                    edited_description,
                                    edited_status,
                                    edited_priority,
                                )
                                st.success("Tarea actualizada.")
                                st.rerun()

                with delete_col:
                    st.write("")
                    st.write("")
                    if st.button("Eliminar", key=f"delete_{task['id']}"):
                        delete_task(task["id"])
                        st.success("Tarea eliminada.")
                        st.rerun()
