from flask import Flask, render_template

app = Flask(__name__, template_folder='views')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/games')
def games():
    return render_template('games.html')


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
