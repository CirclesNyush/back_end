from flask import request, jsonify, url_for
from back_end import db
from models.Users import Users
from models.Circle import Circle
from circles import circles
from sqlalchemy import desc
import random
import base64


@circles.route('/querycirclesbyid', methods=['POST'])
def query_circles_by_id():
    if request.method == 'POST':
        data = request.get_json(force=True)

        index = data['eventId']

        circles = Circle.query.filter_by(id=index).first()

        send = dict(status=0, data=[])
        if circles is not None:
            send['status'] = 1
            user = Users.query.filter_by(id=circles.publisher_id).first()
            cl = dict(title=circles.title, content=circles.content, time=circles.time, imgs=circles.imgs.split(','),
                      location=circles.location,email=user.email,
                          avatar=user.avatar, nickname=user.nickname, event_id=circles.id)
            send['data'].append(cl)
        return jsonify(send)


@circles.route('/querycircles', methods=['POST'])
def query_circles():
    if request.method == 'POST':
        data = request.get_json(force=True)

        index = data['eventId']

        if index < 0:
            circles = Circle.query.order_by(desc(Circle.id)).limit(5).all()
        else:
            circles = Circle.query.order_by(desc(Circle.id)).filter(Circle.id < index).limit(5).all()
            for c in circles:
                print(c.id)
        send = dict(status=0, data=[])
        if circles is not None:
            send['status'] = 1
            for c in circles:
                user = Users.query.filter_by(id=c.publisher_id).first()
                cl = dict(title=c.title, content=c.content, time=c.time, imgs=c.imgs.split(','),
                          avatar=user.avatar, nickname=user.nickname, event_id=c.id)
                send['data'].append(cl)
        return jsonify(send)


@circles.route('/postcircles', methods=['POST'])
def post_circles():
    if request.method == 'POST':
        data = request.get_json(force=True)
        user = Users.query.filter_by(cyphered_email=data['publisher_id']).first()
        if user is not None:
            pics = data['images']
            paths = []
            uid = user.id
            circle = Circle(uid, data['title'], data['content'])
            circle.location = data['location']
            circle.time = data['time']
            db.session.add(circle)
            db.session.commit()
            for i in range(len(pics)):
                img = base64.b64decode(pics[i])
                print(len(img))
                print(circle.id)
                with open("/root/work/back_end/static/pic/" + str(circle.id) + "_" + str(i) + ".jpg", 'wb') as file:
                    file.write(img)
                paths.append(url_for("static", filename="pic/" + str(circle.id) + "_" + str(i) + ".jpg"))
            circle.imgs = ",".join(paths)
            db.session.add(circle)
            db.session.commit()

        return jsonify(status=1)
