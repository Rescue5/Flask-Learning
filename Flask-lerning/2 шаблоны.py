from flask import Flask, render_template

app = Flask(__name__)

songs = [
    {"name": "Saw", "artist": "Orbit Culture",
        "album": "Redfog", "duration": "5:40"},
    {"name": "TokSik", "artist": "STARSET",
        "album": "EP TokSik", "duration": "3:51"},
    {"name": "Let Me Go", "artist": "Sullivan King",
        "album": "Thrones of Blood", "duration": "3:42"}
]


@app.route('/')
def main_page():
    return render_template('index.j2', title='Моя медиатека', link='info', songs=songs)


@app.route('/info')
def info_page():
    return render_template('index.j2', title='АХАХАХАХАХА, НУ ЖМИ ЕЩЕ РАЗ', link='/')


if __name__ == '__main__':
    app.run(debug=True)
