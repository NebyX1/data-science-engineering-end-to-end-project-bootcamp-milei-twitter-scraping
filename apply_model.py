def model_to_tweets():
    # Importar las librerías y dependencias
    from pycaret.classification import load_model, predict_model
    import pandas as pd
    import pickle

    # Cargamos el modelo
    modelo = load_model('hate_tweets_model')

    # Cargamos el vectorizador
    vectorizer = pickle.load(open("tfidf_vectorizer.pkl", 'rb'))

    # Cargar el archivo csv a un dataframe
    df = pd.read_csv("tweets_with_sentiment.csv")

    # Crear una nueva columna 'tweet_category' y la inicializamos con 'normal_tweet'
    df['tweet_category'] = 'normal_tweet'

    # Transformar y predecir cada tweet
    for index, row in df.iterrows():
        # Transformamos el tweet al mismo formato que los datos de entrenamiento
        tweet_transformado = vectorizer.transform([row['tweet_english']])
        df_tfidf = pd.DataFrame(tweet_transformado.toarray(), columns=vectorizer.get_feature_names_out())

        # Predecimos la categoría a la que pertenece el tweet
        prediccion = predict_model(modelo, data=df_tfidf)

        # Verificar si 'Label' está en las columnas del dataframe de predicción
        if 'Label' in prediccion.columns:
            # Si la predicción es 0 o 1, etiquetamos el tweet como 'hate_comment'
            if prediccion.iloc[0]['Label'] in [0, 1]:
                df.at[index, 'tweet_category'] = 'hate_comment'
        else:
            # Aquí puedes manejar el caso cuando 'Label' no está en las columnas
            # Por ejemplo, puedes imprimir las columnas para depurar
            print("Columnas del dataframe de predicción: ", prediccion.columns)

    # Guardar el DataFrame resultante en un archivo csv
    df.to_csv("tweets_with_categories.csv", index=False)