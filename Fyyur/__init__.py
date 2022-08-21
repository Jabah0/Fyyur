from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_migrate import Migrate

db = SQLAlchemy()
def create_app():
    controllers = Flask(__name__)
    moment = Moment(controllers)
    controllers.config.from_pyfile('config.py')
    db.init_app(controllers)
    migrate = Migrate(controllers, db)
    from .controllers import apps
    
    controllers.register_blueprint(apps, url_prefix='/')
    return controllers