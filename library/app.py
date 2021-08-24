from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://user:password@localhost:3306/library"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
db.init_app(app)

app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "123"

from view import api
app.register_blueprint(api.bp)

if __name__ == "__main__":
    app.run(debug=True)
