from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.config['SECRET_KEY'] = '30a469afa9bd791e087d03e29a68e57cbc6e1c9a'


@app.route('/')
def main_page():
    if 'visits' in session:
        session['visits'] += 1
    else:
        session['visits'] = 1
    return f"visits: {session['visits']}"


if __name__ == '__main__':
    app.run(debug=True)


