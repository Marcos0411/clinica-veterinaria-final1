import streamlit as st
import requests
import pandas as pd

# URL base de la API de FastAPI
API_URL = "http://fastapi:8000"

# Función para obtener la lista de productos
def obtener_productos():
    response = requests.get(f"{API_URL}/productos/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener productos")
        return []

# Función para agregar un nuevo producto
def agregar_producto(categoria, marca, precio, stock):
    response = requests.post(f"{API_URL}/productos/", json={
        "categoria": categoria,
        "marca": marca,
        "precio": precio,
        "stock": stock
    })
    if response.status_code == 200:
        st.success("Producto agregado correctamente")
    else:
        st.error("Error al agregar producto")

# Función para eliminar un producto
def eliminar_producto(producto_id):
    response = requests.delete(f"{API_URL}/productos/{producto_id}")
    if response.status_code == 200:
        st.success("Producto eliminado correctamente")
    else:
        st.error("Error al eliminar producto")

# Función para modificar el precio de un producto
def modificar_precio(producto_id, nuevo_precio):
    response = requests.put(f"{API_URL}/productos/{producto_id}/", json={
        "precio": nuevo_precio
    })
    if response.status_code == 200:
        st.success("Precio modificado correctamente")
    else:
        st.error("Error al modificar precio")

# Función para buscar productos
def buscar_productos(criterio):
    response = requests.get(f"{API_URL}/productos/search?criterio={criterio}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al buscar productos")
        return []

# Función para vender un producto
def vender_producto(producto_id, cantidad):
    response = requests.post(f"{API_URL}/ventas/", json={
        "producto_id": int(producto_id),
        "cantidad": cantidad
    })
    if response.status_code == 200:
        st.success("Producto vendido correctamente")
        return response.json()["producto"]
    else:
        st.error("Error al vender producto")
        return None

# Interfaz de usuario con Streamlit
st.title("Gestión de Productos")

# Crear pestañas
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Lista de Productos", "Agregar Producto", "Eliminar Producto", "Modificar Precio", "Buscar Producto", "Vender Producto"])

# Pestaña para mostrar lista de productos
with tab1:
    st.header("Lista de Productos")
    productos = obtener_productos()
    if productos:
        df_productos = pd.DataFrame(productos)
        st.dataframe(df_productos)
    else:
        st.write("No hay productos registrados")

# Pestaña para agregar un nuevo producto
with tab2:
    st.header("Agregar Nuevo Producto")
    categoria = st.text_input("Categoría")  # Changed to text input
    marca = st.text_input("Marca")
    precio = st.number_input("Precio", min_value=0.0, format="%.2f")
    stock = st.number_input("Stock", min_value=0, step=1)
    if st.button("Agregar Producto"):
        agregar_producto(categoria, marca, precio, stock)

# Pestaña para eliminar un producto
with tab3:
    st.header("Eliminar Producto")
    producto_id = st.text_input("ID del Producto a Eliminar", key="eliminar_producto_id")
    if st.button("Eliminar Producto"):
        eliminar_producto(producto_id)

# Pestaña para modificar el precio de un producto
with tab4:
    st.header("Modificar Precio de Producto")
    producto_id = st.text_input("ID del Producto", key="modificar_precio_producto_id")
    nuevo_precio = st.number_input("Nuevo Precio", min_value=0.0, format="%.2f")
    if st.button("Modificar Precio"):
        modificar_precio(producto_id, nuevo_precio)

# Pestaña para buscar productos
with tab5:
    st.header("Buscar Producto")
    criterio = st.text_input("Criterio de Búsqueda (Nombre o Tipología)")
    if st.button("Buscar"):
        productos = buscar_productos(criterio)
        if productos:
            df_productos = pd.DataFrame(productos)
            st.dataframe(df_productos)
        else:
            st.write("No se encontraron productos")

# Pestaña para vender un producto
with tab6:
    st.header("Vender Producto")
    producto_id = st.text_input("ID del Producto", key="vender_producto_id")
    cantidad = st.number_input("Cantidad", min_value=1, step=1, key="vender_producto_cantidad")
    if st.button("Vender Producto"):
        producto_vendido = vender_producto(producto_id, cantidad)
        if producto_vendido:
            productos = obtener_productos()
            df_productos = pd.DataFrame(productos)
            st.dataframe(df_productos)