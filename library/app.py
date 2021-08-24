from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy

from bcrypt import hashpw, checkpw, gensalt
from datetime import datetime

import re

app = Flask(__name__)

# database 설정파일
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://user:password@localhost:3306/library"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
db.init_app(app)

app.secret_key = "123"
app.config["SECRET_KEY"] = "ABCD"

from model.model import *

# 유저 데이터 확인하는 임시 페이지
@app.route('/user')
def home():
    users = User.query.all()
    return render_template('db.html', users=users)

# 메인 페이지
@app.route('/')
def main():
    books = Book.query.all()
    return render_template('main.html', books=books)

# 책 정보 페이지
@app.route('/book_info/<int:book_id>', methods=['GET', 'POST'])
def book_info(book_id):
    if request.method == 'GET':
        book = Book.query.filter_by(id=book_id).first()
        book_reviews = Review.query.filter_by(book_id=book_id).order_by(Review.id.desc()).all()

        return render_template('info.html', book=book, reviews=book_reviews)
        
    elif request.method == 'POST':

        review = Review(
            book_id=book_id, 
            user_id=session['id'], 
            rating=int(request.form['star']), 
            content=request.form['content'], 
            post_date=datetime.now()
        )

        db.session.add(review)
        db.session.commit()

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
@app.route('/rent_log')
def rent_log():
    user_id = session['id']
    rental_info = RentalInfo.query.filter_by(user_id=user_id).all()

    books = []
    for info in rental_info:
        book = Book.query.filter_by(id=info.book_id).all()
        books += book
    return render_template("log.html", books=books, rental_info=rental_info, zip=zip)

# 책 대여
@app.route('/rent_book/<int:book_id>')
def rent_book(book_id):
    book = db.session.query(Book).filter(Book.id == book_id).first()
    
    if book.stock < 1:
        return "재고가 부족합니다."
    else:
        book.stock -= 1

        rental_info = RentalInfo(
            book_id=book_id, 
            user_id=session['id'],
            start_date=datetime.now()
            )
        db.session.add(rental_info)
        db.session.commit()
        return redirect('/')

# 책 반납하기 페이지(빌린 책 리스트)
@app.route('/rent_book_list')
def rent_book_list():
    user_id = session['id']
    rental_info = RentalInfo.query.filter_by(user_id=user_id).all()

    books = []
    for info in rental_info:
        book = Book.query.filter_by(id=info.book_id).all()
        books += book
    return render_template("return.html", books=books, rental_info=rental_info, zip=zip)

# 책 반납
@app.route('/return_book/<int:book_id>/<int:info_id>')
def return_book(book_id, info_id):
    info = db.session.query(RentalInfo).filter(RentalInfo.id == info_id).first()
    book = db.session.query(Book).filter(Book.id == book_id).first()

    info.end_date = datetime.now()
    book.stock += 1

    db.session.commit()

    return redirect('/rent_book_list')

# 회원가입
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")

    elif request.method == 'POST':
        user = User.query.filter_by(id=request.form['id']).first()

        name = request.form['name']
        id = request.form['id']
        password = request.form['password']
        check_password = request.form['check_password']

        p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        q = re.compile('^(?=.*[a-zA-z])(?=.*[0-9])(?=.*[$`~!@$!%*#^?&\\(\\)\-_=+]).{8,16}$')

        if not p.match(id):
            flash("올바른 이메일을 입력하세요.")
            return render_template("signup.html")

        elif not q.match(password):
            flash("비밀번호는 영어, 숫자, 특수문자를 포함한 8자 이상의 단어로 입력해주세요.")
            return render_template("signup.html")

        elif user:
            flash("이미 가입된 아이디입니다.")
            return render_template("signup.html")

        elif not name or not id or not password or not check_password:
            flash("모든 입력창을 채우세요.")
            return render_template("signup.html")

        elif password != check_password:
            flash("비밀번호가 일치하지 않습니다.")
            return render_template("signup.html")

        elif len(password) < 8:
            flash("비밀번호를 8자리 이상 입력하세요.")
            return render_template("signup.html")

        else:
            pw_hash = hashpw(password.encode('utf-8'), gensalt())
            user = User(
                id=id,
                password=pw_hash,
                name=name
            )
            db.session.add(user)
            db.session.commit()
                
        flash("가입을 축하드립니다.")
        return render_template("main.html")

# 로그인
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password'].encode("utf-8")

        user_data = User.query.filter_by(id=id).first()

        if not id or not password:
            flash("모든 입력창을 채우세요.")
            return render_template('login.html')
        elif not user_data:
            flash("존재하지 않는 아이디입니다.")
            return render_template('login.html')
        elif not checkpw(password, user_data.password.encode("utf-8")):
            flash("아이디와 비밀번호가 일치하지 않습니다.")
            return render_template('login.html')
        else:
            session.clear()
            session['id'] = id 
            return redirect('/')

    elif request.method == 'GET':
        return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

