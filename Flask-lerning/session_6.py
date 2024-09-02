from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages, session, abort, g, \
    make_response, request
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DEBUG = True
DATABASE = '/tmp/test.db'
SECRET_KEY = '30a469afa9bd791e087d03e29a68e57cbc6e1c9a'


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


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'test.db')))


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
    return render_template("main(main_login).html")


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
def show_artist(slug):
    return render_template(f"{slug}.html", slug=slug)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404, {"Content-Type": "text/plain"}


@app.route('/transfer')
def transfer_url():
    return redirect(url_for('main_page'), 301)


if __name__ == '__main__':
    app.run(debug=True)
