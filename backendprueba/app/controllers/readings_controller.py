from flask import jsonify, request
from app.services.readings_service import get_latest_state, get_statistics, get_series


def latest(): #llaman al service 
    return jsonify(get_latest_state()), 200


def statistics():
    return jsonify(get_statistics()), 200


def series():
    raw = request.args.get("minutos", "5") #lee el parametro de la url minutos 
    try:
        minutes = int(raw)
    except ValueError:
        return jsonify({"message": "minutos tiene que ser un entero"}), 400
    if not 1 <= minutes <= 1440:
        return jsonify({"message": "minutos tiene que estar entre 1 y 1440"}), 400
    return jsonify(get_series(minutes)), 200
