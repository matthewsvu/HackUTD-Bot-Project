from flask import Flask
from flask import render_template
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return render_template('index.html')

def run():
    app.run()

def keep_alive():
    t = Thread(target=run)
    t.start()
