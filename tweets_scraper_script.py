def extract_tweets():
    # Importamos las dependencias
    from selenium import webdriver
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import NoSuchElementException
    import csv
    import time
    import config

    # Acá creamos las variables con las rutas de nuestro perfil de usuario y la dirección de dónde se encuentra el driver de Firefox
    webdriver_service = Service(config.firefox_driver)
    profile_path = config.profile_path

    # Acá le indicamos la forma en la que debe ejecutar Selenium a Firefox, 
    # le indicamos que debe ejecutarse con nuestro perfil de usuario
    firefox_options = Options()
    firefox_options.add_argument(f"-profile {profile_path}")
    firefox_options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe" # Asegúrate que esta ruta es correcta

    # Acá le indicamos que debe de usar Firefox como navegador
    driver = webdriver.Firefox(service=webdriver_service, options=firefox_options)

    # Aquí le indicamos el link que contiene las palabras claves, locación geográfica y fecha de los tweets que debe scrapear
    url = "https://twitter.com/search?q=(milei%20presidente)%20near%3AArgentina%20until%3A2023-06-16%20since%3A2023-06-10&src=typed_query&f=top"

    #Acá vamos a realizar la tarea de scraping de tweets como tal dentro de un bloque try/except para el manejo de errores
    try:
        driver.get(url)
        time.sleep(5)
        old_tweets_count = 0
        same_count = 0

        #Le indicamos a Selenium donde debe guardar, en qué formato y con qué estructura, los tweets raspados.
        with open('scrapped_tweets.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Autor", "Fecha", "Comentario"])

            #Acá le indicamos que mientras se cumpla la condición "true" debe de seguir haciendo scraping y scrolling para obtener más tweets
            #por defecto es un bucle infinito
            while True:
                ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
                #Esto indica que debe esperar 1 segundo antes de hacer el siguiente scrolling para darle tiempo a twitter de cargar nuevos tweets
                time.sleep(1)
                
                #Acá le indicamos que cada tweet es guardado dentro de un elemento html "article"
                tweets = driver.find_elements(By.XPATH, '//article')
                
                #Cada vez que se realice una iteración nueva, es decir, un scroll down, comparará los tweets anteriores con los nuevos
                #en caso de que sean iguales a los obtenidos anteriormente sumará un 1, de lo contrario reiniciará el contador a 0
                if len(tweets) == old_tweets_count:
                    same_count += 1
                else:
                    same_count = 0
                
                #Cuando se alcanza el número de 5 en el contador o se han obtenido 100 tweets, se rompe el bucle while y termina el scraping
                if same_count > 5 or len(tweets) >= 120:
                    break
                old_tweets_count = len(tweets)
                
                #Este bucle de tipo for recorrerá cada tweet del conjunto de tweets obtenidos en cada scroll down
                for tweet in tweets:

                    #Esto intenta extraer información de cada tweet. Busca el nombre del autor, la fecha y el texto del tweet utilizando XPaths específicos.
                    #Luego, escribe esta información en el archivo csv que definimos anteriormente
                    try:
                        author = tweet.find_element(By.XPATH, './/span[contains(@class, "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0")]').text
                        date = tweet.find_element(By.XPATH, './/time').get_attribute('datetime')
                        comment = tweet.find_element(By.XPATH, './/div[contains(@data-testid, "tweetText")]').text.replace('\n', ' ')
                        writer.writerow([author, date, comment])
                    except NoSuchElementException:
                        pass
    except Exception as e:
        print(f"Error:  {str(e)}")
    finally:
        #Al finalizar todo el proceso, le indicamos que debe cerrar Chrome
        driver.quit()