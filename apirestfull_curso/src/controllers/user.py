from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy import inspect

from apirestfull_curso.src.app import bcrypt
from apirestfull_curso.src.models import User, db
from apirestfull_curso.src.utils import requires_roles
from apirestfull_curso.src.views.user import CreateUserSchema, UserSchema

app = Blueprint("user", __name__, url_prefix="/users")


@app.route("/created", methods=["POST"])
@jwt_required()
def create_user():

    try:
        data = CreateUserSchema().load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]),
        role_id=data["role_id"],
    )
    db.session.add(user)
    db.session.commit()

    return {"message": "User created!"}, HTTPStatus.CREATED


@app.route("/list", methods=["GET"])
@jwt_required()
@requires_roles("Admin")
def list_user():

    users = db.session.execute(db.select(User)).scalars()
    return UserSchema(many=True).dump(users), HTTPStatus.OK


@app.route("/get/<int:user_id>", methods=["GET"])
@jwt_required()
@requires_roles("Admin")
def get_user(user_id):

    user = db.get_or_404(User, user_id)
    return UserSchema().dump(user), HTTPStatus.OK


@app.route("/update/<int:user_id>", methods=["PATCH"])
@jwt_required()
@requires_roles("Admin")
def update_user(user_id):

    user = db.get_or_404(User, user_id)
    data = request.json

    for column in inspect(User).attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])

    db.session.commit()
    return UserSchema().dump(user), HTTPStatus.OK


@app.route("/delete/<int:user_id>", methods=["DELETE"])
@jwt_required()
@requires_roles("Admin")
def delete_user(user_id):

    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
