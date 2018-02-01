from flask import Flask
from flask import request
from flask_mail import Mail
import json
from send_mail import send_mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required
import pymysql

app = Flask(__name__)

app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = False

db = SQLAlchemy()
pymysql.install_as_MySQLdb()
db.init_app(app)

mail = Mail(app)

login_manger = LoginManager()
login_manger.init_app(app)


@login_manger.user_loader
def load_user(user_id):
    from Users import Users
    return Users.query.get(int(user_id))



def init():
    from auth import auth
    app.register_blueprint(blueprint=auth, url_prefix='/auth')


if __name__ == '__main__':
    init()
    app.run(threaded=True)
