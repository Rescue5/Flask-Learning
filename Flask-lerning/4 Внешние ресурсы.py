from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

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
            return render_template('main(fail_register).j2')
        elif request.form['username'] in users_list:
            return render_template('main(fail_register).j2')
        else:
            users_list.append(request.form)
            return redirect(url_for('main_page'))
    return render_template('main(register).j2')


@app.route('/fail_register', methods=['POST', 'GET'])
def fail_register():
    return render_template('main(fail_register).j2')


if __name__ == '__main__':
    app.run(debug=True)
