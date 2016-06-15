from flask import redirect, url_for, flash, current_app
from flask.ext.login import current_user
from flask.ext.admin.contrib import sqla
import flask_admin as admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from flask_admin.base import MenuLink, Admin, BaseView, expose
from flask_admin import form

from app import file_path
from app.models import *


class AdminModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_app.config['PRODUCTION']:
            return True
        else:
            return current_user.is_administrator

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            if current_user.is_administrator:
                return super(MyAdminIndexView, self).index()
            # 如果用户不是管理员，返回首页
            else:
                flash('你没有管理员权限')
                return redirect(url_for('main.index'))
        # 如果用户未登录，返回登录页面
        else:
            flash('请登录')
            return redirect(url_for('auth.login', next=request.url))


class UserView(AdminModelView):
    # 不可见的列
    column_exclude_list = ['password_hash', 'member_since', 'last_seen',
                           'avatar_hash',]

    # inline model
    inline_models = (Post, Theme)


class ThemeView(AdminModelView):
    # 不可见的列
    column_exclude_list = ['timestamp']
    # inline model
    inline_models = (Post,)
    # inline 编辑
    column_editable_list = ['title']


class ArticleColumnView(AdminModelView):
    # inline model
    inline_models = (Article,)
    # inline 编辑
    column_editable_list = ['title']


class FileView(AdminModelView):
    # Override form field to use Flask-Admin FileUploadField
    form_overrides = {
        'path': form.FileUploadField
    }

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        'path': {
            'label': 'File',
            'base_path': file_path,
            'allow_overwrite': False
        }
    }


class FileColumnView(AdminModelView):
    # inline model
    inline_models = (File,)
    # inline 编辑
    column_editable_list = ['title']


class MyAdminIndexView(admin.AdminIndexView):

    def __init__(self):
        super().__init__()

    @expose('/')
    def index(self):
        if not current_app.config['PRODUCTION']:
            return super(MyAdminIndexView, self).index()
        else:
            if current_user.is_authenticated:
                if current_user.is_administrator:
                    return super(MyAdminIndexView, self).index()
                # 如果用户不是管理员，返回首页
                else:
                    flash('你没有管理员权限')
                    return redirect(url_for('main.index'))
            # 如果用户未登录，返回登录页面
            else:
                flash('请登录')
                return redirect(url_for('auth.login', next=request.url))


admin = admin.Admin(name='Admin', index_view=MyAdminIndexView(), template_mode='bootstrap3',)

# 增加主页链接
admin.add_link(MenuLink(name='Back Home', url='/'))

admin.add_view(AdminModelView(Role, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(AdminModelView(Follow, db.session))
admin.add_view(AdminModelView(Post, db.session))
admin.add_view(ThemeView(Theme, db.session))
admin.add_view(AdminModelView(Article, db.session))
admin.add_view(ArticleColumnView(ArticleColumn, db.session))
admin.add_view(FileView(File, db.session))
admin.add_view(FileColumnView(FileColumn, db.session))