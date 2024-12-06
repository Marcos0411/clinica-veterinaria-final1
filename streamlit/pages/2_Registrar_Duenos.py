import streamlit as st
import requests
import pandas as pd
import os

st.title("Registro de Dueños")

# Formulario para buscar dueño existente por DNI
st.header("Buscar Dueño Existente por DNI")
dni_dueno = st.text_input("DNI del Dueño")
if st.button("Buscar Dueño por DNI"):
    response = requests.get(f"http://localhost:8000/buscar_dueno/{dni_dueno}")
    if response.status_code == 200:
        dueno = response.json()
        st.write("Dueño encontrado:", dueno)
    else:
        st.error("Dueño no encontrado")

# Formulario para buscar dueño existente por nombre
st.header("Buscar Dueño Existente por Nombre")
nombre_dueno = st.text_input("Nombre del Dueño")
if st.button("Buscar Dueño por Nombre"):
    response = requests.get(f"http://localhost:8000/buscar_dueno_por_nombre/{nombre_dueno}")
    if response.status_code == 200:
        duenos = response.json()
        st.write("Dueños encontrados:", duenos)
    else:
        st.error("Dueño no encontrado")

# Formulario para buscar dueño existente por nombre de mascota
st.header("Buscar Dueño Existente por Nombre de Mascota")
nombre_mascota = st.text_input("Nombre de la Mascota")
if st.button("Buscar Dueño por Nombre de Mascota"):
    response = requests.get(f"http://localhost:8000/buscar_dueno_por_mascota/{nombre_mascota}")
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
    response = requests.post("http://localhost:8000/alta_duenos/", json=nuevo_dueno)
    if response.status_code == 200:
        st.success("Dueño registrado correctamente")
    else:
        st.error("Error al registrar dueño")

# Mostrar el archivo CSV de dueños registrados
st.header("Dueños Registrados")
csv_path = '/home/marcoscabeza/clinica-veterinaria-final1/fastapi/registroDuenos.csv'
st.write(f"Verificando la existencia del archivo: {csv_path}")
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
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
    st.dataframe(df)
else:
    st.error(f"El archivo {csv_path} no se encontró.")