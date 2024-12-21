import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder
import pickle


try:
    @st.cache_data
    def load_data():
        # Cargar los datos de entrenamiento desde el archivo predefinido
        data = pd.read_csv("data/Dry_Bean_Dataset.csv")
        st.write("Vista previa del conjunto de datos cargado desde el archivo local:")
        st.dataframe(data.head())
        return data

    train_data = load_data()

    # Comprobar que el archivo tiene la columna 'Class'
    if 'Class' not in train_data.columns:
        st.error("El archivo debe contener una columna 'Class' para realizar el entrenamiento.")
    else:
        # Preprocesar la columna target (etiquetas) usando LabelEncoder
        label_encoder = LabelEncoder()
        train_data['label'] = label_encoder.fit_transform(train_data['Class'])

        # Separar características y etiqueta
        X = train_data.drop(columns=['Class', 'label'])
        y = train_data['label']

        # Dividir en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Entrenar un modelo de árbol de decisión
        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)

        # Guardar el modelo entrenado
        model_path = "models/decision_tree_model.pkl"
        with open(model_path, "wb") as file:
            pickle.dump(model, file)

        # Realizar predicciones en el conjunto de prueba
        y_pred = model.predict(X_test)

        # Calcular métricas relevantes
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')

        # Mostrar métricas utilizando st.metric
        st.markdown("<h2 style='color:blue;'>Métricas del Modelo Entrenado</h2>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Accuracy", f"{accuracy:.2f}", border= True)
        col2.metric("F1 Score", f"{f1:.2f}", border= True)
        col3.metric("Precisión", f"{precision:.2f}", border= True)
        col4.metric("Recall", f"{recall:.2f}", border=True)

except FileNotFoundError:
    st.error(f"El archivo {csv_path} no se encontró. Verifica que exista en el folder especificado.")
except Exception as e:
    st.error(f"Ocurrió un error al procesar el archivo de entrenamiento: {e}")

# Sección para realizar predicciones
st.markdown("<h2 style='color:blue;'>Realizar predicciones</h2>", unsafe_allow_html=True)
prediction_file = st.file_uploader("Sube un archivo CSV para realizar predicciones", type=["csv"])

if prediction_file is not None and model is not None:
    try:
        # Cargar los datos del CSV de predicciones
        prediction_data = pd.read_csv(prediction_file)
        st.write("Vista previa del archivo cargado para predicciones:")
        st.dataframe(prediction_data.head())

        # Validar si 'Class' está presente y eliminarla
        if 'Class' in prediction_data.columns:
            st.warning("La columna 'Class' será ignorada para las predicciones.")
            prediction_data = prediction_data.drop(columns=['Class'])

        # Validar si las columnas coinciden con las del modelo
        expected_features = model.feature_names_in_
        if not all(feature in prediction_data.columns for feature in expected_features):
            missing_features = set(expected_features) - set(prediction_data.columns)
            st.error(f"El archivo de predicciones no contiene las siguientes columnas esperadas: {missing_features}")
        else:
            # Realizar predicciones
            y_pred = model.predict(prediction_data)

            # Convertir predicciones numéricas a clases originales
            y_pred_original = label_encoder.inverse_transform(y_pred)

            st.write("Predicciones realizadas exitosamente:")
            st.dataframe(pd.DataFrame({
                'Predicción (Numérica)': y_pred,
                'Predicción (Clase)': y_pred_original
            }))

            # Si el archivo contiene la columna 'Class', calcular métricas
            if 'Class' in prediction_data.columns:
                y_true = label_encoder.transform(prediction_data['Class'])
                accuracy = accuracy_score(y_true, y_pred)
                f1 = f1_score(y_true, y_pred, average='weighted')
                precision = precision_score(y_true, y_pred, average='weighted')
                recall = recall_score(y_true, y_pred, average='weighted')

                st.write("### Métricas del modelo en las predicciones:")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Accuracy", f"{accuracy:.2f}")
                col2.metric("F1 Score", f"{f1:.2f}")
                col3.metric("Precisión", f"{precision:.2f}")
                col4.metric("Recall", f"{recall:.2f}")
            else:
                st.warning("El archivo no contiene una columna 'Class'. Solo se mostrarán las predicciones.")
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo de predicción: {e}")

