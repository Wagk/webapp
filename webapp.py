#!/usr/bin/env python3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='this is a title')

@app.route('/caregiver/<hash>')
def display_caregiver(hash):
    # TODO(pangt): add HTML template for the caregiver,
    # TODO(pangt): extract caregiver data from database
    # TODO(pangt): insert caregiver data into HTML template
    return

if __name__ == "__main__":
    app.run(debug=False)
