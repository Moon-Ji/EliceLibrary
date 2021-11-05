import csv
from datetime import datetime
from model.model import Book

from app import create_app, db
app = create_app()
app.app_context().push()

with app.app_context():
    with open('library.csv', 'r', encoding='UTF-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            publication_date = datetime.strptime(
                row['publication_date'], '%Y-%m-%d').date()
            image_path = f"static/image/book_img/{row['id']}"
            try:
                open(f'{image_path}.png')
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

