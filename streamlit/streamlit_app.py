import streamlit as st
import requests
from datetime import datetime

st.title("Registro de Dueños y Mascotas")

# Formulario para buscar dueño existente por DNI
st.header("Buscar Dueño Existente por DNI")
dni_dueno = st.text_input("DNI del Dueño")
if st.button("Buscar Dueño por DNI"):
    response = requests.get(f"http://fastapi:8000/duenos/{dni_dueno}")
    if response.status_code == 200:
        dueno = response.json()
        st.write("Dueño encontrado:", dueno)
    else:
        st.error("Dueño no encontrado")

# Formulario para buscar dueño existente por nombre
st.header("Buscar Dueño Existente por Nombre")
nombre_dueno = st.text_input("Nombre del Dueño")
if st.button("Buscar Dueño por Nombre"):
    response = requests.get(f"http://fastapi:8000/buscar_dueno_por_nombre/{nombre_dueno}")
    if response.status_code == 200:
        duenos = response.json()
        st.write("Dueños encontrados:", duenos)
    else:
        st.error("Dueño no encontrado")

# Formulario para buscar dueño existente por nombre de mascota
st.header("Buscar Dueño Existente por Nombre de Mascota")
nombre_mascota = st.text_input("Nombre de la Mascota")
if st.button("Buscar Dueño por Nombre de Mascota"):
    response = requests.get(f"http://fastapi:8000/buscar_dueno_por_mascota/{nombre_mascota}")
    if response.status_code == 200:
        dueno = response.json()
        st.write("Dueño encontrado:", dueno)
    else:
        st.error("Dueño no encontrado")

# Formulario para registrar nuevo dueño
st.header("Registrar Nuevo Dueño")
with st.form("nuevo_dueno_form"):
    nombre_dueno = st.text_input("Nombre del Dueño")
    telefono_dueno = st.text_input("Teléfono del Dueño")
    email_dueno = st.text_input("Email del Dueño")
    dni_dueno_nuevo = st.text_input("DNI del Dueño")
    direccion_dueno = st.text_input("Dirección del Dueño")
    submit_dueno = st.form_submit_button("Registrar Dueño")

if submit_dueno:
    nuevo_dueno = {
        "nombre_dueno": nombre_dueno,
        "telefono_dueno": telefono_dueno,
        "email_dueno": email_dueno,
        "dni_dueno": dni_dueno_nuevo,
        "direccion_dueno": direccion_dueno
    }
    response = requests.post("http://fastapi:8000/alta_duenos/", json=nuevo_dueno)
    if response.status_code == 200:
        st.success("Dueño registrado correctamente")
    else:
        st.error("Error al registrar dueño")

# Formulario para registrar nueva mascota
st.header("Registrar Nueva Mascota")
with st.form("nueva_mascota_form"):
    nombre = st.text_input("Nombre de la Mascota")
    especie = st.text_input("Especie")
    raza = st.text_input("Raza")
    fecha_nacimiento = st.date_input("Fecha de Nacimiento")
    patologias_previas = st.text_area("Patologías Previas")
    propietario = st.text_input("DNI del Propietario")
    submit_mascota = st.form_submit_button("Registrar Mascota")

if submit_mascota:
    nueva_mascota = {
        "nombre": nombre,
        "especie": especie,
        "raza": raza,
        "fecha_nacimiento": fecha_nacimiento.isoformat(),
        "patologias_previas": patologias_previas,
        "propietario": propietario
    }
    response = requests.post("http://fastapi:8000/alta_mascota/", json=nueva_mascota)
    if response.status_code == 200:
        st.success("Mascota registrada correctamente")
    else:
        st.error("Error al registrar mascota")

# Mostrar dueños registrados
st.header("Dueños Registrados")
response = requests.get("http://fastapi:8000/duenos/")
if response.status_code == 200:
    duenos = response.json()
    st.write(duenos)
else:
    st.error("Error al recuperar la lista de dueños")