#representa cada lectura del invernadero 

from datetime import datetime, timezone
from app.extensions import db


class Reading(db.Model):
    __tablename__ = "readings"
    id = db.Column(db.Integer, primary_key=True)
    sistema = db.Column(db.String(10), nullable=False)  #"on o off""
    temperatura = db.Column(db.Float, nullable=False)
    humedad_ambiente = db.Column(db.Float, nullable=False)
    humedad_suelo = db.Column(db.Float, nullable=False)
    led_verde_pwm = db.Column(db.Integer, nullable=False)  #de 0 a 100
    led_rojo = db.Column(db.Integer, nullable=False)  #0 o 1
    led_blanco = db.Column(db.Integer, nullable=False)  #0 o 1
    ventilador = db.Column(db.Integer, nullable=False)  #0 o 1
    received_at = db.Column(  #la fecha la pone el servidor, no el esp32
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc), #predeterminado cuando no se proporciona uno 
        index=True,  #se filtra por fecha en /api/serie
    )

    def to_dict(self): #transfrofa objeto reading en un diccionario de python 
        return {
            "id": self.id,
            "sistema": self.sistema,
            "temperatura": self.temperatura,
            "humedad_ambiente": self.humedad_ambiente,
            "humedad_suelo": self.humedad_suelo,
            "led_verde_pwm": self.led_verde_pwm,
            "led_rojo": self.led_rojo,
            "led_blanco": self.led_blanco,
            "ventilador": self.ventilador,
            "received_at": self.received_at.isoformat() if self.received_at else None, #si existe la convierte a texto ISO, si no devuelve None (Null en json)
        }