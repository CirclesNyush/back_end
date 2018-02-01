from back_end import db
from back_end import login_manger
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.VARCHAR(64))
    pwd = db.Column(db.VARCHAR(64))
    is_new = db.Column(db.BOOLEAN())
    gender = db.Column(db.BOOLEAN())
    is_valid = db.Column(db.BOOLEAN(), default=False)

    def __init__(self, email, pwd, gender):
        self.email = email
        self.pwd = pwd
        self.is_new = True
        self.gender = gender

    def __repr__(self):
        return '<Users %r>' % self.email

    def get_email(self):
        return self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
