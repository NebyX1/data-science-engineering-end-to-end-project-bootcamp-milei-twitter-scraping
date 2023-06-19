# Importar las librerías y dependencias
import pandas as pd
from pycaret.anomaly import *
import matplotlib.pyplot as plt

def detect_anomalies():
    # Leer los datos
    df = pd.read_csv('dataset/time_series_hate_speech.csv', sep=';', parse_dates=['date'], dayfirst=True)

    # Reemplazar la coma por un punto y convertir el porcentaje a un número decimal
    df['hate_tweets'] = df['hate_tweets'].str.replace(',', '.').str.rstrip('%').astype('float') / 100.0

    # Configurar el análisis de la serie de tiempo
    s = setup(df, session_id=123)

    # Entrenar un modelo de detección de anomalías.
    model = create_model('iforest', fraction=0.05)

    # Asignar etiquetas de anomalías al conjunto de datos
    df_with_anomalies = assign_model(model)

    # Verificar las etiquetas asignadas
    print(df_with_anomalies)

    # Crear un gráfico
    plt.figure(figsize=(12,6))

    # Dibujar los datos originales
    plt.plot(df.index, df['hate_tweets'], label='Datos originales')

    # Dibujar las anomalías
    anomalies = df_with_anomalies[df_with_anomalies['Anomaly'] == 1]
    plt.scatter(anomalies.index, anomalies['hate_tweets'], color='red', label='Anomalías')

    plt.legend()

    # Guardar la gráfica como un archivo PNG
    plt.savefig('anomalies.png')