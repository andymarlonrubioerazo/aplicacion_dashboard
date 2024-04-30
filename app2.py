import streamlit as st 
import pandas as pd
import numpy as np
from io import BytesIO
import funciones as f
import plotly.express as px


# Título de nuestra aplicación
st.title('Resumen de respuestas')

# Subir base desde el computador
archivo_base = st.file_uploader('Subir base de datos',type=['xlsx'])

if archivo_base is not None:
    # Lectura de la base
    datos = pd.read_excel(archivo_base)    
    
    
    # Lista de opciones
    opciones = ['p1','p2','p3']

    st.subheader('Mi base de datos')
    
    # Mostramos la base
    st.write(datos)
    st.subheader('Analisis de las preguntas por genero')
    
    # Seleccion del pais
    paises = datos['pais'].unique()
    
    pais = st.selectbox('Seleccionar Pais',paises)
    
    # selectbox Widget
    pregunta = st.selectbox('Selecciona una opción',opciones)
    porcentajes = {}
    

    # Analisis
    datos = datos[datos['pais']==pais]
    
    fig = px.histogram(datos,x=pregunta)
    
    st.plotly_chart(fig)
    
    porcentajes[pregunta] = datos[['nombres','genero',pregunta]]
    df = pd.pivot_table(data=porcentajes[pregunta],index='genero',columns=pregunta,aggfunc='count')

    df.columns = df.columns.droplevel(0)

    df = df.transpose()
    df.reset_index(inplace=True)


    for i in df.columns[1:]:
        df[i] = df[i]/df.sum()[i]
        
    st.write(df)

    excel_file = f.to_excel(df)
    st.download_button(
        label = '📥 Descargar Excel',
        data=excel_file,
        file_name = f'respuestas_por_genero_{pais}_{pregunta}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )