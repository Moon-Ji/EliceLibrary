import csv
from datetime import date, datetime

from app import db
from model.model import Book

session = db.session

with open('library.csv', 'r', encoding='UTF-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        publication_date = datetime.strptime(
			row['publication_date'], '%Y-%m-%d').date()
        image_path = f"static/image/book_img/{row['id']}"
        try:
            open(f'library/{image_path}.png')
            image_path = f"../static/image/book_img/{row['id']}.png"
        except:
            image_path = f"../static/image/book_img/{row['id']}.jpg"


        book = Book(
            id=int(row['id']), 
			book_name=row['book_name'], 
			publisher=row['publisher'],
            author=row['author'], 
			publication_date=publication_date, 
			pages=int(row['pages']),
            isbn=row['isbn'], 
			description=row['description'], 
            link=row['link'],
			image_path=image_path,
            stock=5,
            rating=0
        )
        db.session.add(book)

    db.session.commit()

