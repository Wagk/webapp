#!/usr/bin/env python3
from flask import Flask, render_template, request, session, redirect, make_response
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

skill_list = []


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html',
                           title='this is a title',
                           skill_list=skill_list,
                           dest='/search',
                           is_hidden=True)

@app.route('/search')
def display_results():

    if 'last_query' in request.cookies:
        query = request.cookies['last_query']
    else:
        query = request.args.to_dict(flat=False)
        print("printing query")
        print(query)
        pass

    # grab presentable stuff from database
    def format(entry):
        return {x : y for x, y in entry.items() if x in [
            'name', 'gender', 'description', 'price', 'skills'
        ]}

    def correct_skills(entry):
        for skill in request.args.getlist('skills'):
            if skill not in entry['skills']:
                return False
            return True

    def correct_day(entry):
        req_date = datetime.strptime(request.args.get('startdate'), '%Y-%m-%d')
        avail_day = int(req_date.strftime('%w'))
        return entry['days'][avail_day] == True


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
        return care_start_24hr < req_start_24hr and req_end_24hr < care_end_24hr

    local_database = [i for i in database if correct_skills(i) and correct_day(i) and
                      correct_hours(i)]

    #format message
    # text_message = "You have searched for a caregiver on " + request.args.get('startdate') + ", from " + request.args.get('starthour') + ":" + request.args.get('startmin')  + " to " + request.args.get('endhour') + ":" + request.args.get('endmin')
    text_message = "You have searched for a caregiver on {}, from {} to {}".format(request.args.get('startdate'),
                                                                                   datetime.strptime('{}:{}'.format(request.args.get('starthour'),
                                                                                                                    request.args.get('startmin')),
                                                                                                     '%H%M'),
                                                                                   datetime.strptime('{}{}'.format(request.args.get('endhour'),
                                                                                                                   request.args.get('endmin')),
                                                                                                                               '%H%M'))

    resp = make_response(render_template('index.html',
                                         result=[format(i) for i in local_database],
                                         skill_list=skill_list,
                                         text_message = text_message,
                                         title='Search Results',
                                         dest='/search',
                                         is_hidden=False))
    resp.set_cookie('last_query', )
    return resp


@app.route('/caregiver/<hash>')
def display_caregiver(hash):
    # TODO(pangt): add HTML template for the caregiver,
    # TODO(pangt): extract caregiver data from database
    # TODO(pangt): insert caregiver data into HTML template
    return

if __name__ == "__main__":

    with open('caregiver_database.json', 'r') as json_file:
        database = json.load(json_file)

        # dynamically populate skills list
        for caretaker in database:
            for skill in caretaker['skills']:
                if skill not in skill_list:
                    skill_list.append(skill)
                pass
            pass

        app.run(debug=False)
        pass
