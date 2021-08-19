from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from model.model import *
from bcrypt import hashpw, checkpw, gensalt
from datetime import datetime

app = Flask(__name__)

# database 설정파일
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://user:password@localhost:3306/library"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.secret_key = "123"

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
        book_reviews = Review.query.filter_by(book_id=book_id).all()

        return render_template('info.html', book=book, reviews=book_reviews)
        
    elif request.method == 'POST':
        user_id = session['id']
        rating = int(request.form['star'])
        content = request.form['review']

        review = Review(
            id=2,
            book_id=book_id, 
            user_id=user_id, 
            rating=rating, 
            content=content, 
            post_date=datetime.now()
        )
        db.session(review)
        db.session.commit()
        flash("리뷰가 성공적으로 작성되었습니다.")
        return redirect('/book_info/<int:book_id>')


# 회원가입
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")

    elif request.method == 'POST':
        user = User.query.filter_by(id=request.form['id']).first()
        if not user:
            name = request.form['name']
            id = request.form['id']
            password = request.form['password']
            check_password = request.form['check_password']

            if password != check_password:
                return "비밀번호가 일치하지 않습니다."

            else:
                pw_hash = hashpw(password.encode('utf-8'), gensalt())
                user = User(
                    id=id,
                    password=pw_hash,
                    name=name
                )
                db.session.add(user)
                db.session.commit()
                
            return redirect('/')
        else:
            return "이미 가입된 아이디입니다."


# 로그인
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password'].encode("utf-8")

        user_data = User.query.filter_by(id=id).first()

        if not user_data:
            return "없는 아이디입니다."
        elif not checkpw(password, user_data.password.encode("utf-8")):
            return "비밀번호가 일치하지 않습니다."
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

