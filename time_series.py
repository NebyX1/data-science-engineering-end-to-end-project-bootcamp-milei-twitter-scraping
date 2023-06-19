# Importar las librerías y dependencias
import pandas as pd
from pycaret.time_series import *
import matplotlib.pyplot as plt

def create_time_series():
    # Leer los datos
    df = pd.read_csv('dataset/time_series_hate_speech.csv', sep=';', parse_dates=['date'], dayfirst=True)

    # Reemplazar la coma por un punto y convertir el porcentaje a un número decimal
    df['hate_tweets'] = df['hate_tweets'].str.replace(',', '.').str.rstrip('%').astype('float') / 100.0

    # Configurar el análisis de la serie de tiempo
    s = setup(data=df['hate_tweets'], target='hate_tweets', fh=7, fold=3, session_id=123)

    # Entrenar y comparar varios modelos
    best_model = compare_models()

    # Hacer predicciones para los próximos 7 días
    future_predictions = predict_model(best_model, fh=7)

    # Ajustar el índice de las predicciones para que comience después de los datos existentes
    future_predictions.index = pd.RangeIndex(start=df.index.max() + 1, stop=df.index.max() + 1 + len(future_predictions))

    # Imprimir las predicciones
    print(future_predictions)

    # Crear un gráfico
    plt.figure(figsize=(12,6))

    # Dibujar los datos originales
    plt.plot(df.index, df['hate_tweets'], label='Datos originales')

    # Dibujar las predicciones
    plt.plot(future_predictions.index, future_predictions['y_pred'], label='Predicciones')

    plt.legend()
    plt.savefig("time_series.png")  # Guardar el gráfico en un archivo
    plt.close()  # Cerrar el gráfico