from flask import request, jsonify, url_for
from back_end import db
from models.Users import Users
from personal import personal
import base64
import os


@personal.route('/fetchavatar', methods=['POST'])
def get_avatar():
    if request.method == 'POST':
        data = request.get_json(force=True)
        email = data['email']
        user = Users.query.filter_by(cyphered_email=email).first()
        if user is not None:
            return send_from_directory('/root/work/back_end/static/pic', email + '.jpg', as_attachment=True)
        else:
            return jsonify(dict(status=0, avatar=""))


@personal.route('/updateavatar', methods=['POST'])
def upadte_avatar():
    if request.method == 'POST':
        data = request.get_json(force=True)
        email = data['email']
        user = Users.query.filter_by(cyphered_email=email).first()
        print(email)
        if user is not None:
            img = base64.b64decode(data['avatar'])
            print(len(img))
            with open("/root/work/back_end/static/pic/" + email + ".jpg", 'wb') as file:
                file.write(img)
            user.avatar = url_for("static", filename="pic/" + email + '.jpg')
            print(user.avatar)
            db.session.add(user)
            db.session.commit()
            print("yesy")
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
def update_info():
    if request.method == 'POST':
        data = request.get_json(force=True)
        email = data['email']
        user = Users.query.filter_by(cyphered_emai=email).first()
        if user is not None:
            changes = data['data']
            for key, value in changes.items():
                user[key] = value
            db.session.add(user)
            db.session.commit()
            return jsonify(dict(status=0, data=""))
        return jsonify(dict(status=0, data=""))
