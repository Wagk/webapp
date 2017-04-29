#!/usr/bin/env python3
from flask import Flask, render_template, request, session, redirect
import json
import os
import copy
import datetime

"""
- Display search queries if user already has preferences saved
- Ask for preferences otherwise.
"""

app = Flask(__name__)
app.secret_key = os.urandom(24)
database = None


@app.route('/')
@app.route('/index')
def index():

    #if the client has previously searched for something
    if 'last_query' in request.cookies:
        query = request.cookies['last_query']

        print(query)

        redirect(url_for('/search', **query))
        pass

    return render_template('index.html',
                           title='this is a title',
                           dest='/search',
                           is_hidden=True
    )

@app.route('/search')
def display_results():

    local_database = database

    print(request.args.items())

    for key, value in request.args.items():
        if key == 'gender':
            local_database = [i for i in local_database if i['gender'] == value]
        elif key == 'skills':
            local_database = [i for i in local_database if i['skills'] == value]
            pass
        elif key == 'startdate':
            local_database = [i for i in local_database if i['startdate'] == value]
        elif key == 'starthour':
            local_database = [i for i in local_database if i['starthour'] == value]
        elif key == 'startmin':
            local_database = [i for i in local_database if i['startmin'] == value]
        elif key == 'enddate':
            local_database = [i for i in local_database if i['enddate'] == value]
        elif key == 'endhour':
            local_database = [i for i in local_database if i['endhour'] == value]
        elif key == 'endmin':
            local_database = [i for i in local_database if i['endmin'] == value]
        pass

    # TODO(pangt): format and submit data


    return render_template('index.html',
                           result=local_database,
                           title='Search Results',
                           dest='/search',
                           is_hidden=False
    )

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
