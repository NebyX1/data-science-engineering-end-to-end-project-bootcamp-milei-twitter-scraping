#Importamos dependencias
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

#Cargamos el contenido del archivo .env(variables de entorno)
load_dotenv()

#Aquí importamos dentro de nuevas variables los datos del archivo .env que nos permitirán inciar Chrome con nuestra cuenta de usuario y perfil
firefox_driver = os.environ['FIREFOX_DRIVER']
profile_path = os.environ['PROFILE_PATH']

# Datos de conexión
user = os.environ['DB_USER']
password = os.environ['DB_PASS']
host = os.environ['DB_HOST']
database = os.environ['DB_DATABASE']

# Crear el engine de SQL Alchemy
engine = create_engine(f"postgresql://{user}:{password}@{host}/{database}")  