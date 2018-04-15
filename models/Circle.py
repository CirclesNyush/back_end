from back_end import db
import hashlib
from datetime import datetime


class Circle(db.Model):
    __tablename__ = 'Circle'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.VARCHAR(64))
    content = db.Column(db.VARCHAR(140))
    time = db.Column(db.DateTime)

    publisher_id = db.Column(db.Integer)

    follower_id = db.Column(db.VARCHAR(64))

    def __init__(self, p_id, title, content):
        self.publisher = p_id
        self.title = title
        self.content = content
        self.time = datetime.now()

        self.follower_id = ""

    def __repr__(self):
        return '<Circles %r>' % self.email

    def get_email(self):
        return self.email
