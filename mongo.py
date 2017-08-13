# Noah Segal-Gould, Summer 2017

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'courselist'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/courselist'

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/crn/<int:course_registration_number>')
def get_courses_by_crn(course_registration_number):
    search_query = request.args.get('search', None)
    if search_query is not None:
        mongo.db.courselist.drop_indexes()
        mongo.db.courselist.create_index([("$**", "text")], name="textScore")
        cursor = mongo.db.courselist.find({'$text': {'$search': search_query.replace("+", " ")}},
                                          {'score': {'$meta': 'textScore'}})
        cursor.sort([('score', {'$meta': 'textScore'})])
        output = list(sorted(dict(c).items()) for c in cursor)
        for course in output:
            del course[11]
        if len(output) >= 1:
            return render_template('courses.html', output=output)
    sorted_query = request.args.get('sort', None)
    if sorted_query is not None:
        courses = mongo.db.courselist
        if sorted_query == "course_registration_number":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_registration_number": course_registration_number})],
                key=lambda k: k[2][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_code":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_registration_number": course_registration_number})],
                key=lambda k: k[1][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "new_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_registration_number": course_registration_number})],
                key=lambda k: k[7][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "old_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_registration_number": course_registration_number})],
                key=lambda k: k[8][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "department":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_registration_number": course_registration_number})],
                key=lambda k: k[4][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "semester":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_registration_number": course_registration_number})],
                key=lambda k: k[11][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_title":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_registration_number": course_registration_number})],
                key=lambda k: k[3][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "professors":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_registration_number": course_registration_number})],
                key=lambda k: k[9][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "locations":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_registration_number": course_registration_number})],
                key=lambda k: k[6][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "schedules":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_registration_number": course_registration_number})],
                key=lambda k: k[10][1])
            return render_template('courses.html', output=output)
        else:
            courses = mongo.db.courselist
            output = [sorted(c.items()) for c in courses.find({"course_registration_number": course_registration_number})]
            return render_template('courses.html', output=output)
    courses = mongo.db.courselist
    output = [sorted(c.items()) for c in courses.find({"course_registration_number": course_registration_number})]
    return render_template('courses.html', output=output)


@app.route('/course_code/<string:course_code>')
def get_courses_by_code(course_code):
    search_query = request.args.get('search', None)
    if search_query is not None:
        mongo.db.courselist.drop_indexes()
        mongo.db.courselist.create_index([("$**", "text")], name="textScore")
        cursor = mongo.db.courselist.find({'$text': {'$search': search_query.replace("+", " ")}},
                                          {'score': {'$meta': 'textScore'}})
        cursor.sort([('score', {'$meta': 'textScore'})])
        output = list(sorted(dict(c).items()) for c in cursor)
        for course in output:
            del course[11]
        if len(output) >= 1:
            return render_template('courses.html', output=output)
    sorted_query = request.args.get('sort', None)
    if sorted_query is not None:
        courses = mongo.db.courselist
        if sorted_query == "course_registration_number":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_code": course_code.replace("_", " ")})],
                key=lambda k: k[2][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_code":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_code": course_code.replace("_", " ")})],
                key=lambda k: k[1][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "new_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_code": course_code.replace("_", " ")})],
                key=lambda k: k[7][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "old_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_code": course_code.replace("_", " ")})],
                key=lambda k: k[8][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "department":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_code": course_code.replace("_", " ")})],
                key=lambda k: k[4][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "semester":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_code": course_code.replace("_", " ")})],
                key=lambda k: k[11][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_title":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_code": course_code.replace("_", " ")})],
                key=lambda k: k[3][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "professors":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_code": course_code.replace("_", " ")})],
                key=lambda k: k[9][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "locations":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_code": course_code.replace("_", " ")})],
                key=lambda k: k[6][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "schedules":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"course_code": course_code.replace("_", " ")})],
                key=lambda k: k[10][1])
            return render_template('courses.html', output=output)
        else:
            courses = mongo.db.courselist
            output = [sorted(c.items()) for c in
                      courses.find({"course_code": course_code.replace("_", " ")})]
            return render_template('courses.html', output=output)
    courses = mongo.db.courselist
    output = [sorted(c.items()) for c in courses.find({"course_code": course_code.replace("_", " ")})]
    return render_template('courses.html', output=output)


@app.route('/professors/<string:professors>')
def get_courses_by_professor(professors):
    search_query = request.args.get('search', None)
    if search_query is not None:
        mongo.db.courselist.drop_indexes()
        mongo.db.courselist.create_index([("$**", "text")], name="textScore")
        cursor = mongo.db.courselist.find({'$text': {'$search': search_query.replace("+", " ")}},
                                          {'score': {'$meta': 'textScore'}})
        cursor.sort([('score', {'$meta': 'textScore'})])
        output = list(sorted(dict(c).items()) for c in cursor)
        for course in output:
            del course[11]
        if len(output) >= 1:
            return render_template('courses.html', output=output)
    sorted_query = request.args.get('sort', None)
    if sorted_query is not None:
        courses = mongo.db.courselist
        if sorted_query == "course_registration_number":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("_", " ")})],
                key=lambda k: k[2][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_code":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("_", " ")})],
                key=lambda k: k[1][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "new_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("_", " ")})],
                key=lambda k: k[7][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "old_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("_", " ")})],
                key=lambda k: k[8][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "department":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("_", " ")})],
                key=lambda k: k[4][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "semester":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("_", " ")})],
                key=lambda k: k[11][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_title":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("_", " ")})],
                key=lambda k: k[3][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "professors":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("_", " ")})],
                key=lambda k: k[9][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "locations":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("_", " ")})],
                key=lambda k: k[6][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "schedules":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("_", " ")})],
                key=lambda k: k[10][1])
            return render_template('courses.html', output=output)
        else:
            courses = mongo.db.courselist
            output = [sorted(c.items()) for c in
                      courses.find({"professors": professors.replace("_", " ")})]
            return render_template('courses.html', output=output)
    courses = mongo.db.courselist
    output = [sorted(c.items()) for c in courses.find({"professors": professors.replace("_", " ")})]
    return render_template('courses.html', output=output)


@app.route('/locations/<string:locations>')
def get_courses_by_location(locations):
    search_query = request.args.get('search', None)
    if search_query is not None:
        mongo.db.courselist.drop_indexes()
        mongo.db.courselist.create_index([("$**", "text")], name="textScore")
        cursor = mongo.db.courselist.find({'$text': {'$search': search_query.replace("+", " ")}},
                                          {'score': {'$meta': 'textScore'}})
        cursor.sort([('score', {'$meta': 'textScore'})])
        output = list(sorted(dict(c).items()) for c in cursor)
        for course in output:
            del course[11]
        if len(output) >= 1:
            return render_template('courses.html', output=output)
    sorted_query = request.args.get('sort', None)
    if sorted_query is not None:
        courses = mongo.db.courselist
        if sorted_query == "course_registration_number":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"locations": locations.replace("_", " ")})],
                key=lambda k: k[2][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_code":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"locations": locations.replace("_", " ")})],
                key=lambda k: k[1][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "new_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"locations": locations.replace("_", " ")})],
                key=lambda k: k[7][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "old_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"locations": locations.replace("_", " ")})],
                key=lambda k: k[8][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "department":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"locations": locations.replace("_", " ")})],
                key=lambda k: k[4][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "semester":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"locations": locations.replace("_", " ")})],
                key=lambda k: k[11][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_title":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"locations": locations.replace("_", " ")})],
                key=lambda k: k[3][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "professors":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"locations": locations.replace("_", " ")})],
                key=lambda k: k[9][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "locations":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"locations": locations.replace("_", " ")})],
                key=lambda k: k[6][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "schedules":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"locations": locations.replace("_", " ")})],
                key=lambda k: k[10][1])
            return render_template('courses.html', output=output)
        else:
            courses = mongo.db.courselist
            output = [sorted(c.items()) for c in
                      courses.find({"locations": locations.replace("_", " ")})]
            return render_template('courses.html', output=output)
    courses = mongo.db.courselist
    output = [sorted(c.items()) for c in courses.find({"locations": locations.replace("_", " ")})]
    return render_template('courses.html', output=output)


@app.route('/all')
def get_all_courses():
    search_query = request.args.get('search', None)
    if search_query is not None:
        mongo.db.courselist.drop_indexes()
        mongo.db.courselist.create_index([("$**", "text")], name="textScore")
        cursor = mongo.db.courselist.find({'$text': {'$search': search_query.replace("+", " ")}}, {'score': {'$meta': 'textScore'}})
        cursor.sort([('score', {'$meta': 'textScore'})])
        output = list(sorted(dict(c).items()) for c in cursor)
        for course in output:
            del course[11]
        if len(output) >= 1:
            return render_template('courses.html', output=output)
    sorted_query = request.args.get('sort', None)
    if sorted_query is not None:
        courses = mongo.db.courselist
        if sorted_query == "course_registration_number":
            output = sorted([sorted(c.items()) for c in courses.find()], key=lambda k: k[2][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_code":
            output = sorted([sorted(c.items()) for c in courses.find()], key=lambda k: k[1][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "new_distributions":
            output = sorted([sorted(c.items()) for c in courses.find()], key=lambda k: k[7][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "old_distributions":
            output = sorted([sorted(c.items()) for c in courses.find()], key=lambda k: k[8][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "department":
            output = sorted([sorted(c.items()) for c in courses.find()], key=lambda k: k[4][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "semester":
            output = sorted([sorted(c.items()) for c in courses.find()], key=lambda k: k[11][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_title":
            output = sorted([sorted(c.items()) for c in courses.find()], key=lambda k: k[3][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "professors":
            output = sorted([sorted(c.items()) for c in courses.find()], key=lambda k: k[9][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "locations":
            output = sorted([sorted(c.items()) for c in courses.find()], key=lambda k: k[6][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "schedules":
            output = sorted([sorted(c.items()) for c in courses.find()], key=lambda k: k[10][1])
            return render_template('courses.html', output=output)
        else:
            courses = mongo.db.courselist
            output = [sorted(c.items()) for c in courses.find()]
            return render_template('courses.html', output=output)
    courses = mongo.db.courselist
    output = [sorted(c.items()) for c in courses.find()]
    return render_template('courses.html', output=output)


@app.route('/semesters')
def get_semesters():
    search_query = request.args.get('search', None)
    all_semesters = ["fall2014", "spring2015", "fall2015", "spring2016", "fall2016", "spring2017", "current"]
    if search_query is not None:
        semesters = [semester for semester in all_semesters if search_query.replace("+", " ") in semester]
        return render_template('semesters.html', output=semesters)
    return render_template('semesters.html', output=all_semesters)


@app.route('/semesters/<string:semester>')
def get_deparments_by_semester(semester):
    search_query = request.args.get('search', None)
    courses = mongo.db.courselist
    all_departments = sorted(set([course_dict["department"] for course_dict in courses.find({"season": semester})]))
    if search_query is not None:
        departments = [department for department in all_departments if search_query.replace("+", " ") in department]
        return render_template('departments.html', output=departments)
    return render_template('departments.html', output=all_departments)


@app.route('/semesters/<string:semester>/<string:department>')
def get_courses_by_department_by_semester(semester, department):
    search_query = request.args.get('search', None)
    if search_query is not None:
        mongo.db.courselist.drop_indexes()
        mongo.db.courselist.create_index([("$**", "text")], name="textScore")
        cursor = mongo.db.courselist.find({'$text': {'$search': search_query.replace("+", " ")}},
                                          {'score': {'$meta': 'textScore'}})
        cursor.sort([('score', {'$meta': 'textScore'})])
        output = list(sorted(dict(c).items()) for c in cursor if c["department"] == department and c["season"] == semester)
        for course in output:
            del course[11]
        if len(output) >= 1:
            return render_template('courses.html', output=output)
    sorted_query = request.args.get('sort', None)
    if sorted_query is not None:
        courses = mongo.db.courselist
        if sorted_query == "course_registration_number":
            output = sorted([sorted(c.items()) for c in courses.find({"department": department}) if c["season"] == semester], key=lambda k: k[2][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_code":
            output = sorted([sorted(c.items()) for c in courses.find({"department": department}) if c["season"] == semester], key=lambda k: k[1][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "new_distributions":
            output = sorted([sorted(c.items()) for c in courses.find({"department": department}) if c["season"] == semester], key=lambda k: k[7][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "old_distributions":
            output = sorted([sorted(c.items()) for c in courses.find({"department": department}) if c["season"] == semester], key=lambda k: k[8][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "department":
            output = sorted([sorted(c.items()) for c in courses.find({"department": department}) if c["season"] == semester], key=lambda k: k[4][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "semester":
            output = sorted([sorted(c.items()) for c in courses.find({"department": department}) if c["season"] == semester], key=lambda k: k[11][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_title":
            output = sorted([sorted(c.items()) for c in courses.find({"department": department}) if c["season"] == semester], key=lambda k: k[3][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "professors":
            output = sorted([sorted(c.items()) for c in courses.find({"department": department}) if c["season"] == semester], key=lambda k: k[9][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "locations":
            output = sorted([sorted(c.items()) for c in courses.find({"department": department}) if c["season"] == semester], key=lambda k: k[6][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "schedules":
            output = sorted([sorted(c.items()) for c in courses.find({"department": department}) if c["season"] == semester], key=lambda k: k[10][1])
            return render_template('courses.html', output=output)
        else:
            courses = mongo.db.courselist
            output = [sorted(c.items()) for c in courses.find({"department": department}) if c["season"] == semester]
            return render_template('courses.html', output=output)
    courses = mongo.db.courselist
    output = [sorted(c.items()) for c in courses.find({"department": department}) if c["season"] == semester]
    return render_template('courses.html', output=output)


@app.route('/departments')
def get_departments():
    search_query = request.args.get('search', None)
    courses = mongo.db.courselist
    all_departments = sorted(set([course_dict["department"] for course_dict in courses.find()]))
    if search_query is not None:
        departments = [department for department in all_departments if search_query.replace("+", " ") in department]
        return render_template('departments.html', output=departments)
    return render_template('departments.html', output=all_departments)


@app.route('/departments/<string:department>')
def get_courses_by_department(department):
    search_query = request.args.get('search', None)
    if search_query is not None:
        mongo.db.courselist.drop_indexes()
        mongo.db.courselist.create_index([("$**", "text")], name="textScore")
        cursor = mongo.db.courselist.find({'$text': {'$search': search_query.replace("+", " ")}},
                                          {'score': {'$meta': 'textScore'}})
        cursor.sort([('score', {'$meta': 'textScore'})])
        output = list(sorted(dict(c).items()) for c in cursor if c["department"] == department)
        for course in output:
            del course[11]
        if len(output) >= 1:
            return render_template('courses.html', output=output)
    sorted_query = request.args.get('sort', None)
    if sorted_query is not None:
        courses = mongo.db.courselist
        if sorted_query == "course_registration_number":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"department": department})],
                key=lambda k: k[2][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_code":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"department": department})],
                key=lambda k: k[1][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "new_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"department": department})],
                key=lambda k: k[7][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "old_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"department": department})],
                key=lambda k: k[8][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "department":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"department": department})],
                key=lambda k: k[4][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "semester":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"department": department})],
                key=lambda k: k[11][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_title":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"department": department})],
                key=lambda k: k[3][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "professors":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"department": department})],
                key=lambda k: k[9][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "locations":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"department": department})],
                key=lambda k: k[6][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "schedules":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"department": department})],
                key=lambda k: k[10][1])
            return render_template('courses.html', output=output)
        else:
            courses = mongo.db.courselist
            output = [sorted(c.items()) for c in courses.find({"department": department})]
            return render_template('courses.html', output=output)
    courses = mongo.db.courselist
    output = [sorted(c.items()) for c in courses.find({"department": department})]
    return render_template('courses.html', output=output)


@app.route('/api/courses', methods=['GET'])
def api_get_all_courses():
    courses = mongo.db.courselist
    output = [{'course_code': c['course_code'],
               'course_registration_number': c['course_registration_number'],
               'course_title': c['course_title'],
               'department': c['department'],
               'description': c['description'],
               'locations': c['locations'],
               'new_distributions': c['new_distributions'],
               'old_distributions': c['old_distributions'],
               'professors': c['professors'],
               'schedules': c['schedules'],
               'season': c['season'],
               'url': c['url']} for c in courses.find()]
    return jsonify({'result': output})


@app.route('/api/department/<string:department>', methods=['GET'])
def api_get_courses_by_department(department):
    courses = mongo.db.courselist
    courselist = courses.find({'department': department})
    output = [{'course_code': c['course_code'],
               'course_registration_number': c['course_registration_number'],
               'course_title': c['course_title'],
               'department': c['department'],
               'description': c['description'],
               'locations': c['locations'],
               'new_distributions': c['new_distributions'],
               'old_distributions': c['old_distributions'],
               'professors': c['professors'],
               'schedules': c['schedules'],
               'season': c['season'],
               'url': c['url']} for c in courselist]
    if len(output) >= 1:
        final_output = output
    else:
        final_output = "No courses exist in that department."
    return jsonify({'result': final_output})


@app.route('/api/distribution/<string:distribution>', methods=['GET'])
def api_get_courses_by_distribution(distribution):
    courses = mongo.db.courselist
    courselist = courses.find({'old_distributions': distribution})
    output = [{'course_code': c['course_code'],
               'course_registration_number': c['course_registration_number'],
               'course_title': c['course_title'],
               'department': c['department'],
               'description': c['description'],
               'locations': c['locations'],
               'new_distributions': c['new_distributions'],
               'old_distributions': c['old_distributions'],
               'professors': c['professors'],
               'schedules': c['schedules'],
               'season': c['season'],
               'url': c['url']} for c in courselist]
    if len(output) >= 1:
        final_output = output
    else:
        final_output = "No courses exist with that distribution."
    return jsonify({'result': final_output})


@app.route('/api/semester/<string:season>', methods=['GET'])
def api_get_courses_by_semester(season):
    courses = mongo.db.courselist
    courselist = courses.find({'season': season})
    output = [{'course_code': c['course_code'],
               'course_registration_number': c['course_registration_number'],
               'course_title': c['course_title'],
               'department': c['department'],
               'description': c['description'],
               'locations': c['locations'],
               'new_distributions': c['new_distributions'],
               'old_distributions': c['old_distributions'],
               'professors': c['professors'],
               'schedules': c['schedules'],
               'season': c['season'],
               'url': c['url']} for c in courselist]
    if len(output) >= 1:
        final_output = output
    else:
        final_output = "No courses exist in that semester."
    return jsonify({'result': final_output})


@app.route('/api/crn/<int:course_registration_number>', methods=['GET'])
def api_get_courses_by_crn(course_registration_number):
    courses = mongo.db.courselist
    courselist = courses.find({'course_registration_number': course_registration_number})
    output = [{'course_code': c['course_code'],
               'course_registration_number': c['course_registration_number'],
               'course_title': c['course_title'],
               'department': c['department'],
               'description': c['description'],
               'locations': c['locations'],
               'new_distributions': c['new_distributions'],
               'old_distributions': c['old_distributions'],
               'professors': c['professors'],
               'schedules': c['schedules'],
               'season': c['season'],
               'url': c['url']} for c in courselist]
    if len(output) >= 1:
        final_output = output
    else:
        final_output = "No courses exist with that course registration number."
    return jsonify({'result': final_output})


@app.route('/api/course_code/<string:course_code>', methods=['GET'])
def api_get_courses_by_code(course_code):
    courses = mongo.db.courselist
    courselist = courses.find({'course_code': course_code.replace("_", " ")})
    output = [{'course_code': c['course_code'],
               'course_registration_number': c['course_registration_number'],
               'course_title': c['course_title'],
               'department': c['department'],
               'description': c['description'],
               'locations': c['locations'],
               'new_distributions': c['new_distributions'],
               'old_distributions': c['old_distributions'],
               'professors': c['professors'],
               'schedules': c['schedules'],
               'season': c['season'],
               'url': c['url']} for c in courselist]
    if len(output) >= 1:
        final_output = output
    else:
        final_output = "No courses exist with that course code."
    return jsonify({'result': final_output})


@app.route('/api/professors/<string:professors>', methods=['GET'])
def api_get_courses_by_professor(professors):
    courses = mongo.db.courselist
    courselist = courses.find({'professors': professors.replace("_", " ")})
    output = [{'course_code': c['course_code'],
               'course_registration_number': c['course_registration_number'],
               'course_title': c['course_title'],
               'department': c['department'],
               'description': c['description'],
               'locations': c['locations'],
               'new_distributions': c['new_distributions'],
               'old_distributions': c['old_distributions'],
               'professors': c['professors'],
               'schedules': c['schedules'],
               'season': c['season'],
               'url': c['url']} for c in courselist]
    if len(output) >= 1:
        final_output = output
    else:
        final_output = "No courses exist which have been instructed by that professor."
    return jsonify({'result': final_output})


@app.route('/api/locations/<string:location>', methods=['GET'])
def api_get_courses_by_location(location):
    courses = mongo.db.courselist
    courselist = courses.find({'locations': location.replace("_", " ")})
    output = [{'course_code': c['course_code'],
               'course_registration_number': c['course_registration_number'],
               'course_title': c['course_title'],
               'department': c['department'],
               'description': c['description'],
               'locations': c['locations'],
               'new_distributions': c['new_distributions'],
               'old_distributions': c['old_distributions'],
               'professors': c['professors'],
               'schedules': c['schedules'],
               'season': c['season'],
               'url': c['url']} for c in courselist]
    if len(output) >= 1:
        final_output = output
    else:
        final_output = "No courses exist which have been instructed in that location."
    return jsonify({'result': final_output})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=False)
