import streamlit as st
import requests

st.title("Gestión de Facturas")

# Función para obtener facturas
def obtener_facturas():
    response = requests.get('http://localhost:8000/facturas/')
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener las facturas")
        return []

# Función para actualizar el estado de pago de una factura
def actualizar_estado_factura(factura_id, estado_pago):
    response = requests.put(f"http://localhost:8000/facturas/{factura_id}", json={"estado_pago": estado_pago})
    if response.status_code == 200:
        st.success("Estado de pago actualizado correctamente")
    else:
        st.error("Error al actualizar el estado de pago")

# Mostrar facturas
facturas = obtener_facturas()
for factura in facturas:
    st.write(f"Factura ID: {factura['id']}")
    st.write(f"Cliente: {factura['cliente']}")
    st.write(f"Mascota: {factura['mascota']}")
    st.write(f"Tratamientos: {factura['tratamientos']}")
    st.write(f"Productos: {factura['productos']}")
    st.write(f"Total: {factura['total']}")
    st.write(f"Estado de Pago: {factura['estado_pago']}")
    if st.button("Marcar como Pagada", key=f"pagada_{factura['id']}"):
        actualizar_estado_factura(factura['id'], "pagada")
    st.write("---")