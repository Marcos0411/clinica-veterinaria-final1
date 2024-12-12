FROM python:3.11-slim

RUN mkdir /streamlit

COPY requirements.txt /streamlit

WORKDIR /streamlit

RUN pip install -r requirements.txt

COPY ../fastapi/registroDuenos.csv /streamlit/registroDuenos.csv

COPY . /streamlit

EXPOSE 8501

CMD ["streamlit", "run", "Pagina_de_inicio.py"]