from flask import request, jsonify
from back_end import db
from models.Users import Users
from personal import personal
from flask_login import logout_user, login_required

@login_required
@personal.route('/fetchavatar/<username>', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'hello'