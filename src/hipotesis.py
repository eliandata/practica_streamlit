# hip.py
import plotly.express as px

# Hipótesis 1
def hipotesis_1(data):
    # Gráfico 1: Promedio de Area por Clase (Gráfico de Barras)
    avg_length = data.groupby('Class', as_index=False)['Area'].mean()
    fig_bar = px.bar(
        avg_length,
        x='Class',
        y='Area',
        labels={'Area': 'Promedio área por clase', 'Class': 'Clase'},
        color='Area',
        color_continuous_scale='Viridis',
        title="Promedio de Área por Clase"
    )

    # Gráfico 2: Gráfico de Caja por Clase
    fig_box = px.box(
        data,
        x="Class",   # Valores únicos de la columna Class en el eje X
        y="Area",    # Valores de la columna Area en el eje Y
        color="Class",  # Diferentes colores para cada clase
        points="all",   # Mostrar todos los puntos en el gráfico
        title="Distribución de Área por Clase"
    )

    return fig_bar, fig_box

# Hipótesis 2 (Ejemplo)
def hipotesis_2(data):
    # Crear el scatter plot
    fig_scatter = px.scatter(
        data,
        x="Compactness",
        y="AspectRation",
        color="Class",  # Diferenciar por clase
        title="Relación entre Compactness y Aspect Ratio por clase",
        labels={'Compactness': 'Compactness', 'AspectRation': 'Aspect Ratio'},
        symbol="Class"  # Opcional, símbolos para diferenciar
    )

    #calcular coeficiente de relacion para cada clase
    # Calcular la correlación entre Compactness y Aspect_Ration para cada valor de 'Class'
    correlation_data = data.groupby('Class').apply(
        lambda group: group['Compactness'].corr(group['AspectRation'])
    ).reset_index(name='Correlation')

    # Crear el gráfico de barras
    fig_corr = px.bar(
        correlation_data,
        x='Class',
        y='Correlation',
        color='Class',
        title="Correlación entre Compactness y Aspect Ratio por Clase",
        labels={'Correlation': 'Correlación'},
        text='Correlation'  # Muestra el valor de la correlación sobre las barras
    )

    return fig_scatter, fig_corr
