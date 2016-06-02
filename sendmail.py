import unittest
import time
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app import mail
from flask import current_app, render_template
from flask.ext.mail import Message
from email.mime.text import MIMEText

from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission, Follow

from document_filder.email_context import *


def send_mail():
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + '123',
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=['1074976039@qq.com'])

    print(body)
    # print(html)
    body1 = body
    text = "Wiadomość testowa"
    msg.body = MIMEText(text.encode('utf-8'), 'plain', 'utf-8')
    msg.html = '123'
    with app.app_context():
        mail.send(msg)

app = create_app('default')
send_mail()
# app.run()
