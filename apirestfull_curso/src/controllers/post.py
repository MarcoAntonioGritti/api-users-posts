from datetime import datetime
from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect

from apirestfull_curso.src.models.base import db
from apirestfull_curso.src.models.post import Post
from apirestfull_curso.src.models.user import User
from apirestfull_curso.src.utils import requires_roles

app = Blueprint("post", __name__, url_prefix="/posts")


@app.route("/create", methods=["POST"])
@jwt_required()
@requires_roles("Admin")
def create_user():
    data = request.json
    created_date = datetime.fromisoformat(
        data["created"]
    )  # Converte a string created enviada na req,e transforma em datetime
    post = Post(
        title=data["title"],
        body=data["body"],
        created=created_date,
        author_id=data["author_id"],
    )
    db.session.add(post)
    db.session.commit()

    return {"message": "Post created!"}, HTTPStatus.CREATED


@app.route("/list", methods=["GET"])
@jwt_required()
@requires_roles("Admin", "Normal")
def list_post():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    return [
        {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "created": post.created,
            "author_id": post.author_id,
        }
        for post in posts
    ]


@app.route("/get/<int:post_id>", methods=["GET"])
@jwt_required()
@requires_roles("Admin", "Normal")
def _get_id_post_(post_id):
    post = db.get_or_404(Post, post_id)
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created": post.created,
        "author_id": post.author_id,
    }


@app.route("/update/<int:post_id>", methods=["PATCH"])
@jwt_required()
@requires_roles("Admin")
def _update_post_(post_id):
    post = db.get_or_404(Post, post_id)
    data = request.json

    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])

    db.session.commit()

    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created": post.created,
        "author_id": post.author_id,
    }


@app.route("/delete/<int:post_id>", methods=["DELETE"])
@jwt_required()
@requires_roles("Admin")
def _delete_post_(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
