from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages, session, abort, g
import sqlite3
import os

DEBUG = True
DATABASE = '/tmp/test.db'
SECRET_KEY = 'fajnpavvjsdgmvsa;cerfa/sbv/rsgtbqo3k4gjiewovwslj'


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


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
def main_page():
    db = FDataBase(get_db())
    print(db.getsongs())
    return render_template('main(main_page).j2', songs=db.getsongs())


@app.route('/addsong', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        db = FDataBase(get_db())
        name = request.form['name']
        artist = request.form['artist']
        album = request.form['album']
        duration = request.form['duration']
        if db.addsong(name, artist, album, duration):
            flash('Song added successfully!', category='succes')
        else:
            flash('Something went wrong!', category='fail')

    return render_template('main(add_song).j2')


if __name__ == '__main__':
    app.run(debug=True)
