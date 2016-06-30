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

from app.tool.send_mail import send_email,send_163
from app.email import send_email_test


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
        msg = Message(host_ip, recipients=[new_email])
        msg.body = '测试_body'
        msg.html = '测试_html'
        with app.app_context():
            send_163(msg)