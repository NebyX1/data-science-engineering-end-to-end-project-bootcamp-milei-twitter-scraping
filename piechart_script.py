def create_piechart():
    # Importamos las dependencias
    import pandas as pd
    import matplotlib.pyplot as plt
    from config import engine
    from sqlalchemy.orm import sessionmaker

    engine = engine

    # Intentamos leer desde la base de datos, la tabla "tabla_1"
    try:
        with engine.connect() as connection:
            df = pd.read_sql_table('tabla_1', connection)
    except Exception as e:
        print('Ocurrió un error al intentar conectar o leer la base de datos:')
        print(str(e))
        return

    # Va recorrer la columna "sentiment" de nuestro dataframe y sumará la cantidad de veces que se repite cada valor disponible(negative, positive y neutral)
    sentiment_counts = df['sentiment'].value_counts()

    # Le indicamos a matplotlib las características con las que debe crear nuestro piechart
    plt.figure(figsize=(10, 5))
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%')
    plt.title('Sentiment Analysis Pie Chart')

    # Guardamos en la carpeta raíz del proyecto el piechart generado en formato png
    plt.savefig("piechart.png")

    # Esto sirve para mostrar en pantalla el piechart generado, por defecto está deshabilitado
    # plt.show()






