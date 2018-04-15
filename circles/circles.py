from flask import request, jsonify
from back_end import db
from models.Users import Users
from models.Circle import Circle
from circles import circles

@circles.route('/querycircles', methods=['POST'])
def query_circles():
    if request.method == 'POST':
        data = request.get_json(force=True)

        index = data['eventId']

        circles = Circle.query.filter(Circle.id > index).limit(10).all()
        send = dict(status=0, data=[])
        if circles is not None:
            send['status'] = 1
            for c in circles:
                user = Users.query.filter_by(id=c.publisher_id).first()
                print(c.publisher_id)
                cl = dict(title=c.title, content=c.content, time=c.time,
                          avatar=user.avatar, nickname=user.nickname)
                send['data'].append(cl)
        return jsonify(send)


@circles.route('/postcircles', methods=['POST'])
def post_circles():
    if request.method == 'POST':
        data = request.get_json(force=True)
        user = Users.query.filter_by(cyphered_email=data['publisher_id']).first()
        print(user.id, user.email)
        if user is not None:
            uid = user.id
            print(uid)

            circle = Circle(uid, data['title'], data['content'])
            db.session.add(circle)
            db.session.commit()

        return jsonify(status=1)
