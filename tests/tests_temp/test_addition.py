import socket
import unittest
from flask import current_app, render_template
from flask.ext.mail import Message

from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission, Follow

from app.tool.send_mail import send_163


class AdditionModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.config['SERVER_NAME'] = 'flasky_server'
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_mail_send(self):
        new_email = '1074976039@qq.com'
        app = current_app._get_current_object()
        host_ip = socket.gethostbyname(socket.gethostname())
        template = 'auth/email/confirm'
        username = 'cxc_test'
        password = '123'
        user = User(email=new_email,
                    username=username,
                    password=password)
        token = user.generate_confirmation_token()

        self.send_email_test(new_email, host_ip, template, user=user, token=token)

    def send_email_test(self, to, subject, template, **kwargs):
        app = current_app._get_current_object()
        sender = app.config['FLASKY_MAIL_SENDER']

        msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                      sender=sender, recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)

        with app.app_context():
            send_163(msg)
