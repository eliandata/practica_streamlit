import pandas as pd
import plotly.express as px

def plot_heatmap(df):
    """Genera un heatmap de las correlaciones en el DataFrame."""
    correlation_matrix = df.loc[:, df.columns != 'Class'].corr()
    fig = px.imshow(
        correlation_matrix,
        text_auto=True,
        color_continuous_scale='Viridis',
        labels=dict(color="Correlación")
    )
    return fig

def plot_class_count(df):
    """Genera un gráfico de barras con el conteo de valores por clase."""
    beans_count = df['Class'].value_counts()
    fig = px.bar(
        beans_count,
        x=beans_count.index,
        y=beans_count.values,
        labels={'x': 'Beans', 'y': 'Count'},
        color=beans_count.values,
        color_continuous_scale='Viridis'
    )
    return fig

def plot_avg_major_axis_length(df):
    """Genera un gráfico de barras del promedio del largo mayor por clase."""
    avg_length = df.groupby('Class', as_index=False)['MajorAxisLength'].mean()
    fig = px.bar(
        avg_length,
        x='Class',
        y='MajorAxisLength',
        labels={'MajorAxisLength': 'Promedio del Largo mayor', 'Class': 'Clase'},
        color='MajorAxisLength',
        color_continuous_scale='Viridis'
    )
    return fig

def plot_avg_minor_axis_length(df):
    """Genera un gráfico de barras del promedio del largo mayor por clase."""
    avg_length = df.groupby('Class', as_index=False)['MinorAxisLength'].mean()
    fig = px.bar(
        avg_length,
        x='Class',
        y='MinorAxisLength',
        labels={'MinorAxisLength': 'Promedio del Largo menor', 'Class': 'Clase'},
        color='MinorAxisLength',
        color_continuous_scale='Viridis'
    )
    return fig

def plot_scatter(df, class_column, x_column, y_column):
    """Genera un gráfico de dispersión basado en las selecciones del usuario."""
    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        color='Class',
        labels={'x': x_column, 'y': y_column, 'color': 'Clases'},
        title="Gráfico de Dispersión"
    )
    return fig
