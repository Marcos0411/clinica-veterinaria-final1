import streamlit as st
import requests

st.title("Registrar Mascotas")

def registrar_mascota(nombre, especie, raza, edad, propietario):
    url = 'http://localhost:8000/mascotas'  
    data = {
        'nombre': nombre,
        'especie': especie,
        'raza': raza,
        'edad': edad,
        'propietario': propietario
    }
    response = requests.post(url, json=data)
    return response.status_code

def obtener_mascotas():
    url = 'http://localhost:8000/mascotas'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

with st.form("registro_mascota"):
    nombre = st.text_input("Nombre de la mascota")
    especie = st.selectbox("Especie", ["Perro", "Gato", "Ave", "Otro"])
    raza = st.text_input("Raza")
    edad = st.number_input("Edad", min_value=0, max_value=100, step=1)
    propietario = st.text_input("Nombre del propietario")
    
    submitted = st.form_submit_button("Registrar")
    if submitted:
        status_code = registrar_mascota(nombre, especie, raza, edad, propietario)
        if status_code == 200:
            st.success("Mascota registrada exitosamente")
        else:
            st.error("Error al registrar la mascota")

st.header("Mascotas Registradas")
mascotas = obtener_mascotas()
if mascotas:
    st.write(mascotas)
else:
    st.write("No hay mascotas registradas")