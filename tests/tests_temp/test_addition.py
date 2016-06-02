import unittest
import time
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app import mail
from flask import current_app, render_template
from flask.ext.mail import Message

from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission, Follow

from document_filder.email_context import *
from app.tool.send_mail import send_email,send_163


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
        app = current_app._get_current_object()
        with mail.record_messages() as outbox:
            msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + '验证你的帐号',
                          sender=app.config['FLASKY_MAIL_SENDER'], recipients=['1074976039@qq.com'])
            print(body)
            print(html)
            msg.body = body
            msg.html = html
            send_163(msg)
            # mail.send_message(subject='testing',
            #                   body='test',
            #                   sender=app.config['FLASKY_MAIL_SENDER'],
            #                   recipients=["jcnlcxc@163.com"])
            self.assertTrue(len(outbox) == 1)
            self.assertTrue(outbox[0].subject == subject)
