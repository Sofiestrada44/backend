import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") #busca variable del entorno DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") #Carga la clave secreta que utilizará Flask-JWT-Extended para firmar los tokens JWT.

#Es el archivo que centraliza la configuración de la aplicación. Carga las variables de entorno y define la URL de conexión a PostgreSQL, la opción de seguimiento de SQLAlchemy y la clave secreta utilizada para JWT.