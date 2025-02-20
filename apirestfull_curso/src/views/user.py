from marshmallow import fields

from apirestfull_curso.src.app import ma
from apirestfull_curso.src.models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True  # Incluir as referências de foreign key


class CreateUserSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    role_id = fields.Integer(required=True, strict=True)
