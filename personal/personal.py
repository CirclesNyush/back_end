from flask import request, jsonify
from back_end import db
from models.Users import Users
from personal import personal
from flask_login import logout_user, login_required


@personal.route('/fetchavatar/', methods=['POST'])
@login_required
def get_avatar():
    if request.method == 'POST':
        data = request.get_json(force=True)
        email = data['email']
        user = Users.query.filter_by(cyphered_email=email).first()
        if user is not None:
            return jsonify(dict(status=1, avatar=user.avatar))
        else:
            return jsonify(dict(status=0, avatar=""))


@personal.route('/updateavatar/', methods=['POST'])
def upadte_avatar():
    if request.method == 'POST':
        data = request.get_json(force=True)
        email = data['email']
        user = Users.query.filter_by(cyphered_email=email).first()
        if user is not None:
            user.avatar = data['avatar'] #TODO : load avatar locally
            db.session.add(user)
            db.session.close()
            return jsonify(dict(status=1, avatar=user.avatar))
        else:
            return jsonify(dict(status=0, avatar=""))


@personal.route('/getinfo', methods=['POST'])
def get_info():
    if request.method == 'POST':
        data = request.get_json(force=True)
        email = data['email']
        user = Users.query.filter_by(cyphered_emai=email).first()
        if user is not None:
            json = dict(avatar=user.avatar, nickname=user.nickname,
                        phone=user.phone, tags=user.tags)
            return jsonify(dict(status=1, data=jsonify(json)))
        return jsonify(dict(status=0, data=""))


@personal.route('/updateinfo', methods=['POST'])
def get_info():
    if request.method == 'POST':
        data = request.get_json(force=True)
        email = data['email']
        user = Users.query.filter_by(cyphered_emai=email).first()
        if user is not None:
            changes = data['data']
            for key, value in changes.items():
                user[key] = value
            return jsonify(dict(status=0, data=""))
        return jsonify(dict(status=0, data=""))