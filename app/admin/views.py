from flask.ext.admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import *

admin = Admin(name='Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Follow, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Theme, db.session))
admin.add_view(ModelView(Article, db.session))
admin.add_view(ModelView(ArticleColumn, db.session))