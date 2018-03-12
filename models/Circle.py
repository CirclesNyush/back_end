from back_end import db
import hashlib


class Users(db.Model):
    __tablename__ = 'Circles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.VARCHAR(64))
    content = db.Column(db.VARCHAR(140))
    time = db.Column(db.DateTime, default=datetime.now())
    is_valid = db.Column(db.BOOLEAN(), default=True)
    tags = db.Column(db.PickleType)

    publisher = db.Column(db.VARCHAR(64))
    follower = db.Column(db.VARCHAR(140))

    def __init__(self, email, title, content, tags):
        self.publisher = email
        self.title = title
        self.content = content
        self.tags = tags

    def __repr__(self):
        return '<Circles %r>' % self.email

    def get_email(self):
        return self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
