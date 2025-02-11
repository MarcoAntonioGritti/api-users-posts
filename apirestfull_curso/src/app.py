import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from apirestfull_curso.src.models.base import db

# instances
migrate = Migrate()
jwt = JWTManager()

load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "super-secret"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)  # Garante a criação das pastas
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # import models
    from apirestfull_curso.src.models.user import User
    from apirestfull_curso.src.models.role import Role
    from apirestfull_curso.src.models.post import Post

    # Cria o application context para operações com o banco de dados
    with app.app_context():
        # Cria todas as tabelas (caso não existam)
        db.create_all()

        # Importa os modelos necessários para a seed
        from apirestfull_curso.src.models.user import User
        from apirestfull_curso.src.models.role import Role
        from apirestfull_curso.src.models.post import Post

    # register blueprints
    from apirestfull_curso.src.controllers import auth, post, role, user

    app.register_blueprint(user.app)
    app.register_blueprint(post.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    return app


# comando para inicializar a aplicação - poetry run flask --app src.app run --debug
