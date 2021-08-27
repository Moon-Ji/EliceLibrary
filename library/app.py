from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate




app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://kdt:kdt_password@localhost:3306/library?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "123"

db.init_app(app)
migrate = Migrate(app, db)

from view import user_api, api

app.register_blueprint(api.bp)
app.register_blueprint(user_api.bp)


if __name__ == "__main__":
    app.run(debug=True)
