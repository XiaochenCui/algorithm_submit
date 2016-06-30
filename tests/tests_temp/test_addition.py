import unittest
import time
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app import mail
from flask import current_app, render_template
from flask.ext.mail import Message

from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission, Follow

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
        recipient_addr = ['jcnlcxc@163.com']
        subject = 'Żółta kartka'
        text = "Wiadomość testowa"
        html = """
                <html>
                <head>
                <meta http-equiv="content-type" content="text/html;charset=utf-8" />
                </head>
                <body>
                <font face="verdana" size=2>{}<br/></font>
                <img src="cid:image0" border=0 />
                </body>
                </html>
                """.format(text)  # template

        msg = Message(subject=subject, )
        msg.body = text
        msg.html = html

        send_163(msg,
                 recipient_addr=recipient_addr,
                 fn='my.eml',
                 save=True)