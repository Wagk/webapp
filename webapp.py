#!/usr/bin/env python3
from flask import Flask, render_template, request, session, redirect
import json
import os
import copy
from datetime import datetime

"""
- Display search queries if user already has preferences saved
- Ask for preferences otherwise.
"""

app = Flask(__name__)
app.secret_key = os.urandom(24)
database = None

skill_list = [
    "Autism Friendly", "Disability Friendly", "Asthmatic Friendly"
]

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
        return {x : y for x, y in entry.items() if x in [
            'name', 'gender', 'description', 'price', 'skills'
        ]}

    def correct_skills(entry):
        for skill in request.args.getlist('skills'):
            if skill_list[int(skill)] not in entry['skills']:
                print("Incorrect skills! {} wanted but not found".format(skill))
                print(entry['skills'])
                return False

            print("Correct Skills")
            return True

    def correct_gender(entry):
        correct = entry['gender'] == request.args.get('gender')
        print("Gender: {}".format(correct))
        return correct

    def correct_day(entry):
        req_date = datetime.strptime(request.args.get('startdate'), '%Y-%m-%d')
        avail_day = int(req_date.strftime('%w'))
        correct = entry['days'][avail_day] == True
        print("Day: {}".format(correct))
        return correct

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
        care_end_24hr = datetime.strptime(entry['end'], '%H%M')
        correct = care_start_24hr < req_start_24hr and req_end_24hr < care_end_24hr
        print("Time: {}".format(correct))
        return correct

    local_database = [i for i in database if
                      correct_skills(i) and
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
