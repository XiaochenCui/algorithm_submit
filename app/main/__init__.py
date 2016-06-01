from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from app.models import Permission, ArticleColumn


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@main.app_context_processor
def inject_column():
    return dict(ArticleColumn=ArticleColumn)
