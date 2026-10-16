from flask import Flask 
from config import Config
from app.extensions import db, migrate, jwt, cors
from app.routes.auth_routes import auth_bp
from app.routes.devices_routes import devices_bp
from app.routes.readings_routes import readings_bp

#auth registro e inicio de sesion
#devices recepcion de las mediciones 
#readings consulta de estado, estadisticas. 

def create_app():
    app = Flask(__name__) #crea app Flask
    app.config.from_object(Config) #carga configuracion de config 
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)  #el frontend manda el header authorization ---> necesita cors para que no lo bloquee el navegador

    from app import models  #importar los modelos para que las migraciones los vean

    app.register_blueprint(auth_bp, url_prefix="/auth")  #/auth/register, /auth/login
    app.register_blueprint(devices_bp, url_prefix="/devices")  #/devices/insert (esp32, sin token)
    app.register_blueprint(readings_bp, url_prefix="/api")  #/api/ultima, /api/estadisticas, /api/serie (con token)
    return app

#Una ruta define una dirección y el método HTTP que atiende. Un Blueprint agrupa varias rutas relacionadas para organizarlas y registrarlas en la aplicación.