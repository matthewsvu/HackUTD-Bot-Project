from flask import Flask
from flask import render_template
from threading import Thread

app = Flask(__name__)


@app.route('/')
def render_index():
    return render_template('index.html')

def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
