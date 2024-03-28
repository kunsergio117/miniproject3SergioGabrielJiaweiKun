### INF601 - Advanced Programming in Python
### Sergio Gabriel Jiawei Kun
### Mini Project 3
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, abort, app
)
from werkzeug.utils import secure_filename
from flaskr.auth import login_required
from flaskr.db import get_db
from flask import current_app

bp = Blueprint('blog', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    current_app.config['UPLOAD_FOLDER'] = '/Users/kunsergio/Library/CloudStorage/GoogleDrive-kunsergio117@gmail.com/My Drive/FHSU/Spring_2024/Advanced_Python/miniproject3SergioGabrielJiaweiKun/flaskr/media_uploads'
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        file = request.files['image']

        error = None

        if not title:
            error = 'Title is required.'


        if file:
            if allowed_file(file.filename):
                # save file
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                print("saved: " + filename + " to media_uploads folder")

                # Continue with post creation
                db = get_db()
                db.execute(
                    'INSERT INTO post (title, body, author_id, image_filename)'
                    ' VALUES (?, ?, ?, ?)',
                    (title, body, g.user['id'], filename)
                )
                db.commit()
                return redirect(url_for('blog.index'))
            else:
                flash(error)
                return redirect(request.url)
        else:
            # Continue with post creation (without image)
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, image_filename'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        image_file = request.files['image']
        error = None

        if not title:
            error = 'Title is required.'

        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, image_filename = ?'
                ' WHERE id = ?',
                (title, body, filename, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
        else:
            flash(error)

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


    return post
