from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages, session
import time
app = Flask(__name__)

app.config['SECRET_KEY'] = 'askdafnpailfinealfjkafj;sdjf;afjaefjaiejjaskldasd'

songs = [
    {"name": "Saw", "artist": "Orbit Culture",
        "album": "Redfog", "duration": "5:40", "artist_link": "/Orbit_culture"},
    {"name": "TokSik", "artist": "STARSET",
        "album": "EP TokSik", "duration": "3:51", "artist_link": "/STARSET"},
    {"name": "Let Me Go", "artist": "Sullivan King",
        "album": "Thrones of Blood",   "duration": "3:42", "artist_link": "/Sullivan_King"}
]

users_list = []


@app.route('/')
def main_page():
    return render_template('main(main_page).j2', songs=songs)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if request.form['password'] != request.form['confirm_password']:
            flash('Пароли должны совпадать', category='error')
        elif request.form['username'] in users_list:
            flash('Вы уже зарегистрированы', category='error')
        else:
            users_list.append(request.form)
            flash('Вы успешно зарегистрированы!', category='succes')
    return render_template('main(register).j2')


@app.route('/fail_register', methods=['POST', 'GET'])
def fail_register():
    return render_template('main(fail_register).j2')


@app.errorhandler(404)
def main_404(error):
    return render_template('404.html'), 404


@app.route('/callback', methods=['POST', 'GET'])
def main_callback():
    if 'usercall' in session:
        return redirect(url_for('main_page'))
    elif request.method == 'POST' and request.form['username'] == 'admin':
        session['usercall'] = request.form['username']
        return redirect(url_for('register'))
    return render_template('main(callback).j2')


if __name__ == '__main__':
    app.run(debug=True)
