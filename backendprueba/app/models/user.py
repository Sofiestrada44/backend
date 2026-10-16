#representa cada usuario que puede iniciar sesion 

from datetime import datetime, timezone
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    identification = db.Column(db.String(50), nullable=False, unique=True)
    phone_number = db.Column(db.String(40), nullable=True, unique=True)
    full_name = db.Column(db.String(200), nullable=False)  #no puede ser nulo
    email = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)  #inactivar sin eliminar
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    update_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
