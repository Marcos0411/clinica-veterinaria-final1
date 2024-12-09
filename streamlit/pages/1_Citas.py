import streamlit as st
import requests
import pandas as pd

# URL base de la API de FastAPI
API_URL = "http://localhost:8000"

# Función para registrar una nueva cita
def registrar_cita(mascota, dueno, tratamiento, fecha, hora):
    response = requests.post(f"{API_URL}/citas/", json={
        "nombre_mascota": mascota,
        "nombre_dueno": dueno,
        "tratamiento": tratamiento,
        "fecha_inicio": f"{fecha}T{hora}"
    })
    if response.status_code == 200:
        st.success("Cita registrada correctamente")
        st.session_state["refresh"] = True
    else:
        st.error("Error al registrar cita")

# Función para obtener la lista de mascotas
def obtener_mascotas():
    response = requests.get(f"{API_URL}/mascotas/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener mascotas")
        return []

# Función para obtener la lista de dueños
def obtener_duenos():
    response = requests.get(f"{API_URL}/duenos/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener dueños")
        return []

# Función para obtener la lista de tratamientos
def obtener_tratamientos():
    response = requests.get(f"{API_URL}/tratamientos/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener tratamientos")
        return []

# Función para obtener la lista de citas
def obtener_citas():
    response = requests.get(f"{API_URL}/citas/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener citas")
        return []

# Función para cancelar una cita
def cancelar_cita(cita_id):
    response = requests.delete(f"{API_URL}/citas/{cita_id}")
    if response.status_code == 200:
        st.success("Cita cancelada correctamente")
        st.session_state["refresh"] = True
    else:
        st.error("Error al cancelar cita")

# Interfaz de usuario con Streamlit
st.title("Gestión de Citas")

# Obtener listas de mascotas, dueños y tratamientos
mascotas = obtener_mascotas()
duenos = obtener_duenos()
tratamientos = obtener_tratamientos()

# Crear formulario para registrar citas
with st.form("registro_cita"):
    mascota = st.selectbox("Mascota", [m['nombre'] for m in mascotas])
    dueno = st.selectbox("Dueño", [d['nombre_dueno'] for d in duenos])
    tratamiento = st.selectbox("Tratamiento", [t['nombre'] for t in tratamientos])
    fecha = st.date_input("Fecha")
    hora = st.time_input("Hora")
    
    submitted = st.form_submit_button("Registrar Cita")
    if submitted:
        registrar_cita(mascota, dueno, tratamiento, fecha, hora)

# Mostrar citas registradas
st.header("Citas Registradas")
if "refresh" in st.session_state and st.session_state["refresh"]:
    citas = obtener_citas()
    st.session_state["refresh"] = False
else:
    citas = obtener_citas()

if citas:
    df_citas = pd.DataFrame(citas)
    st.dataframe(df_citas)
else:
    st.write("No hay citas registradas")

# Formulario para cancelar citas
st.header("Cancelar Cita")
with st.form("cancelar_cita"):
    cita_id = st.number_input("ID de la cita a cancelar", min_value=1, step=1)
    submitted_cancelar = st.form_submit_button("Cancelar Cita")
    if submitted_cancelar:
        cancelar_cita(cita_id)
