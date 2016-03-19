import unittest
import time
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask.ext import mail

from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission, Follow

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
        with mail.record_messages() as outbox:
            mail.send_message(subject='testing',
                      body='test',
                      recipients="jcnlcxc@163.com")
            assert len(outbox) == 1
            assert outbox[0].subject == "testing"