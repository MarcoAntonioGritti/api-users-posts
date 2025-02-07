from functools import wraps
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity

from apirestfull_curso.src.models.base import db
from apirestfull_curso.src.models.user import User


def requires_roles(*role_names):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.get_or_404(User, user_id)

            if user.role.name not in role_names:
                return {"message": "User dont have access."}, HTTPStatus.FORBIDDEN
            return f(*args, **kwargs)

        return wrapped

    return decorator
