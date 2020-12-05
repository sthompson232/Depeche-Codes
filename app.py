from flask import Flask, render_template, request, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
from helper import descriptions, dates, tags, goals, names

app = Flask(__name__)
app.config['SECRET_KEY'] = '4w3yjcf7t8w9eovc5we'

class ProjectFilter(FlaskForm):
    python_field = BooleanField("Python")
    flask_field = BooleanField("Flask")
    django_field = BooleanField("Django")
    sql_field = BooleanField("SQL")
    csv_field = BooleanField("CSV Files")
    search = SubmitField("Filter")


################################################################################

#ROUTES

@app.route('/', methods=["GET", "POST"])
def index():

    unfiltered_projects = ["Eisenhower's Quadrant", "Depeche House", "Depeche Codes", "UNFILTERED LIST"]
    filtered_projects = []

    filter_form = ProjectFilter()
  
    python_bool = filter_form.python_field.data
    flask_bool = filter_form.flask_field.data
    django_bool = filter_form.django_field.data
    sql_bool = filter_form.sql_field.data
    csv_bool = filter_form.csv_field.data

    selected_tags = []

    if python_bool:
        selected_tags.append("Python")
    if flask_bool:
        selected_tags.append("Flask")
    if django_bool:
        selected_tags.append("Django")
    if sql_bool:
        selected_tags.append("SQL")
    if csv_bool:
        selected_tags.append("CSV")

    #FILTER FORM
    if filter_form.search.data and len(selected_tags) != 0:
        
        projects = [
            {id: 1, "name": "Eisenhower's Quadrant", "Python": True, "Flask": True, "Django": False, "SQL": False, "CSV": True}, 
            {id: 2, "name": "Depeche House", "Python": True, "Flask": True, "Django": False, "SQL": True, "CSV": False},
            {id: 3, "name": "Depeche Codes", "Python": True, "Flask": True, "Django": False, "SQL": False, "CSV": False}
            ]

        for project in projects:
            truth_checker = []
            for selected_tag in selected_tags:
                if project[selected_tag] == True:
                    truth_checker.append(True)
                else:
                    truth_checker.append(False)
            if len(truth_checker) == truth_checker.count(True):
                filtered_projects.append(project["name"])
                truth_checker = [] 

    else:
        filtered_projects = unfiltered_projects

    return render_template("index.html", filter_form=filter_form, filtered_projects=filtered_projects, unfiltered_projects=unfiltered_projects)



@app.route('/project/<project_name>')
def project(project_name):

    return render_template("projects.html", project_name=project_name, name=names[project_name], description=descriptions[project_name], date_created=dates[project_name], tags=tags[project_name], goals=goals[project_name])



@app.route('/profile')
def profile():
    return render_template("profile.html")


if __name__=='__main__':
    app.run(debug=True)