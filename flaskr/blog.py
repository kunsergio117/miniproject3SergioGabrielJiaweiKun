### INF601 - Advanced Programming in Python
### Sergio Gabriel Jiawei Kun
### Mini Project 3
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, abort
)
from werkzeug.utils import secure_filename
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '')
        db = get_db()
        if search_query:
            # Perform search query on posts or titles
            # You can adjust the SQL query based on your database schema and search logic
            query = """
                SELECT p.id, title, body, created, author_id, username
                FROM post p JOIN user u ON p.author_id = u.id
                WHERE title LIKE ? OR body LIKE ?
                ORDER BY created DESC
            """
            search_term = f"%{search_query}%"
            posts = db.execute(query, (search_term, search_term)).fetchall()
        else:
            # Fetch all posts
            posts = db.execute(
                'SELECT p.id, title, body, created, author_id, username'
                ' FROM post p JOIN user u ON p.author_id = u.id'
                ' ORDER BY created DESC'
            ).fetchall()
    else:
        # Fetch all posts if no search query is provided
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
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        # Continue with post creation
        if error is None:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
        else:
            flash(error)

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        db = get_db()
        # Perform search query
        results = db.execute(
            'SELECT id, title, body FROM post WHERE title LIKE ? OR body LIKE ?',
            ('%' + search_query + '%', '%' + search_query + '%')
        ).fetchall()
        return render_template('blog/search_results.html', search_results=results, query=search_query)
    return redirect(url_for('blog.index'))  # Redirect to index if accessed via GET method
