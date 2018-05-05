from flask import Flask, request, jsonify, send_from_directory
from flask_mail import Mail
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pymysql
from utli import getData

app = Flask(__name__)

app.config.from_object(config['development'])

# scheduler = APScheduler()
# scheduler.init_app(app)


db = SQLAlchemy()
pymysql.install_as_MySQLdb()
db.init_app(app)

mail = Mail(app)

login_manger = LoginManager()
login_manger.init_app(app)


@login_manger.user_loader
def load_user(user_id):
    from models.Users import Users
    return Users.query.get(int(user_id))


def init():
    from auth import auth
    from personal import personal
    from circles import circles
    app.register_blueprint(blueprint=auth, url_prefix='/auth')
    app.register_blueprint(blueprint=personal, url_prefix='/personal')
    app.register_blueprint(blueprint=circles, url_prefix='/circles')


@app.route('/news', methods=['POST'])
def news():
    if request.method == 'POST':
        return jsonify(getData())


@app.route('/test', methods=["GET"])
def test():
    # return app.send_static_file('pic/33a5cbb6a9a0e88b4a6adcb73f6ad025.ipg')
    return send_from_directory('/root/work/back_end/static/pic', "33a5cbb6a9a0e88b4a6adcb73f6ad025.jpg", as_attachment=True)



if __name__ == '__main__':
    init()
    # scheduler.start()
    app.run(threaded=True,
            debug=True,
            host='0.0.0.0',
            port=8001
            )
