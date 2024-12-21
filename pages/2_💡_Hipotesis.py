import pandas as pd
import plotly.express as px
import streamlit as st
from src.hipotesis import hipotesis_1, hipotesis_2


#Carga el DataFrame
@st.cache_data
def load_data():
    return pd.read_csv("data\Dry_Bean_Dataset.csv")  # Cambiar a la ruta de tu archivo

# Cargar datos
df = load_data()

st.title("Hipótesis del Proyecto")

# Hipótesis 1
st.header("Hipótesis 1: Análisis de Área por Clase")
fig_bar, fig_box = hipotesis_1(df)
st.plotly_chart(fig_bar, use_container_width=True)
st.plotly_chart(fig_box, use_container_width=True)

# Hipótesis 2
st.header("Hipótesis 2: Distribución del Área por Clase")
fig_scatter, fig_corr = hipotesis_2(df)
st.plotly_chart(fig_scatter, use_container_width=True)
st.plotly_chart(fig_corr, use_container_width=True)