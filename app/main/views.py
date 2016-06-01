import ast
import json
import string

from flask import render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response, jsonify
from flask.ext.login import login_required, current_user

from . import main
from .forms import *
from .. import db
from ..decorators import admin_required, permission_required
from ..models import Permission, Role, User, Post, Theme, Article, ArticleColumn


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    theme=Theme.query.filter_by(title='1_title').first(),
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items


    return render_template('index.html', form=form, posts=posts,
                           show_followed=show_followed, pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="学生列表 - ",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/teacher-list')
@login_required
def teacher_list():
    users = User.query.join(Role).filter(Role.name == 'Teacher').all()
    return render_template('teacher_list.html', users=users)


@main.route('/theme-list')
@login_required
def theme_list():
    themes = Theme.query.order_by(Theme.timestamp.desc())
    return render_template('theme_list.html', themes=themes)


@main.route('/manage-theme/<int:id>', methods=['GET', 'POST'])
@login_required
def manage_theme(id):
    user = User.query.filter_by(id=id).first()
    if user is None or \
                    current_user.id != id:
        abort(404)
    form = ThemeForm()
    if current_user.can(Permission.MANAGE_THEME) and \
            form.validate_on_submit():
        theme = Theme(title=form.title.data, body=form.body.data, author=current_user._get_current_object())
        db.session.add(theme)
        return redirect(url_for('.manage_theme', id=id))
    themes = user.themes.order_by(Theme.timestamp.desc()).all()
    return render_template('manage_theme.html', form=form, user=user, themes=themes)


@main.route('/theme-list-student/<int:id>')
@login_required
def theme_list_student(id):
    user = User.query.filter_by(id=id).first()
    if user is None or \
                    current_user.id != id:
        abort(404)
    page = request.args.get('page', 1, type=int)
    query = current_user.followed_themes
    pagination = query.order_by(Theme.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    themes = pagination.items
    # has_submit = {}
    # for i in range(len(themes)):
    #     var = Post.query.join(Theme, Theme.id = Post.)
    return render_template('theme_list.html', user=user, themes=themes,
                           pagination=pagination)


@main.route('/theme/<int:id>', methods=['GET', 'POST'])
@login_required
def theme(id):
    theme = Theme.query.get_or_404(id)
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    theme=theme,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.theme', id=theme.id))
    return render_template('theme.html', form=form, themes=[theme])


@main.route('/theme-teacher/<int:id>', methods=['GET', 'POST'])
@permission_required(Permission.MANAGE_THEME)
def theme_teacher(id):
    theme = Theme.query.get_or_404(id)
    if theme.author != current_user:
        abort(404)
    posts = Post.query.filter_by(theme=theme).all()
    return render_template('theme_teacher.html', themes=[theme], posts=posts)


@main.route('/theme-delete/<int:id>', methods=['GET', 'POST'])
def theme_delete(id):
    theme = Theme.query.filter_by(id=id).first()
    if theme is None:
        flash('此主题不存在')
        return redirect(url_for('.theme_list'))
    if theme.author != current_user:
        flash('您无权删除该主题')
        return redirect(url_for('.theme_list'))
    theme.delete()
    flash('主题删除成功！')
    return redirect(url_for('.theme_list'))


@main.route('/theme-edit/<int:id>', methods=['GET', 'POST'])
def theme_edit(id):
    theme = Theme.query.filter_by(id=id).first()
    if theme is None:
        flash('此主题不存在')
        return redirect(url_for('.theme_list'))
    if theme.author != current_user:
        flash('您无权编辑该主题')
        return redirect(url_for('.theme_list'))
    form = ThemeForm()
    if form.validate_on_submit():
        theme.title = form.title.data
        theme.body = form.body.data
        db.session.add(theme)
        flash('主题已被更新')
        return redirect(url_for('.theme_edit', id=theme.id))
    form.title.data = theme.title
    form.body.data = theme.body
    return render_template('theme_edit.html', form=form)


@main.route('/column/<int:id>')
def article_column(id):
    column = ArticleColumn.query.filter_by(id=id).first()
    articles = Article.query.filter_by(column=column).all()
    return render_template('column.html', column=column, articles=articles)


@main.route('/column_list')
@login_required
@admin_required
def column_list():
    form = ColumnTitleForm()
    columns = ArticleColumn.query.all()
    return render_template('column_list.html', columns=columns, form=form)


@main.route('/article_list/<int:id>')
@admin_required
def article_list(id):
    pass


@main.route('/article_edit')
@admin_required
def article_edit(id):
    pass


@main.route('/column_delete')
@admin_required
def column_delete(id):
    pass


@main.route('/column_title', methods=['POST', 'GET'])
@admin_required
def column_title():
    ret_data = {"id": request.args.get('id'),
                "title": request.args.get('title')
                }
    column = ArticleColumn.query.filter_by(id=ret_data["id"]).first()
    column.title = ret_data["title"]
    db.session.add(column)
    flash('栏目标题已经被更新')
    return jsonify(ret_data)


@main.route('/column_add', methods=['POST', 'GET'])
@admin_required
def column_add():
    form = ColumnAddForm()
    if form.validate_on_submit():
        column = ArticleColumn(title = form.data.title)
        db.session.add(column)
        flash('栏目添加成功！')
    else:
        flash('栏目添加失败！')
    return redirect(url_for(column_list))



