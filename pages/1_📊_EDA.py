import streamlit as st
import pandas as pd
from src.eda import plot_heatmap, plot_class_count, plot_avg_major_axis_length, plot_scatter, plot_avg_minor_axis_length

# Carga el DataFrame
@st.cache_data
def load_data():
    return pd.read_csv("data/Dry_Bean_Dataset.csv")  

# Configuración de la página
st.title("Análisis Exploratorio de Datos (EDA)")

# Cargar datos
df = load_data()

# Información básica del conjunto de datos
st.header("Aspectos Básicos del Conjunto de Datos")
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Número de Filas", value=df.shape[0], border=True)
    with col2:
        st.metric(label="Número de Columnas", value=df.shape[1], border=True)
    with col3:
        missing_values = df.isnull().any().sum()
        st.metric(label="Valores Perdidos", value="Sí" if missing_values > 0 else "No", border=True)

# Mostrar gráficos
st.header("Mapa de Calor de Correlaciones")
heatmap_fig = plot_heatmap(df)
st.plotly_chart(heatmap_fig)

st.header("Conteo de Valores por Clase")
class_count_fig = plot_class_count(df)
st.plotly_chart(class_count_fig)

st.header("Promedio de Largo Mayor y menor")
# Crear columnas para los gráficos
col1, col2 = st.columns(2)
with col1:
    major_axis_plot= plot_avg_major_axis_length(df)  # Gráfico en la primera columna
    st.plotly_chart(major_axis_plot)
with col2:
    minor_axis_plot= plot_avg_minor_axis_length(df)  # Gráfico en la segunda columna
    st.plotly_chart(minor_axis_plot)

# Gráfico de dispersión interactivo
st.header("Gráfico de Dispersión Interactivo")
x_column = st.selectbox("Selecciona la columna X:", df.columns)
y_column = st.selectbox("Selecciona la columna Y:", df.columns)

scatter_fig = plot_scatter(df, x_column, y_column)
st.plotly_chart(scatter_fig)