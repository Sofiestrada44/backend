from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.services.auth_service import register_user, validate_credentials


def register():
    data = request.get_json(silent=True) or {} #devuelve none si el cuerpo json no es valido, diccionario vacio 
    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    identification = data.get("identification")

    if not full_name or not email or not password or not identification:
        return jsonify({
            "message": "full_name, email, password and identification are required"
        }), 400  #solicitud mal hecha

    try:
        user = register_user(
            full_name=full_name,
            email=email,
            password=password,
            identification=identification,
        )
        return jsonify({
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "identification": user.identification,
        }), 201  # creado
    except ValueError as error:
        return jsonify({"message": str(error)}), 409  #conflicto ---> ya existe


def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400 #falta alguno 

    user = validate_credentials(email=email, password=password)
    if user is None:
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {"id": user.id, "full_name": user.full_name, "email": user.email},
    }), 200
