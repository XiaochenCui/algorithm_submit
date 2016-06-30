import socket
import unittest
import time
from datetime import datetime

from flask.ext.login import current_user
from sqlalchemy.exc import IntegrityError
from app import mail
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

        msg = Message(host_ip, recipients=[new_email])
        msg.body = '测试_body'
        msg.html = '测试_html'

        # with app.app_context():
        #     send_163(msg)

        self.send_email_test(new_email, host_ip, template, user=user, token=token)

    def send_email_test(self, to, subject, template, **kwargs):
        app = current_app._get_current_object()
        msg = Message('[Flasky]' + subject,
                      sender='Flasky Admin <flasky@example.com>', recipients=[to])
        # msg.body = render_template(template + '.txt', **kwargs)
        # msg.html = render_template(template + '.html', **kwargs)

        # msg = Message(subject, recipients=[to])
        msg.body = '测试1_body'
        msg.html = '测试1_html'
        with app.app_context():
            send_163(msg)
