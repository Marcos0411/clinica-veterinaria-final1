import streamlit as st
import requests

# URL base de la API de FastAPI
API_URL = "http://localhost:8000"

# Función para obtener la lista de tratamientos
def obtener_tratamientos():
    response = requests.get(f"{API_URL}/tratamientos/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener tratamientos")
        return []

# Función para agregar un nuevo tratamiento
def agregar_tratamiento(nombre, precio):
    response = requests.post(f"{API_URL}/tratamientos/", json={"nombre": nombre, "precio": precio})
    if response.status_code == 200:
        st.success("Tratamiento agregado correctamente")
    else:
        st.error("Error al agregar tratamiento")

# Función para eliminar un tratamiento
def eliminar_tratamiento(nombre):
    response = requests.delete(f"{API_URL}/tratamientos/{nombre}")
    if response.status_code == 200:
        st.success("Tratamiento eliminado correctamente")
    else:
        st.error("Error al eliminar tratamiento")

# Función para registrar un nuevo dueño
def registrar_dueno(nombre, telefono, email, dni, direccion):
    response = requests.post(f"{API_URL}/alta_duenos/", json={
        "nombre_dueno": nombre,
        "telefono_dueno": telefono,
        "email_dueno": email,
        "dni_dueno": dni,
        "direccion_dueno": direccion
    })
    if response.status_code == 200:
        st.success("Dueño registrado correctamente")
    else:
        st.error("Error al registrar dueño")

# Función para registrar una nueva mascota
def registrar_mascota(nombre, especie, raza, edad, propietario):
    response = requests.post(f"{API_URL}/alta_mascota/", json={
        "nombre": nombre,
        "especie": especie,
        "raza": raza,
        "edad": edad,
        "propietario": propietario
    })
    if response.status_code == 200:
        st.success("Mascota registrada correctamente")
    else:
        st.error("Error al registrar mascota")

# Función para obtener la lista de dueños
def obtener_duenos():
    response = requests.get(f"{API_URL}/duenos/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener dueños")
        return []

# Función para obtener la lista de mascotas
def obtener_mascotas():
    response = requests.get(f"{API_URL}/mascotas/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener mascotas")
        return []

# Interfaz de usuario con Streamlit
st.title("Gestión de Tratamientos")

# Crear pestañas
tab1, tab2, tab3 = st.tabs(["Lista de Tratamientos", "Agregar Tratamiento", "Eliminar Tratamiento"])

# Pestaña para mostrar lista de tratamientos
with tab1:
    st.header("Lista de Tratamientos")
    tratamientos = obtener_tratamientos()
    for tratamiento in tratamientos:
        st.write(f"Nombre: {tratamiento['nombre']}, Precio: {tratamiento['precio']}")

# Pestaña para agregar un nuevo tratamiento
with tab2:
    st.header("Agregar Nuevo Tratamiento")
    nombre = st.text_input("Nombre del Tratamiento")
    precio = st.number_input("Precio del Tratamiento", min_value=0.0, format="%.2f")
    if st.button("Agregar Tratamiento"):
        agregar_tratamiento(nombre, precio)

# Pestaña para eliminar un tratamiento
with tab3:
    st.header("Eliminar Tratamiento")
    nombre_eliminar = st.text_input("Nombre del Tratamiento a Eliminar")
    if st.button("Eliminar Tratamiento"):
        eliminar_tratamiento(nombre_eliminar)