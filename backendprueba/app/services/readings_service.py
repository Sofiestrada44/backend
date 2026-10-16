from datetime import datetime, timedelta, timezone
from sqlalchemy import select, func
from app.extensions import db
from app.models.reading import Reading


ESTADO_APAGADO = {
    "sistema": "OFF",
    "temperatura": 0,
    "humedad_ambiente": 0,
    "humedad_suelo": 0,
    "led_verde_pwm": 0,
    "led_rojo": 0,
    "led_blanco": 0,
    "ventilador": 0,
    "ultima_lectura": None,
}

OFFLINE_SECONDS=30 #si pasan estos segundos sin recibir datos del esp32, se considera apagado

def save_reading(data): #guarda una lectura validada
    reading = Reading(**data) #desempaqueta diccionario como argumentos 
    try:
        db.session.add(reading)
        db.session.commit()
    except Exception:
        db.session.rollback()  # deja la sesion limpia si algo falla
        raise #vuelve a lanzar el error 
    return reading


def get_latest_state(): #ultima lectura, si es muy vieja, el esp32  esta apagado
    reading = db.session.execute(
        select(Reading).order_by(Reading.received_at.desc(), Reading.id.desc()).limit(1) #pide la lectura mas reciente 
    ).scalar_one_or_none()

    if reading is None:
        return dict(ESTADO_APAGADO) #si no hay ninguna devuelve estado apagado 

    edad = datetime.now(timezone.utc) - reading.received_at
    if edad > timedelta(seconds=OFFLINE_SECONDS): #si es mayor a 30 devuelve estado apagado 
        return dict(ESTADO_APAGADO)

    return {
        "sistema": reading.sistema,
        "temperatura": reading.temperatura,
        "humedad_ambiente": reading.humedad_ambiente,
        "humedad_suelo": reading.humedad_suelo,
        "led_verde_pwm": reading.led_verde_pwm,
        "led_rojo": reading.led_rojo,
        "led_blanco": reading.led_blanco,
        "ventilador": reading.ventilador,
        "ultima_lectura": reading.received_at.isoformat(),
    }


def get_statistics(): #total, max y min de cada sensor. una sola consulta al sql 
    row = db.session.execute(
        select(
            func.count(Reading.id),
            func.max(Reading.temperatura),
            func.min(Reading.temperatura),
            func.max(Reading.humedad_ambiente),
            func.min(Reading.humedad_ambiente),
            func.max(Reading.humedad_suelo),
            func.min(Reading.humedad_suelo),
        )
    ).one() #exactamente una fila 

    #sin datos, max/min vienen como none(null en json) y el frontend debe mostrar un "--" yo no sabia esto se lo pregunte a claud
    return {
        "total": row[0],
        "temperatura": {"max": row[1], "min": row[2]},
        "humedad_ambiente": {"max": row[3], "min": row[4]},
        "humedad_suelo": {"max": row[5], "min": row[6]},
    }


def get_series(minutes):
    desde = datetime.now(timezone.utc) - timedelta(minutes=minutes) #lecturas de los ultimos minutos, de la mas antigua a la mas reciente
    readings = (
        db.session.execute(
            select(Reading).where(Reading.received_at >= desde).order_by(Reading.received_at.asc())
        )
        .scalars()
        .all()
    )
    return [
        {
            "ts": r.received_at.isoformat(),
            "temperatura": r.temperatura,
            "humedad_ambiente": r.humedad_ambiente,
            "humedad_suelo": r.humedad_suelo,
        }
        for r in readings
    ]