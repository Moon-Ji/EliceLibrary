from app import db
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.String(50), primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)

class Book(db.Model):
    __tablename__ = "Book"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
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

    rentals = db.relationship('Rental',backref='Book')
    
class Review(db.Model):
    __tablename__ = 'Review'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    book_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer)
    content = db.Column(db.Text())
    post_date = db.Column(db.String(50))

class Rental(db.Model):
    __tablename__ = 'Rental'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.String(50), nullable=False)
    end_date = db.Column(db.String(50))

    book_id = db.Column(db.Integer, db.ForeignKey('Book.id'), nullable=False)