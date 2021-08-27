from flask import Blueprint, render_template, request, url_for, session, flash
from sqlalchemy.sql.elements import Null
from werkzeug.utils import redirect
from bcrypt import hashpw, checkpw, gensalt
import datetime
import re

bp = Blueprint('main', __name__)

from model.model import *

# 메인 페이지
@bp.route('/')
def home():
    books = Book.query.all()
    return render_template('main.html', books=books)

# 책 정보 페이지
@bp.route('/book_info/<int:book_id>', methods=['GET', 'POST'])
def book_info(book_id):
    if request.method == 'GET':
        book = Book.query.filter_by(id=book_id).first()
        book_reviews = Review.query.filter_by(book_id=book_id).order_by(Review.id.desc()).all()

        return render_template('info.html', book=book, reviews=book_reviews)
        
        
    elif request.method == 'POST':
        utcnow= datetime.datetime.utcnow()
        time_gap= datetime.timedelta(hours=9)
        kor_time= utcnow+ time_gap
        now_str_date = kor_time.strftime('%Y-%m-%d')

        review = Review(
            book_id=book_id, 
            user_id=session['id'], 
            rating=int(request.form['star']), 
            content=request.form['content'], 
            post_date=now_str_date
        )

        if not request.form['star'] or not request.form['content']:
            flash("별점과 댓글을 모두 작성해주세요.")
            return redirect('/book_info/'+ str(book_id))

        db.session.add(review)
        db.session.commit()

        # 리뷰를 작성할 때마다 책 평점을 업데이트(더 좋은 방법이 있을지 고민해보자)
        reviews = Review.query.filter_by(book_id=book_id).all()
        reviews_rating = [review.rating for review in reviews]
        total_rate = sum(reviews_rating)
        avg_rate = total_rate / len(reviews)

        book = Book.query.filter_by(id=book_id).first()
        book.rating = avg_rate

        db.session.commit()

        flash("리뷰가 성공적으로 작성되었습니다.")
        return redirect('/book_info/'+ str(book_id))

# 대여 기록
@bp.route('/rent_log')
def rent_log():
    if 'id' not in session:
        flash("로그인이 필요한 서비스입니다!.")
        return redirect("/login")

    user_id = session['id']
    rental_info = Rental.query.filter_by(user_id=user_id).all()

    books = []
    for info in rental_info:
        book = Book.query.filter_by(id=info.book_id).all()
        books += book
    return render_template("log.html", books=books, rental_info=rental_info, zip=zip)

# 책 대여
@bp.route('/rent_book/<int:book_id>')
def rent_book(book_id):
    book = db.session.query(Book).filter(Book.id == book_id).first()
    
    if 'id' not in session:
        flash("로그인이 필요한 서비스입니다!.")
        return redirect("/login")

    id = session['id']
    rental_book = Rental.query.filter_by(book_id=book_id, user_id=id, end_date=None).all() # 쿼리문으로 values('book_id')

    if rental_book:
        flash("이미 대여한 책입니다.")
        return redirect('/')
    if book.stock < 1:
        flash("재고가 부족합니다.")
        return redirect('/')
    else:
        book.stock -= 1
        utcnow= datetime.datetime.utcnow()
        time_gap= datetime.timedelta(hours=9)
        kor_time= utcnow+ time_gap
        now_str_date = kor_time.strftime('%Y-%m-%d')
        rental_info = Rental(
            book_id=book_id, 
            user_id=session['id'],
            start_date=now_str_date
            )
        db.session.add(rental_info)
        db.session.commit()
        return redirect('/')

# 책 반납하기 페이지(빌린 책 리스트)
@bp.route('/rent_book_list')
def rent_book_list():
    if 'id' not in session:
        flash("로그인이 필요한 서비스입니다!.")
        return redirect("/login")

    user_id = session['id']
    rental_info = Rental.query.filter_by(user_id=user_id).all()

    return render_template("return.html", rental_info=rental_info)

# 책 반납
@bp.route('/return_book/<int:info_id>')
def return_book(info_id):
    info = db.session.query(Rental).filter(Rental.id == info_id).first()
    book = db.session.query(Book).filter(Book.id == info.book_id).first()

    utcnow= datetime.datetime.utcnow()
    time_gap= datetime.timedelta(hours=9)
    kor_time= utcnow+ time_gap
    now_str_date = kor_time.strftime('%Y-%m-%d')

    info.end_date = now_str_date
    book.stock += 1
    db.session.commit()

    return redirect('/rent_book_list')
