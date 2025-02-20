from marshmallow import fields

from apirestfull_curso.src.app import ma
from apirestfull_curso.src.models import Post


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True


class CreatePostSchema(ma.Schema):
    title = fields.String(required=True)
    body = fields.String(required=True)
    created = fields.DateTime(required=True)
    author_id = fields.Integer(required=True, strict=True)
