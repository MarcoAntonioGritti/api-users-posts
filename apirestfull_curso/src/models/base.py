from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()


class Base(db.Model):  # Permite que outros modelos herdem essa base
    __abstract__ = True
