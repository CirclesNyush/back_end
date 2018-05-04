from flask import request, jsonify, url_for
from back_end import db
from models.Users import Users
from models.Circle import Circle
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
        print(data)
        user = Users.query.filter_by(cyphered_email=email).first()
        if user is not None:
            json = dict(avatar=user.avatar, nickname=user.nickname, email=user.email,
                        phone=user.phone, description=user.description)
            return jsonify(dict(status=1, data=json))
        json = dict(avatar='', nickname='',
                    phone='', tags='')
        return jsonify(dict(status=0, data=json))


@personal.route('/updateinfo', methods=['POST'])
def update_info():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = data['data']
        user = Users.query.filter_by(cyphered_email=data['email']).first()
        if user is not None:
            print(data)
            for key, value in data.items():
                if value != "":
                    if key == 'phone':
                        user.phone = value
                    elif key == 'nickname':
                        user.nickname = value
                    elif key == 'description':
                        user.description = value

            print(user.phone)
            db.session.add(user)
            db.session.commit()
            return jsonify(dict(status=1, data=""))
        return jsonify(diict(status=0, data=""))


@personal.route('/getuserinfo', methods=['POST'])
def get_user_info():
    if request.method == 'POST':
        data = request.get_json(force=True)
        event_id = data['email']
        print(event_id)
        event = Circle.query.filter_by(id=event_id).first()
        if event is not None:
            user = Users.query.filter_by(id=event.publisher_id).first()
            if user is not None:
                json = dict(avatar=user.avatar, nickname=user.nickname, email=user.email,
                        phone=user.phone, description=user.description)
            else:
                json = dict(avatar='', nickname='',
                            phone='', tags='')
            return jsonify(dict(status=1, data=json))
        json = dict(avatar='', nickname='',
                    phone='', tags='')
        return jsonify(dict(status=0, data=json))
