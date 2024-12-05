SQLALCHEMY_DATABASE_URI = "postgresql://swen_ii_db_user:Lh6vGGX0fiSg7uoWVDlWhQGD3oBPFEqV@dpg-ct3r1jl2ng1s73a07qtg-a.oregon-postgres.render.com/swen_ii_db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"


class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False