import os

from dotenv import load_dotenv
from flask import Flask, json
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

from apirestfull_curso.src.models import Role, User, db

# instances
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()


def create_admin_user():
    # Verifique se a role Admin já existe
    admin_role = Role.query.filter_by(name="Admin").first()
    if not admin_role:
        # Crie a role Admin se não existir
        admin_role = Role(name="Admin")
        db.session.add(admin_role)
        db.session.commit()

    # Verifique se o usuário Admin já existe
    admin_user = User.query.filter_by(username="admin").first()
    if not admin_user:
        # Crie o usuário Admin
        admin_user = User(username="admin", password="123", role_id=admin_role.id)
        db.session.add(admin_user)
        db.session.commit()


def create_app(environment=os.environ["ENVIRONMENT"]):
    load_dotenv()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"apirestfull_curso.src.config.{environment.title()}Config")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)  # Garante a criação das pastas
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    # import models
    from apirestfull_curso.src.models import Post, Role, User

    # Cria o application context para operações com o banco de dados
    with app.app_context():
        # Cria todas as tabelas (caso não existam)
        db.create_all()

        # Cria o usuário admin com a role 'Admin'
        create_admin_user()

    # register blueprints
    from apirestfull_curso.src.controllers import auth, post, role, user

    app.register_blueprint(user.app)
    app.register_blueprint(post.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    return app
