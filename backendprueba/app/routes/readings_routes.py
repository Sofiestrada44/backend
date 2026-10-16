from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.readings_controller import latest, statistics, series

readings_bp=Blueprint("readings", __name__)

@readings_bp.route("/ultima", methods=["GET"])
@jwt_required()
def latest_route(): #estado mas reciente 
    return latest()


@readings_bp.route("/estadisticas", methods=["GET"])
@jwt_required()
def statistics_route():
    return statistics()


@readings_bp.route("/serie", methods=["GET"])
@jwt_required() #proteccion de rutas 
def series_route():
    return series()
