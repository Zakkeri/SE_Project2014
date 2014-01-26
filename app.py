import sys
import os
from flask import Flask, request, session, url_for, \
    abort, render_template, flash, redirect, Response

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent = True)

app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run()
