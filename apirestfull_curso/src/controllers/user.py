from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect

from apirestfull_curso.src.models.base import db
from apirestfull_curso.src.models.user import User
from apirestfull_curso.src.utils import requires_roles

app = Blueprint("user", __name__, url_prefix="/users")


@app.route("/created", methods=["POST"])
@jwt_required()
@requires_roles("Admin")
def create_user():
    data = request.json
    user = User(
        username=data["username"],
        password=data["password"],
        role_id=data["role_id"],
    )
    db.session.add(user)
    db.session.commit()

    return {"message": "User created!"}, HTTPStatus.CREATED


@app.route("/list", methods=["GET"])
@jwt_required()
@requires_roles("Admin", "Normal")
def list_user():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "role": {
                "id": user.role.id,
                "name": user.role.name,
            },
        }
        for user in users
    ]


@app.route("/get/<int:user_id>", methods=["GET"])
@jwt_required()
@requires_roles("Admin", "Normal")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username,
        "password": user.password,
        "role": {
            "id": user.role.id,
            "name": user.role.name,
        },
    }


@app.route("/update/<int:user_id>", methods=["PATCH"])
@jwt_required()
@requires_roles("Admin")
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])

    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
        "password": user.password,
        "role_id": user.role_id,
    }


@app.route("/delete/<int:user_id>", methods=["DELETE"])
@jwt_required()
@requires_roles("Admin")
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
