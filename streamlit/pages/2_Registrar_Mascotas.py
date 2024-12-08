import streamlit as st
import requests
import pandas as pd

st.title("Registrar Mascotas")

def registrar_mascota(nombre, especie, raza, edad, propietario):
    url = 'http://localhost:8000/mascotas/'  # Updated URL
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
    url = 'http://localhost:8000/mascotas/'  # Updated URL
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error al obtener las mascotas: {response.status_code} - {response.text}")
        return []

def eliminar_mascota(nombre):
    url = f'http://localhost:8000/mascotas/{nombre}'
    response = requests.delete(url)
    return response.status_code

def obtener_duenos():
    url = 'http://localhost:8000/duenos/'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error al obtener los dueños: {response.status_code} - {response.text}")
        return []

with st.form("registro_mascota"):
    nombre = st.text_input("Nombre de la mascota")
    especie = st.selectbox("Especie", ["Perro", "Gato", "Ave", "Otro"])
    raza = st.text_input("Raza")
    edad = st.number_input("Edad", min_value=0, max_value=100, step=1)
    propietario = st.text_input("Nombre del propietario")
    
    submitted = st.form_submit_button("Registrar")
    if submitted:
        duenos = obtener_duenos()
        if any(dueno['nombre_dueno'] == propietario for dueno in duenos):
            status_code = registrar_mascota(nombre, especie, raza, edad, propietario)
            if status_code == 200:
                st.success("Mascota registrada exitosamente")
                st.session_state["refresh"] = True
            else:
                st.error("Error al registrar la mascota")
        else:
            st.error("El propietario no existe. Por favor, registre al propietario primero.")

with st.form("eliminar_mascota"):
    nombre_eliminar = st.text_input("Nombre de la mascota a eliminar")
    submitted_eliminar = st.form_submit_button("Eliminar")
    if submitted_eliminar:
        status_code = eliminar_mascota(nombre_eliminar)
        if status_code == 200:
            st.success("Mascota eliminada exitosamente")
            st.session_state["refresh"] = True
        else:
            st.error("Error al eliminar la mascota")

st.header("Mascotas Registradas")
if "refresh" in st.session_state and st.session_state["refresh"]:
    mascotas = obtener_mascotas()
    st.session_state["refresh"] = False
else:
    mascotas = obtener_mascotas()

if mascotas:
    df_mascotas = pd.DataFrame(mascotas)
    st.markdown(
        """
        <style>
        .dataframe {
            border-collapse: collapse;
            width: 100%;
        }
        .dataframe th, .dataframe td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        .dataframe th {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #4CAF50;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
    st.dataframe(df_mascotas)
else:
    st.write("No hay mascotas registradas")