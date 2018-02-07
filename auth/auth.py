from flask import request, jsonify
from back_end import db
from models.Users import Users
from auth import auth
from flask_login import login_user, logout_user, login_required

from utli import send_mail


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(force=True)

        user = Users.query.filter_by(email=data['email']).first()

        if user is not None and user.pwd == data['pwd']:
            if not user.is_valid:
                return jsonify(dict(status=0, type=0, is_new=-1))
            else:
                login_user(user)

                user_info = jsonify(dict(status=1, is_new=user.is_new, type=-1))
                return user_info
        else:
            user_info = jsonify(dict(status=0, type=1, is_new=-1))
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

        q = Users.query.filter_by(email=data['email']).first()
        if q is None:
            user = Users(email=data['email'], pwd=data['pwd'], gender=data['gender'])
            db.session.add(user)
            db.session.commit()
            subject = 'verify from circles'
            rec = [data['email']]
            content = 'steins.xin:8001/auth/verify/' + data['email']
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
            content = 'steins.xin:8001/auth/forget/' + data['email']
            send_mail(subject=subject, recv=rec, content=content)
            return jsonify(dict(status=1, type=-1, is_new=-1))
        else:
            return jsonify(dict(status=0, type=-1, is_new=-1))


@auth.route('/verify/<username>', methods=['GET'])
def check(username):
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


# TODO: Website!
@auth.route('/forget/<username>', methods=['GET'])
def get_pwd(username):
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