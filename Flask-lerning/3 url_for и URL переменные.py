from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def main_view():
    print(url_for('main_view'))
    return render_template('index.j2', title='привет')


@app.route('/found')
def found_view():
    print(url_for('found_view'))
    return render_template('found.j2')


@app.route('/user/<path:username>')
def user_view(username):
    return f"<h1>Пользователь - {username}</h1>"


if __name__ == '__main__':
    app.run(debug=True)
