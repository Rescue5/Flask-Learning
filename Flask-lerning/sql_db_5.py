from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages, session, abort, g
import sqlite3
import os

DEBUG = True
DATABASE = '/tmp/test.db'
SECRET_KEY = 'fajnpavvjsdgmvsa;cerfa/sbv/rsgtbqo3k4gjiewovwslj'

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
    db = get_db()
    return render_template('main(main_page).j2')


if __name__ == '__main__':
    app.run(debug=True)
