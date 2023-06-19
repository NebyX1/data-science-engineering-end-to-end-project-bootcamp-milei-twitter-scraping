# Importamos las dependencias
import os
import luigi
import webbrowser
from app import app

# Importamos los componentes(funciones)
from tweets_scraper_script import extract_tweets
from clean_tweets_script import clean_tweets
from translate_tweets_script import trans_tweets
from sentiment_analytics import analyze_sentiment
from apply_model import model_to_tweets
from save_to_database_script import save_database
from wordcloud_script import create_wordcloud
from piechart_script import create_piechart
from time_series import create_time_series
from anomaly_detection import detect_anomalies

# Creamos una clase que se encargue de eliminar todos los archivos en caso de que existan.
class LetsCleanIt:
    @staticmethod
    def CleanAll():
        files_to_remove = [
            'scrapped_tweets.csv',
            'cleaned_tweets.csv',
            'translated_tweets.csv',
            'tweets_with_sentiment.csv',
            'tweets_with_categories.csv',
            'databaseOK.txt',
            'wordcloud.png',
            'piechart.png',
            'time_series.png',
            'anomalies.png',
        ]
        
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)

# Ahora definimos las tareas de Luigi

class ExtractTweets(luigi.Task):
    def run(self):
        extract_tweets()

    def complete(self):
        return os.path.exists('scrapped_tweets.csv')


class CleanTweets(luigi.Task):
    def requires(self):
        return ExtractTweets()

    def run(self):
        clean_tweets()

    def complete(self):
        return os.path.exists('cleaned_tweets.csv')


class TranslateTweets(luigi.Task):
    def requires(self):
        return CleanTweets()

    def run(self):
        trans_tweets()

    def complete(self):
        return os.path.exists('translated_tweets.csv')


class AnalyzeSentiment(luigi.Task):
    def requires(self):
        return TranslateTweets()

    def run(self):
        analyze_sentiment()

    def complete(self):
        return os.path.exists('tweets_with_sentiment.csv')


class ApplyModel(luigi.Task):
    def requires(self):
        return AnalyzeSentiment()

    def run(self):
        model_to_tweets()

    def complete(self):
        return os.path.exists('tweets_with_categories.csv')


class SaveDatabase(luigi.Task):
    def requires(self):
        return ApplyModel()

    def run(self):
        save_database()

    def complete(self):
        return os.path.exists('databaseOK.txt')
    
class GenerateWordcloud(luigi.Task):
    def requires(self):
        return SaveDatabase()

    def run(self):
        create_wordcloud()

    def complete(self):
        return os.path.exists('wordcloud.png')

class GeneratePiechart(luigi.Task):  # Creamos una nueva tarea para generar el piechart
    def requires(self):
        return GenerateWordcloud()  # Esta tarea requiere que la tarea GenerateWordcloud se haya completado

    def run(self):
        create_piechart()  # Ejecutamos la función create_piechart

    def complete(self):
        return os.path.exists('piechart.png')  # La tarea se completa cuando el archivo piechart.png existe


class GenerateTimeSeries(luigi.Task):
    def requires(self):
        return GeneratePiechart()

    def run(self):
        create_time_series()

    def complete(self):
        return os.path.exists('time_series.png')


class DetectAnomalies(luigi.Task):
    def requires(self):
        return GenerateTimeSeries()

    def run(self):
        detect_anomalies()

    def complete(self):
        return os.path.exists('anomalies.png')

# Tarea final para ejecutar la aplicación Flask
class RunApp(luigi.Task):
    def requires(self):
        return DetectAnomalies()

    def run(self):
        webbrowser.open("http://localhost:5000")
        app.run()


if __name__ == '__main__':
    # Primero ejecutamos la función de eliminar todos los archivos en caso de existir
    LetsCleanIt.CleanAll()
    # Ejecutamos las tareas de Luigi
    luigi.run(main_task_cls=RunApp)  # Ahora la tarea final es RunApp