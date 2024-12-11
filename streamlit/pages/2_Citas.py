import streamlit as st
import requests
import pandas as pd


# URL base de la API de FastAPI
API_URL = "http://localhost:8000"

# Función para registrar una nueva cita
def registrar_cita(mascota, dueno, tratamiento, fecha, hora):
    fecha_hora = f"{fecha.strftime('%Y-%m-%d')} {hora.strftime('%H:%M:%S')}"
    response = requests.post(f"{API_URL}/citas/", json={
        "nombre_mascota": mascota,
        "nombre_dueno": dueno,
        "tratamiento": tratamiento,
        "fecha_inicio": fecha_hora,
        "estado": "pendiente"
    })
    if response.status_code == 200:
        st.success("Cita registrada correctamente")
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
        citas = response.json()
        for cita in citas:
            for key, value in cita.items():
                if isinstance(value, float) and (value == float('inf') or value == float('-inf') or value != value):
                    cita[key] = str(value)
        return citas
    else:
        st.error("Error al obtener citas")
        return []

# Función para cancelar una cita
def cancelar_cita(cita_id):
    response = requests.delete(f"{API_URL}/citas/{cita_id}")
    if response.status_code == 200:
        st.success("Cita cancelada correctamente")
    else:
        st.error("Error al cancelar cita")

# Función para actualizar el estado de una cita
def actualizar_estado_cita(cita_id, nuevo_estado):
    response = requests.put(f"{API_URL}/citas/{cita_id}", json={"estado": nuevo_estado})
    if response.status_code == 200:
        st.success(f"Cita {nuevo_estado} correctamente")
    else:
        st.error(f"Error al {nuevo_estado} la cita")

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

# Mostrar tabla de citas
st.header("Tabla de Citas")
citas = obtener_citas()
citas_df = pd.DataFrame(citas)

# Mostrar tabla interactiva con botones
for index, row in citas_df.iterrows():
    st.write(f"Cita ID: {row['id']}, Mascota: {row['nombre_mascota']}, Dueño: {row['nombre_dueno']}, Tratamiento: {row['tratamiento']}, Fecha: {row['fecha_inicio']}, Estado: {row['estado']}")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(f"Aceptar {row['id']}", key=f"aceptar_{row['id']}"):
            actualizar_estado_cita(row['id'], "aceptada")
    with col2:
        if st.button(f"Rechazar {row['id']}", key=f"rechazar_{row['id']}"):
            actualizar_estado_cita(row['id'], "rechazada")
