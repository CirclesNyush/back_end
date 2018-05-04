from flask import request, jsonify
from back_end import db
from models.Users import Users
from models.Circle import Circle
from circles import circles
from sqlalchemy import desc


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
                cl = dict(title=c.title, content=c.content, time=c.time,
                          avatar=user.avatar, nickname=user.nickname, event_id=c.id)
                send['data'].append(cl)
        return jsonify(send)


@circles.route('/postcircles', methods=['POST'])
def post_circles():
    if request.method == 'POST':
        data = request.get_json(force=True)
        user = Users.query.filter_by(cyphered_email=data['publisher_id']).first()
        if user is not None:
            uid = user.id
            circle = Circle(uid, data['title'], data['content'])
            db.session.add(circle)
            db.session.commit()

        return jsonify(status=1)
