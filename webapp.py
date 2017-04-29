#!/usr/bin/env python3
from flask import Flask, render_template, request, session, redirect
import json
import os

"""
- Display search queries if user already has preferences saved
- Ask for preferences otherwise.
"""

app = Flask(__name__)

flask.secret_key = os.urandom(24)

database = None

@app.route('/')
@app.route('/index')
def index():

    #if the client has previously searched for something
    if 'last_query' in request.cookies:
        query = request.cookies['last_query']

        redirect(url_for('/search', **query))
        pass

    return render_template('index.html',
                           title='this is a title')

@app.route('/search')
def display_results():
    query = request.args

    # TODO(pangt): Search and accumulate data

    return render_template('search.html')

@app.route('/caregiver/<hash>')
def display_caregiver(hash):
    # TODO(pangt): add HTML template for the caregiver,
    # TODO(pangt): extract caregiver data from database
    # TODO(pangt): insert caregiver data into HTML template
    return

if __name__ == "__main__":

    with open('caregiver_database.json', 'r') as json_file:
        database = json.load(json_file)
        app.run(debug=False)
        pass
