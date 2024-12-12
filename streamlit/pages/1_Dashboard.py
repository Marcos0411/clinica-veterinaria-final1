import streamlit as st
import pandas as pd
import os

# Título del Dashboard
st.title("Dashboard de la Clínica Veterinaria")

# Cargar datos desde CSV
csv_paths = {
    'productos': '/streamlit/registroProductos.csv',
    'mascotas': '/streamlit/registroMascotas.csv',
    'duenos': '/streamlit/registroDuenos.csv',
    'facturas': '/streamlit/facturas.csv',
    'citas': '/streamlit/citas.csv'
}

dataframes = {}
for key, path in csv_paths.items():
    st.write(f"Verificando la existencia del archivo: {path}")
    if os.path.exists(path):
        dataframes[key] = pd.read_csv(path)
    else:
        st.error(f"El archivo {path} no se encontró.")
        dataframes[key] = pd.DataFrame()  # Crear un DataFrame vacío para evitar errores posteriores

productos_df = dataframes['productos']
mascotas_df = dataframes['mascotas']
duenos_df = dataframes['duenos']
facturas_df = dataframes['facturas']
citas_df = dataframes['citas']

# Calcular estadísticas
data = {
    'Categoría': ['Productos', 'Mascotas', 'Dueños', 'Facturas', 'Citas'],
    'Cantidad': [
        productos_df.shape[0],
        mascotas_df.shape[0],
        duenos_df.shape[0],
        facturas_df.shape[0],
        citas_df.shape[0]
    ]
}

# Mostrar estadísticas
st.write(pd.DataFrame(data))