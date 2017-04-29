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
                           is_hidden="true"
    )

@app.route('/search')
def display_results():

    print(request.args.items())

    # grab presentable stuff from database
    def format(entry):
        return {x : y for x, y in entry if x in [
            'name', 'gender', 'description', 'price', 'skills'
        ]}

    def correct_skills(entry):
        print(request.args.get('skills'))
        for skill in request.args.get('skills'):
            if skill not in entry['skills']:
                return False
        return True

    def correct_gender(entry):
        return entry['gender'] == request.args.get['gender']

    def correct_day(entry):
        req_date = datetime.strptime(request.args.get('startdate'), '%Y-%m-%d')
        avail_day = int(req_date.strftime('%w'))
        return entry['day'][avail_day] == True

    def correct_hours(entry):
        req_start_24hr = datetime.strptime('{}{}'.format(request.args.get('starthour'),
                                                         request.args.get('startmin')),
                                           '%H%M')
        req_end_24hr = datetime.strptime('{}{}'.format(request.args.get('endhour'),
                                                       request.args.get('endmin')),
                                         '%H%M')

        if req_end_24hr < req_start_24hr:
            req_end_24hr, req_start_24hr = req_start_24hr, req_end_24hr

        care_start_24hr = datetime.strptime(entry['start'], '%H%M')
        care_end_ = datetime.strptime(entry['end'], '%H%M')

        return care_start < req_start_24hr and req_end_24hr < care_end

    local_database = [i for i in database if
                      correct_skills(i) and
                      correct_gender(i) and
                      correct_day(i) and
                      correct_hours(i)]

    return render_template('index.html',
                           # result=local_database,
                           result=[format(i) for i in local_database],
                           title='Search Results',
                           dest='/search',
                           is_hidden="false")

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
