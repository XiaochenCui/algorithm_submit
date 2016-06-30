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
from app.email import send_email


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
        username = 'cxc_test'
        password = '123'
        user = User(email=new_email,
                    username=username,
                    password=password)
        token = user.generate_confirmation_token()
        send_email(user.email, '验证你的帐号',
                   'auth/email/confirm', user=user, token=token)