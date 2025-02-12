from http import HTTPStatus

from apirestfull_curso.src.models.base import db
from apirestfull_curso.src.models.role import Role
from apirestfull_curso.src.models.user import User


def test_created_token_success(client):
    role = db.session.execute(db.select(Role).where(Role.name == "Admin")).scalar()
    role_id = role.id
    user = User(username="marcola", password="123", role_id=role_id)
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login", json={"username": user.username, "password": user.password}
    )

    user = db.session.execute(
        db.select(User).where(User.username == user.username)
    ).scalar()

    if not user or user.password != user.password:
        return {"message": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = response.json["access_token"]

    assert response.json == {"access_token": access_token}
