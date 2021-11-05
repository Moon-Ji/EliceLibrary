from flask import Flask
from flask_migrate import Migrate

from db_connect import db
import config

def create_app():
    app = Flask(__name__)

    app.config.from_object(config)
    db.init_app(app)
    migrate = Migrate(app, db)

    from view import user_api, api

    app.register_blueprint(api.bp)
    app.register_blueprint(user_api.bp)

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
