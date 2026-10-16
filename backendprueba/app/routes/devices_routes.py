from flask import Blueprint
from app.controllers.devices_controller import insert_reading

devices_bp=Blueprint("devices", __name__) #blueprint llamado devices 

@devices_bp.route("/insert", methods=["POST"])
def insert_route(): #Define la función que Flask ejecuta cuando llega una petición válida a esa ruta.
    return insert_reading()
