from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()  #conector de base de datos por objetos python y consultas ORM
migrate = Migrate()  #migraciones crean/modifican las tablas
jwt = JWTManager()  #autenticacion con tokens
cors = CORS()  #permite que el frontend (otro puerto/equipo) llame a la api
