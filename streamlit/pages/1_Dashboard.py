import streamlit as st
import pandas as pd

# Título del Dashboard
st.title("Dashboard de la Clínica Veterinaria")

# Cargar datos desde CSV
productos_df = pd.read_csv('/home/marcoscabeza/clinica-veterinaria-final1/fastapi/registroProductos.csv')
mascotas_df = pd.read_csv('/home/marcoscabeza/clinica-veterinaria-final1/fastapi/registroMascotas.csv')
duenos_df = pd.read_csv('/home/marcoscabeza/clinica-veterinaria-final1/fastapi/registroDuenos.csv')
facturas_df = pd.read_csv('/home/marcoscabeza/clinica-veterinaria-final1/fastapi/facturas.csv')
citas_df = pd.read_csv('/home/marcoscabeza/clinica-veterinaria-final1/fastapi/citas.csv')

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

df = pd.DataFrame(data)

# Mostrar datos en una tabla
st.subheader("Estadísticas de Servicios")
st.table(df)

# Gráfica de barras
st.subheader("Distribución de Servicios")
st.bar_chart(df.set_index('Categoría'))

# Métricas clave
st.subheader("Métricas Clave")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Productos", str(productos_df.shape[0]))
col2.metric("Mascotas", str(mascotas_df.shape[0]))
col3.metric("Dueños", str(duenos_df.shape[0]))
col4.metric("Facturas", str(facturas_df.shape[0]))
col5.metric("Citas", str(citas_df.shape[0]))

# ...existing code...
