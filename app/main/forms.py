from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, \
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(Form):
    name = StringField('正文:', validators=[Required()])
    submit = SubmitField('提交')


class EditProfileForm(Form):
    name = StringField('姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用')


class PostForm(Form):
    body = PageDownField("正文:", validators=[Required()])
    submit = SubmitField('提交')


class ThemeForm(Form):
    title = StringField('课题名称:', validators=[Required()])
    body = TextAreaField("课题内容:", validators=[Required()])
    submit = SubmitField('提交')


class ColumnTitleForm(Form):
    title = StringField('', validators=[Required()])
    id = StringField('', validators=[Required()])
    submit = SubmitField('保存')


class ColumnAddForm(Form):
    title = StringField('', validators=[Required()])
    submit = SubmitField('保存')
