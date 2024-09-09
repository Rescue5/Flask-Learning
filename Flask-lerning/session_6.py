from flask import (Flask, render_template, url_for, request, redirect, flash, get_flashed_messages, session, abort,
                   g, make_response, request)
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DEBUG = True
DATABASE = '/tmp/test.db'
SECRET_KEY = '30a469afa9bd791e087d03e29a68e57cbc6e1c9a'


class UserLogin:
    def __init__(self):
        self.__user = None

    def fromDB(self, user_id, db):
        self.__user = db.get_user(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymus(self):
        return False

    def get_id(self):
        return str(self.__user['user_id_pk'])


class FDataBase:
    def __init__(self, conn):
        self.__conn = conn
        self.__cursor = self.__conn.cursor()

    def getsongs(self):
        sql = """SELECT * FROM songs"""
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res:
                return res
        except Exception as e:
            print(f"Ошибка чтение из БД: {e}")
        return []

    def addsong(self, name, artist, album, duration):
        check_sql = """SELECT COUNT(*) as count FROM songs WHERE name=?"""
        sql = """INSERT INTO songs (name, artist, album, duration) VALUES (?, ?, ?, ?)"""
        try:
            self.__cursor.execute(check_sql, (name,))
            res = self.__cursor.fetchone()
            if res['count'] > 0:
                return False
            self.__cursor.execute(sql, (name, artist, album, duration))
            self.__conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка записи в базу данных: {e}")
            return False

    def get_link_by_slug(self, slug):
        sql = """SELECT artist_url FROM songs WHERE artist=?"""
        try:
            self.__cursor.execute(sql, (slug,))
            res = self.__cursor.fetchone()
            if res:
                return res
        except Exception as e:
            print(e)

    def get_user_by_login(self, user_login):
        sql = """SELECT * FROM users WHERE login = ?"""
        try:
            self.__cursor.execute(sql, (user_login,))
            res = self.__cursor.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except Exception as e:
            print("Ошибка чтения с БД")
            print(e)

    def check_unic_login(self, login):
        sql = """SELECT COUNT(*) as count FROM users WHERE login=?"""
        try:
            self.__cursor.execute(sql, (login,))
            res = self.__cursor.fetchone()
            if res['count'] > 0:
                return False
            else:
                return True
        except Exception as e:
            print(e)

    def register(self, login, password):
        sql = """INSERT INTO users (login, password) VALUES (?, ?)"""
        hash = generate_password_hash(password)
        try:
            self.__cursor.execute(sql, (login, hash))
            self.__conn.commit()
        except Exception as e:
            print(e)

    def get_user(self, user_id_pk):
        sql = f"""SELECT * FROM users WHERE user_id_pk = {user_id_pk} LIMIT 1"""
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except Exception as e:
            print(e)
        return False


app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager(app)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'test.db')))


@login_manager.user_loader
def load_user(user_id_pk):
    print("load_user")
    return UserLogin().fromDB(user_id_pk, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def get_conn():
    """Установление соединение с БД и получение объекта для взаимодействия с ней"""
    db = get_db()
    global dbase
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    if request.method == 'POST':
        user_login = request.form['login']
        user = dbase.get_user_by_login(user_login)
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('main_page'))
        else:
            flash('Неверная пара логин/пароль')
    return render_template('main(main_login).html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        login = request.form["username"]
        password = request.form["password"]
        password_2 = request.form["confirm_password"]
        if not dbase.check_unic_login(login):
            flash("Username is already used")
            return render_template("main(register).j2")
        elif password != password_2:
            flash("Passwords are not equal")
        else:
            dbase.register(login, password)
            flash("Register complete")
            return redirect(url_for("login"))

    return render_template("main(register).j2")


@app.route('/')
def main_page():
    return render_template('main(main_page).j2', songs=dbase.getsongs())


@app.route('/addsong', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        name = request.form['name']
        artist = request.form['artist']
        album = request.form['album']
        duration = request.form['duration']
        if dbase.addsong(name, artist, album, duration):
            flash('Song added successfully!', category='succes')
        else:
            flash('Something went wrong!', category='fail')

    return render_template('main(add_song).j2')


@app.route('/<slug>')
@login_required
def show_artist(slug):
    try:
        return render_template(f"{slug}.html", slug=slug)
    except Exception as e:
        abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/transfer')
def transfer_url():
    return redirect(url_for('main_page'), 301)


if __name__ == '__main__':
    app.run(debug=True)
