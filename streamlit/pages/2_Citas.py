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
        return response.json()
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

# Función para modificar una cita
def modificar_cita(cita_id, mascota, dueno, tratamiento, fecha, hora):
    fecha_hora = f"{fecha.strftime('%Y-%m-%d')} {hora.strftime('%H:%M:%S')}"
    response = requests.put(f"{API_URL}/citas/{cita_id}", json={
        "nombre_mascota": mascota,
        "nombre_dueno": dueno,
        "tratamiento": tratamiento,
        "fecha_inicio": fecha_hora,
        "estado": "pendiente"
    })
    if response.status_code == 200:
        st.success("Cita modificada correctamente")
    else:
        st.error("Error al modificar cita")

# Función para obtener la lista de productos
def obtener_productos():
    response = requests.get(f"{API_URL}/productos/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener productos")
        return []

# Función para generar factura
def generar_factura(cita_id):
    cita = next((c for c in citas if c['id'] == cita_id), None)
    if not cita:
        st.error("Cita no encontrada")
        return

    tratamientos = obtener_tratamientos()
    total_tratamientos = sum(t['precio'] for t in tratamientos if t['nombre'] == cita['tratamiento'])
    
    productos = obtener_productos()
    total_productos = sum(p['precio'] for p in productos if p['id'] in cita.get('productos', []))
    
    total = total_tratamientos + total_productos

    factura = {
        "id": cita_id,
        "cliente": cita['nombre_dueno'],
        "mascota": cita['nombre_mascota'],
        "tratamientos": cita['tratamiento'],
        "productos": cita.get('productos', []),
        "total": total,
        "estado_pago": "pendiente"
    }
    
    response = requests.post(f"{API_URL}/facturas/", json=factura)
    if response.status_code == 200:
        st.success("Factura generada correctamente")
    else:
        st.error("Error al generar la factura")

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
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button(f"Aceptar {row['id']}", key=f"aceptar_{row['id']}_{index}"):
            actualizar_estado_cita(row['id'], "aceptada")
    with col2:
        if st.button(f"Rechazar {row['id']}", key=f"rechazar_{row['id']}_{index}"):
            actualizar_estado_cita(row['id'], "rechazada")
    with col3:
        if st.button(f"Modificar {row['id']}", key=f"modificar_{row['id']}_{index}"):
            with st.form(f"modificar_cita_{row['id']}"):
                mascota = st.selectbox("Mascota", [m['nombre'] for m in mascotas], index=[m['nombre'] for m in mascotas].index(row['nombre_mascota']))
                dueno = st.selectbox("Dueño", [d['nombre_dueno'] for d in duenos], index=[d['nombre_dueno'] for d in duenos].index(row['nombre_dueno']))
                tratamiento = st.selectbox("Tratamiento", [t['nombre'] for t in tratamientos], index=[t['nombre'] for t in tratamientos].index(row['tratamiento']))
                fecha = st.date_input("Fecha", value=pd.to_datetime(row['fecha_inicio']).date())
                hora = st.time_input("Hora", value=pd.to_datetime(row['fecha_inicio']).time())
                submitted = st.form_submit_button("Modificar Cita")
                if submitted:
                    modificar_cita(row['id'], mascota, dueno, tratamiento, fecha, hora)
    with col4:
        if st.button(f"Cancelar {row['id']}", key=f"cancelar_{row['id']}_{index}"):
            cancelar_cita(row['id'])
    with col5:
        if st.button(f"Generar Factura {row['id']}", key=f"factura_{row['id']}_{index}"):
            generar_factura(row['id'])
