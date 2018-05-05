from back_end import db
import hashlib
from datetime import datetime


class Circle(db.Model):
    __tablename__ = 'Circle'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.VARCHAR(64))
    content = db.Column(db.VARCHAR(140))
    time = db.Column(db.VARCHAR(60))
    location = db.Column(db.VARCHAR(60))

    publisher_id = db.Column(db.Integer)

    follower_id = db.Column(db.VARCHAR(64))

    imgs = db.Column(db.VARCHAR(200))

    def __init__(self, p_id, title, content):
        self.publisher_id = p_id
        self.title = title
        self.content = content
        self.time = ""
        self.location = ""
        self.imgs = ""
        self.follower_id = ""

    def __repr__(self):
        return '<Circles %r>' % self.email

    def get_email(self):
        return self.email
