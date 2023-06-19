def analyze_sentiment():
    # Importamos las dependencias
    import pandas as pd
    from textblob import TextBlob

    # Esta función utiliza TextBlob para analizar el sentimiento del tweet de entrada,
    # determina el sentimiento y la polaridad, y los devuelve
    def get_sentiment(tweet_english):
        try:
            blob = TextBlob(tweet_english)
            sentiment = blob.sentiment.polarity
            # Clasificamos el sentimiento
            if sentiment < 0.0:
                sentiment_class = 'NEGATIVE'
            elif sentiment > 0.0:
                sentiment_class = 'POSITIVE'
            else:
                sentiment_class = 'NEUTRAL'
            return sentiment_class, sentiment
        except Exception as e:
            print(f"Error: {e}")
            return None, None

    # Aquí importamos el archivo csv a usar y lo guardamos en un dataframe
    df = pd.read_csv("translated_tweets.csv")

    # Esto elimina cualquier fila del DataFrame donde 'tweet_english' esté vacío o solo contenga espacios en blanco.
    df = df[df['tweet_english'].str.strip() != ""]

    # Esto convoca a la función "get_sentiment", la cual agregará dos nuevas columnas a nuestro dataframe, las mismas son "sentiment" y "polarity",
    # que contienen el resultado del análisis llevado a cabo por TextBlob, pasará tweet por tweet
    df['sentiment'], df['polarity'] = zip(*df['tweet_english'].apply(get_sentiment))

    # Guardamos en un csv lo resultante del análisis de sentimientos
    df.to_csv("tweets_with_sentiment.csv", index=False)