import os

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
            'logs.log',
            'geckodriver.log',
        ]
        
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)

if __name__ == '__main__':
    LetsCleanIt.CleanAll()