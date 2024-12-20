import streamlit as st
import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

# Título de la página
st.title("Predicción con Modelo de Árbol de Decisión")

# Cargar el modelo desde la carpeta 'models'
def load_model():
    model_path = "models\decision_tree_model.pkl"
    try:
        with open(model_path, "rb") as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        st.error("El modelo no se encontró en la carpeta 'models'. Verifica el archivo.")
        return None

model = load_model()

# Subida del archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV para realizar predicciones", type=["csv"])

if uploaded_file is not None and model is not None:
    try:
        # Cargar los datos del CSV
        data = pd.read_csv(uploaded_file)
        st.write("Vista previa del archivo cargado:")
        st.dataframe(data.head())

        # Validar si el archivo tiene los datos necesarios para el modelo
        if 'Class' in data.columns:
            X = data.drop(columns=['Class'])
            y_true = data['target']
        else:
            X = data
            y_true = None

        # Realizar predicciones
        y_pred = model.predict(X)
        st.write("Predicciones:")
        st.dataframe(pd.DataFrame(y_pred, columns=['Predicción']))

        # Calcular métricas si los valores verdaderos están presentes
        if y_true is not None:
            accuracy = accuracy_score(y_true, y_pred)
            f1 = f1_score(y_true, y_pred, average='weighted')
            precision = precision_score(y_true, y_pred, average='weighted')
            recall = recall_score(y_true, y_pred, average='weighted')

            st.write("### Métricas del modelo:")
            st.write(f"- **Accuracy:** {accuracy:.2f}")
            st.write(f"- **F1 Score:** {f1:.2f}")
            st.write(f"- **Precisión:** {precision:.2f}")
            st.write(f"- **Recall:** {recall:.2f}")
        else:
            st.warning("El archivo no contiene una columna 'target'. Solo se mostrarán las predicciones.")
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
