from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages, session, abort
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


if __name__ == '__main__':
    app.run(debug=True)
