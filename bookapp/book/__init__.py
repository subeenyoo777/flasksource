# __init__.py : 해당 디렉토리가 패키지의 일부임을 알려주는 역할
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    from .views import main_views, book_views, auth_views

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # 블루 프린트 등록
    # 블루 프린트 등록함
    app.register_blueprint(main_views.bp)
    app.register_blueprint(book_views.bp)
    app.register_blueprint(auth_views.bp)
    return app
