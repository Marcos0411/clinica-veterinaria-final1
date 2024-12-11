import streamlit as st
import requests
import ast

st.title("Gestión de Facturas")

# Función para obtener facturas
def obtener_facturas():
    response = requests.get('http://localhost:8000/facturas/')
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener las facturas")
        return []

# Función para obtener tratamientos
def obtener_tratamientos():
    response = requests.get('http://localhost:8000/tratamientos/')
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener los tratamientos")
        return []

# Función para actualizar el estado de pago de una factura
def actualizar_estado_factura(factura_id, estado_pago):
    response = requests.put(f"http://localhost:8000/facturas/{factura_id}", json={"estado_pago": estado_pago})
    if response.status_code == 200:
        st.success("Estado de pago actualizado correctamente")
    else:
        st.error("Error al actualizar el estado de pago")

# Función para actualizar la factura con tratamientos extras
def actualizar_factura_con_tratamientos(factura_id, tratamientos_extras, nuevo_total):
    response = requests.put(f"http://localhost:8000/facturas/{factura_id}/tratamientos", json={"tratamientos": tratamientos_extras, "total": nuevo_total})
    if response.status_code == 200:
        st.success("Factura actualizada correctamente")
    else:
        st.error("Error al actualizar la factura")

# Mostrar facturas en tabs
facturas = obtener_facturas()
tratamientos = obtener_tratamientos()
tab1, tab2 = st.tabs(["Facturas Pendientes", "Facturas Pagadas"])

with tab1:
    st.header("Facturas Pendientes")
    for factura in facturas:
        if factura['estado_pago'] == "pendiente":
            st.write(f"Factura ID: {factura['id']}")
            st.write(f"Cliente: {factura['cliente']}")
            st.write(f"Mascota: {factura['mascota']}")
            st.write(f"Tratamientos: {factura['tratamientos']}")
            st.write(f"Productos: {factura['productos']}")
            st.write(f"Total: {factura['total']}")
            st.write(f"Estado de Pago: {factura['estado_pago']}")
            tratamientos_extras = st.multiselect("Añadir Tratamientos Extras", [t['nombre'] for t in tratamientos], key=f"tratamientos_{factura['id']}")
            if st.button("Actualizar Factura", key=f"actualizar_{factura['id']}"):
                tratamientos_actuales = ast.literal_eval(factura['tratamientos']) if isinstance(factura['tratamientos'], str) else factura['tratamientos']
                nuevo_total = factura['total'] + sum(t['precio'] for t in tratamientos if t['nombre'] in tratamientos_extras)
                tratamientos_completos = list(set(tratamientos_actuales + tratamientos_extras))
                actualizar_factura_con_tratamientos(factura['id'], tratamientos_completos, nuevo_total)
            if st.button("Marcar como Pagada", key=f"pagada_{factura['id']}"):
                actualizar_estado_factura(factura['id'], "pagada")
            st.write("---")

with tab2:
    st.header("Facturas Pagadas")
    for factura in facturas:
        if factura['estado_pago'] == "pagada":
            st.write(f"Factura ID: {factura['id']}")
            st.write(f"Cliente: {factura['cliente']}")
            st.write(f"Mascota: {factura['mascota']}")
            st.write(f"Tratamientos: {factura['tratamientos']}")
            st.write(f"Productos: {factura['productos']}")
            st.write(f"Total: {factura['total']}")
            tratamientos_actuales = ast.literal_eval(factura['tratamientos']) if isinstance(factura['tratamientos'], str) else factura['tratamientos']
            st.write("---")