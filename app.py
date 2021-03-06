from flask import Flask, render_template, request, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
from helper import descriptions, dates, tags, goals, names, github_links, project_links, brief_desc

#CREATE THE NAME OF THE APP
app = Flask(__name__)
app.config['SECRET_KEY'] = '4w3yjcf7t8w9eovc5we'

#CREATING A FORM WHICH IS INHERITING FROM FLASKFORM. THIS WILL BE THE FILTER FORM
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

    #THE UNFILTERED PROJECTS LIST WILL BE THE LIST OF PROJECTS YOU INITIALLY SEE DISPLAYED WHEN YOU FIRST GO TO THE WEBSITE
    unfiltered_projects = ["eisenhowersquadrant", "depechehouse", "depechecodes", "mileagecalculator", "djangounrestrained"]
    #FILTERED PROJECTS WILL BE USED AS SOON AS THE FILTER FORM IS SUBMITTED
    filtered_projects = []
    #CREATING AN INSTANCE OF THE FORM
    filter_form = ProjectFilter()
    #VARIABLES THAT ARE A BOOLEAN VALUE OF THE FORM DATA
    python_bool = filter_form.python_field.data
    flask_bool = filter_form.flask_field.data
    django_bool = filter_form.django_field.data
    sql_bool = filter_form.sql_field.data
    csv_bool = filter_form.csv_field.data

    #A LIST WILL BE CREATED OF THE TAGS THAT WERE SELECTED
    selected_tags = []
    #IF A CHECKBOX WAS SELECTED THE BOOL VALUE WILL BE TRUE, THUS ADDING ITS TAG TO THE LIST
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
        #DICTIONARY OF PROJECTS WITH THEIR CORESPONDING TAGS
        projects = [
            {id: 1, "display_name": "Eisenhower's Quadrant", "name": "eisenhowersquadrant", "Python": True, "Flask": True, "Django": False, "SQL": False, "CSV": True}, 
            {id: 2, "display_name": "Depeche House", "name": "depechehouse", "Python": True, "Flask": True, "Django": False, "SQL": True, "CSV": False},
            {id: 3, "display_name": "Depeche Codes", "name": "depechecodes", "Python": True, "Flask": True, "Django": False, "SQL": False, "CSV": False},
            {id: 4, "display_name": "Mileage Calculator", "name": "mileagecalculator", "Python": True, "Flask": False, "Django": False, "SQL": False, "CSV": True},
            {id: 5, "display_name": "Django Unrestrained", "name": "djangounrestrained", "Python": True, "Flask": False, "Django": True, "SQL": False, "CSV": False}
            ]

        #ITERATE THROUGH PROJECTS DICTIONARY, IF ALL SELECTED TAGS ARE TRUE IN ONE OF THE PROJECTS IN THE DICTIONARY, THE PROJECT NAME WILL BE ADDED TO THE FILTERED_PROJECTS LIST 
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

    return render_template("index.html", filter_form=filter_form, filtered_projects=filtered_projects, unfiltered_projects=unfiltered_projects, names=names, brief_desc=brief_desc)


#THIS WILL TAKE YOU TO DIFFERENT PAGES DEPENDING ON THE PROJECT_NAME. 
@app.route('/project/<project_name>')
def project(project_name):

    return render_template("projects.html", project_name=project_name, name=names[project_name], description=descriptions[project_name], date_created=dates[project_name], tags=tags[project_name], goals=goals[project_name], github_link=github_links[project_name], project_link=project_links[project_name])



@app.route('/profile')
def profile():
    return render_template("profile.html")


if __name__=='__main__':
    app.run(debug=True)