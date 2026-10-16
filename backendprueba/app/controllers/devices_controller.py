#lo que recibe al SP32 
from flask import jsonify, request
from app.services.readings_service import save_reading

CAMPOS = [
    "sistema",
    "temperatura",
    "humedad_ambiente",
    "humedad_suelo",
    "led_verde_pwm",
    "led_rojo",
    "led_blanco",
    "ventilador",
] #obligatorios 


def insert_reading(): #recibe el post del esp32, lee json 
    data=request.get_json(silent=True) or {}
    faltantes=[campo for campo in CAMPOS if data.get(campo) is None] #junta campos que no llegaron 
    if faltantes:
        return jsonify({"message": "Missing fields: " + ", ".join(faltantes)}), 400

    try:
        item={
            "sistema": str(data["sistema"]),
            "temperatura": float(data["temperatura"]),
            "humedad_ambiente": float(data["humedad_ambiente"]),
            "humedad_suelo": float(data["humedad_suelo"]),
            "led_verde_pwm": int(data["led_verde_pwm"]),
            "led_rojo": int(data["led_rojo"]),
            "led_blanco": int(data["led_blanco"]),
            "ventilador": int(data["ventilador"]),
        }
    except (TypeError, ValueError):
        return jsonify({"message": "los valores del sensor deben ser numeros"}), 400 #si la conversion falla 

    try:
        reading = save_reading(item) #llama funcion del service 
    except Exception as error:
        print("Error al guardar la lectura: ", error)
        return jsonify({"message": "No se pudo guardar la lectura"}), 500

    return jsonify({"message": "Lectura guardada", "id": reading.id}), 201