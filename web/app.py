import sqlite3
from werkzeug.exceptions import abort
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user

from web import app, db, manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect(url_for('index'))
        else:
            flash("идентификатор или пароль некорректен")
    else:
        flash("Введите идентификатор и пароль")
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')

    if request.method == 'POST':
        if not (email or password):
            flash("идентификатор или пароль некорректен")
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(email=email, password=hash_pwd, name=name)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('index'))
    return render_template('signup.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next' + request.url)
    return response


@app.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date_begin = request.form['date_begin']
        date_end = request.form['date_end']
        status = 'Ожидание'
        code = request.form['teg']
        if not title or not content or not date_begin or not date_end:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO posts (title, content, status, date_begin, date_end, code) VALUES (?, ?, ?, ?, ?, ?)',
                (title, content, status, date_begin, date_end, code))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/accepted', methods=('GET', 'POST'))
@login_required
def accepted():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('accepted.html', posts=posts)


@app.route('/tags', methods=('GET', 'POST'))
@login_required
def tags():
    return render_template('tags.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date_begin = request.form['date_begin']
        date_end = request.form['date_end']
        code = request.form['code']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?, date_begin = ?, date_end = ?, code = ? '
                         ' WHERE id = ?',
                         (title, content, date_begin, date_end, code, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


@app.route('/<int:id>/accept', methods=('POST',))
@login_required
def accept(id):
    post = get_post(id)
    conn = get_db_connection()
    acc = 'Принято'
    conn.execute('UPDATE posts SET status = ? WHERE id = ?', (acc, id))
    conn.commit()
    conn.close()
    # persons_conn = sqlite3.connect('./AllPersons.db')
    # for it in range(int(post['date_begin']),int(post['date_end'] + 1)):
    #     persons_conn.execute('UPDATE posts SET status = ? WHERE id = ?', (acc, id))
    # #persons_conn.execute('UPDATE posts SET status = ? WHERE id = ?', (acc, id))
    # #persons_conn.commit()
    # persons_conn.close()
    flash('"{}" was successfully accepted!'.format(post['title']))
    return redirect(url_for('accepted'))


@app.route('/<int:id>/refusal', methods=('POST',))
@login_required
def refusal(id):
    post = get_post(id)
    conn = get_db_connection()
    acc = 'Отказано'
    conn.execute('UPDATE posts SET status = ? WHERE id = ?', (acc, id))
    conn.commit()
    conn.close()
    flash('"{}" was successfully refusaled!'.format(post['title']))
    return redirect(url_for('index'))


app.run('127.0.0.1', debug=True)
