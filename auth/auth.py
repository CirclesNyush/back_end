from flask import request, jsonify
from back_end import db
from models.Users import Users
from auth import auth
from flask_login import login_user, logout_user, login_required

from utli import send_mail

import time


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(force=True)

        user = Users.query.filter_by(email=data['email']).first()

        if user is not None and user.pwd == data['pwd']:
            if not user.is_valid:
                return jsonify(dict(status=0, type=0, is_new=-1, nickname='', avatar=''))
            else:
                login_user(user)
                now = time.time()
                user.timestamp = int(now)
                user_info = jsonify(dict(status=1, is_new=int(user.is_new), type=-1, nickname=user.nickname, avatar=user.avatar))
                return user_info
        else:
            user_info = jsonify(dict(status=0, type=1, is_new=-1, nickname='', avatar=''))
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
        print(data)
        q = Users.query.filter_by(email=data['email']).first()
        print(q)
        if q is None:
            user = Users(email=data['email'], pwd=data['pwd'], gender=data['gender'], nickname=data['nickname'])
            db.session.add(user)
            db.session.commit()
            subject = 'verify from circles'
            rec = [data['email']]
            content = {'url': 'steins.xin:8001/auth/verify/' + user.cyphered_email,
                       'nickname': user.nickname}
            send_mail(subject=subject, recv=rec, content=content)
            return jsonify(dict(status=1, type=-1, is_new=-1))
        else:
            return jsonify(dict(status=0, type=1, is_new=-1))


@auth.route('/forgetpwd', methods=['POST'])
def forget_pwd():
    if request.method == 'POST':
        data = request.get_json(force=True)

        q = Users.query.filter_by(email=data['email']).first()
        if q is not None:
            subject = 'Change your password'
            rec = [data['email']]
            content = {'url': 'steins.xin:8001/auth/forget/' + q.cyphered_email,
                       'nickname': q.nickname}
            send_mail(subject=subject, recv=rec, content=content)
            q.is_forget = True
            db.session.add(q)
            db.session.close()
            return jsonify(dict(status=1, type=-1, is_new=-1))
        else:
            return jsonify(dict(status=0, type=-1, is_new=-1))


@auth.route('/checksession', methods=['POST'])
def check_session():
    if request.method == 'POST':
        data = request.get_json(force=True)

        q = Users.query.filter_by(cyphered_email=data['email']).first()
        if q is not None:
            previous = q.timestamp
            now = time.time()

            interval = now - previous
            print(interval, now, previous, q.timestamp)
            if interval < 604800:
                return jsonify(dict(status=1, avatar=q.avatar, nickname=q.nickname))
            else:
                return jsonify(dict(status=0, avatar='', nickname=''))
        else:
            return jsonify(dict(status=0, avatar='', nickname=''))


@auth.route('/verify/<username>', methods=['GET'])
def check(username):
    user = Users.query.filter_by(cyphered_email=username).first()
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


# TODO: Website!
@auth.route('/forget/<username>', methods=['GET'])
def get_pwd(username):
    user = Users.query.filter_by(email=username).first()
    if user is not None:
        if user.is_valid and user.is_forget:
            return "change"
        return "wrong"
