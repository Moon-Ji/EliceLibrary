from flask import Blueprint, render_template, request, session, flash
from werkzeug.utils import redirect
from bcrypt import hashpw, checkpw, gensalt
import re

bp = Blueprint('user', __name__)

from model.model import *

# 회원가입
@bp.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")

    elif request.method == 'POST':
        user = User.query.filter_by(id=request.form['id']).first()

        name = request.form['name']
        id = request.form['id']
        password = request.form['password']
        check_password = request.form['check_password']

        id_check = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        pw_check = re.compile('^(?=.*[a-zA-z])(?=.*[0-9])(?=.*[$`~!@$!%*#^?&\\(\\)\-_=+]).{8,16}$')

        if not id_check.match(id):
            flash("올바른 이메일을 입력하세요.")
            return render_template("signup.html")

        elif not pw_check.match(password):
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
        return redirect('/')

# 로그인
@bp.route("/login", methods=['GET', 'POST'])
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

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")