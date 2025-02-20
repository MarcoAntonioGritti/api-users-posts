from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy import inspect

from apirestfull_curso.src.models import Post, db
from apirestfull_curso.src.utils import requires_roles
from apirestfull_curso.src.views.post import CreatePostSchema, PostSchema

app = Blueprint("post", __name__, url_prefix="/posts")


@app.route("/create", methods=["POST"])
@jwt_required()
def create_post():

    post_schema = CreatePostSchema()

    try:
        data = post_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_CONTENT

    post = Post(
        title=data["title"],
        body=data["body"],
        created=data["created"],
        author_id=data["author_id"],
    )
    db.session.add(post)
    db.session.commit()

    return {"message": "Post created!"}, HTTPStatus.CREATED


@app.route("/list", methods=["GET"])
@jwt_required()
@requires_roles("Admin")
def list_post():

    posts = db.session.execute(db.select(Post)).scalars()
    return PostSchema(many=True).dump(posts)


@app.route("/get/<int:post_id>", methods=["GET"])
@jwt_required()
@requires_roles("Admin")
def get_post(post_id):

    post = db.get_or_404(Post, post_id)
    return PostSchema().dump(post)


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

    return PostSchema().dump(post)


@app.route("/delete/<int:post_id>", methods=["DELETE"])
@jwt_required()
@requires_roles("Admin")
def delete_post(post_id):

    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
