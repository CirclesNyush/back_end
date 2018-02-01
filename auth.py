from flask import request, Blueprint, redirect, url_for, jsonify
from back_end import login_manger, db
from Users import Users
import json
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required

from send_mail import send_mail

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(force=True)
        print(data)

        user = Users.query.filter_by(email=data['email']).first()
        if user is not None and user.pwd == data['pwd']:
            if not user.is_valid:
                return jsonify(dict(status=0, type=0))
            else:
                login_user(user)

                user_info = jsonify(dict(status=1, is_new=user.is_new))
                return user_info
        else:
            user_info = jsonify(dict(status=0, type=1))
            return user_info
    else:
        return 'hello'


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({
        'status': 1
    })


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json(force=True)
        user = Users(email=data['email'], pwd=data['pwd'], gender=data['gender'])
        db.session.add(user)
        db.session.commit()
        subject = 'verify from circles'
        rec = [data['email']]
        content = '127.0.0.1:5000/auth/verify/' + data['email']
        send_mail(subject=subject, recv=rec, content=content)
        return jsonify(dict(end=1))


@auth.route('/verify/<username>', methods=['GET'])
def check(username):
    print(username)
    user = Users.query.filter_by(email=username).first()
    if user is not None:
        if not user.is_valid:
            user.is_valid = True
            db.session.add(user)
            db.session.commit()
            return 'cong! U have activate this email'
        else:
            return 'you have done this already'
    else:
        return 'please check the link if it is right'
