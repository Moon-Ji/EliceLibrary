from typing_extensions import ParamSpecArgs
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import Authorization

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.String(50), primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)

class Book(db.Model):
    __tablename__ = "Book"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    book_name = db.Column(db.String(255), nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publication_date = db.Column(db.String(), nullable=False)
    pages = db.Column(db.Integer)
    isbn = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String())
    link = db.Column(db.String(255))
    image_path = db.Column(db.String(255))
    stock = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer)
    