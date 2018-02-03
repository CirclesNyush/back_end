from flask_mail import Message
from threading import Thread
from flask import current_app, render_template


class SendMailThread(Thread):
    def __init__(self, app, msg):
        super(SendMailThread, self).__init__()
        self.__app = app
        self.__msg = msg

    def send_asyc_mail(self, app, msg):
        with app.app_context():
            from back_end import mail
            mail.send(msg)

    def run(self):
        self.send_asyc_mail(self.__app, self.__msg)


def send_mail(subject, recv, content):
    msg = Message(subject, sender='nyucircles@163.com', recipients=recv)
    msg.body = content
    print('sending!')
    app = current_app._get_current_object()

    send = SendMailThread(app, msg)
    send.start()