from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from apirestfull_curso.src.models import Role, db
from apirestfull_curso.src.utils import requires_roles

app = Blueprint("role", __name__, url_prefix="/roles")


@app.route("/created", methods=["POST"])
@jwt_required()
@requires_roles("Admin")
def _create_role_():
    data = request.json
    role = Role(
        name=data["name"],
    )
    db.session.add(role)
    db.session.commit()

    return {"message": "Role created!"}, HTTPStatus.CREATED


@app.route("/list", methods=["GET"])
@jwt_required()
@requires_roles("Admin", "Normal")
def _list_roles_():
    query = db.select(Role)
    roles = db.session.execute(query).scalars().all()
    return [
        {
            "id": role.id,
            "name": role.name,
            "user": [user.username for user in role.users],
        }
        for role in roles
    ]


@app.route("/get/<int:role_id>", methods=["GET"])
@jwt_required()
@requires_roles("Admin", "Normal")
def _get_by_id_(role_id):
    role = db.get_or_404(Role, role_id)
    return {
        "id": role.id,
        "name": role.name,
        "users": [{"id": user.id, "username": user.username} for user in role.users],
    }


@app.route("/delete/<int:role_id>", methods=["DELETE"])
@jwt_required()
@requires_roles("Admin")
def delete_role(role_id):
    role = db.get_or_404(Role, role_id)
    db.session.delete(role)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT
