import os


class Config:
    TESTNG = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///bank.sqlite"
    JWT_SECRET_KEY = "super-secret"


class TestingConfig(Config):
    TESTNG = True
    SECRET_KEY = "test"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    JWT_SECRET_KEY = "test"
