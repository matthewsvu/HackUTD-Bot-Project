from flask import Flask
from flask import render_template
from threading import Thread

app = Flask(__name__)


@app.route('/')
def render_index():
    return render_template('index.html')

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)

