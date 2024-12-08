import streamlit as st
import time

# Configuración de la página
st.set_page_config(page_title='Clínica Veterinaria', layout='wide', page_icon="🐾")

# Título de la aplicación
st.title("🐾 CLÍNICA VETERINARIA CUATRO PATAS 🐾")

st.image('logo.jpg')

placeholder = st.empty()
with placeholder:
    #from PIL import Image
    #image = Image.open('mired.png')
    #placeholder.image(image, caption='MiRed semantic engine',use_column_width = 'always') 
    for seconds in range(5):
        placeholder.write(f"⏳ {seconds} Cargando sistema")
        time.sleep(1)
placeholder.empty()


st.write("# Cuidamos a tus mejores amigos como si fueran nuestros.")

st.sidebar.success("Selecciona una página. Eres libre de seleccionar.")

