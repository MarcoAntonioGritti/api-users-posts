import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from apirestfull_curso.src.models.base import db
from apirestfull_curso.src.models.user import User
from apirestfull_curso.src.models.role import Role
from datetime import datetime

# instances
migrate = Migrate()
jwt = JWTManager()


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


def create_app(test_config=None):
    load_dotenv()

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

        # Cria o usuário admin com a role 'Admin'
        create_admin_user()

    # register blueprints
    from apirestfull_curso.src.controllers import auth, post, role, user

    app.register_blueprint(user.app)
    app.register_blueprint(post.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    return app
