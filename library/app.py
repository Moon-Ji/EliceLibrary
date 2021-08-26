from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@localhost:3306/library"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
db.init_app(app)

app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "123"

from view import api, user_api

app.register_blueprint(api.bp)
app.register_blueprint(user_api.bp)

if __name__ == "__main__":
    app.run(debug=True)
