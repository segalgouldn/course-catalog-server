# Noah Segal-Gould, Summer 2017

from flask import url_for, session, redirect, request, render_template, jsonify, Flask
from flask_pymongo import PyMongo

import bcrypt


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'courselist'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/courselist'

mongo = PyMongo(app)


@app.route('/user/<path:username>')
def get_courses_for_user(username):
    users = mongo.db.users
    login_user = users.find_one({'name': username})
    if login_user:
        courses = login_user.get("courses", None)
        if courses:
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
                    return render_template('courses.html', output=output, username=username)
            sorted_query = request.args.get('sort', None)
            if sorted_query is not None:
                if sorted_query == "course_registration_number":
                    output = sorted([sorted(c.items()) for c in courses], key=lambda k: k[2][1])
                    return render_template('courses.html', output=output, username=username)
                elif sorted_query == "course_code":
                    output = sorted([sorted(c.items()) for c in courses], key=lambda k: k[1][1])
                    return render_template('courses.html', output=output, username=username)
                elif sorted_query == "new_distributions":
                    output = sorted([sorted(c.items()) for c in courses], key=lambda k: k[7][1])
                    return render_template('courses.html', output=output, username=username)
                elif sorted_query == "old_distributions":
                    output = sorted([sorted(c.items()) for c in courses], key=lambda k: k[8][1])
                    return render_template('courses.html', output=output, username=username)
                elif sorted_query == "department":
                    output = sorted([sorted(c.items()) for c in courses], key=lambda k: k[4][1])
                    return render_template('courses.html', output=output, username=username)
                elif sorted_query == "semester":
                    output = sorted([sorted(c.items()) for c in courses], key=lambda k: k[11][1])
                    return render_template('courses.html', output=output, username=username)
                elif sorted_query == "course_title":
                    output = sorted([sorted(c.items()) for c in courses], key=lambda k: k[3][1])
                    return render_template('courses.html', output=output, username=username)
                elif sorted_query == "professors":
                    output = sorted([sorted(c.items()) for c in courses], key=lambda k: k[9][1])
                    return render_template('courses.html', output=output, username=username)
                elif sorted_query == "locations":
                    output = sorted([sorted(c.items()) for c in courses], key=lambda k: k[6][1])
                    return render_template('courses.html', output=output, username=username)
                elif sorted_query == "schedules":
                    output = sorted([sorted(c.items()) for c in courses], key=lambda k: k[10][1])
                    return render_template('courses.html', output=output, username=username)
                else:
                    output = [sorted(c.items()) for c in courses]
                    return render_template('courses.html', output=output, username=username)
            output = [sorted(c.items()) for c in courses]
            return render_template('courses.html', output=output, username=username)
        if 'username' in session:
            return render_template('error.html', error="You haven\'t added any courses yet.", username=session['username'])
        return render_template('error.html', error="That user hasn\'t added any courses yet.")
    return render_template('error.html', error="There does not exist a user with that name.")


@app.route('/add_course/<ObjectId:course_id>')
def add_course_to_user_by_id(course_id):
    if 'username' in session:
        users = mongo.db.users
        courses = mongo.db.courselist
        login_user = users.find_one({'name': session['username']})
        specific_course = courses.find_one({'_id': course_id})
        if specific_course:
            if specific_course not in login_user["courses"]:
                users.update({"_id": login_user["_id"]}, {'$push': {'courses': specific_course}})
                return redirect(url_for('get_courses_for_user', username=session['username']))
            return render_template('error.html', error="That course is already in your favorites.", username=session['username'])
        return render_template('error.html', error="A course with that ID does not exist.", username=session['username'])
    return render_template('error.html', error="Please log in to add courses to your favorites.")


@app.route('/remove_course/<ObjectId:course_id>')
def remove_course_from_user_by_id(course_id):
    if 'username' in session:
        users = mongo.db.users
        courses = mongo.db.courselist
        login_user = users.find_one({'name': session['username']})
        specific_course = courses.find_one({'_id': course_id})
        if specific_course:
            if specific_course in login_user["courses"]:
                users.update({"_id": login_user["_id"]}, {'$pull': {'courses': specific_course}})
                return redirect(url_for('get_courses_for_user', username=session['username']))
            return render_template('error.html', error="That course is not already in your favorites.", username=session['username'])
        return render_template('error.html', error="A course with that ID does not exist.", username=session['username'])
    return render_template('error.html', error="Please log in to add courses to your favorites.")


@app.route('/')
def index():
    if 'username' in session:
        return render_template('home.html', username=session['username'])

    return render_template('home.html')


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return render_template("error.html", error='Invalid username/password combination.')


@app.route('/logoff')
def logoff():
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password': hashpass, 'courses': []})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return render_template("error.html", error='That username already exists.')

    return render_template('register.html')


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


@app.route('/course_codes/<path:course_code>')
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


@app.route('/professors/<path:professors>')
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
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("%20", " ").replace("%2F", "/")})],
                key=lambda k: k[2][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_code":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("%20", " ").replace("%2F", "/")})],
                key=lambda k: k[1][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "new_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("%20", " ").replace("%2F", "/")})],
                key=lambda k: k[7][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "old_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("%20", " ").replace("%2F", "/")})],
                key=lambda k: k[8][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "department":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("%20", " ").replace("%2F", "/")})],
                key=lambda k: k[4][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "semester":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("%20", " ").replace("%2F", "/")})],
                key=lambda k: k[11][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_title":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("%20", " ").replace("%2F", "/")})],
                key=lambda k: k[3][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "professors":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("%20", " ").replace("%2F", "/")})],
                key=lambda k: k[9][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "locations":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("%20", " ").replace("%2F", "/")})],
                key=lambda k: k[6][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "schedules":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"professors": professors.replace("%20", " ").replace("%2F", "/")})],
                key=lambda k: k[10][1])
            return render_template('courses.html', output=output)
        else:
            courses = mongo.db.courselist
            output = [sorted(c.items()) for c in
                      courses.find({"professors": professors.replace("%20", " ").replace("%2F", "/")})]
            return render_template('courses.html', output=output)
    courses = mongo.db.courselist
    output = [sorted(c.items()) for c in courses.find({"professors": professors.replace("%20", " ").replace("%2F", "/")})]
    return render_template('courses.html', output=output)


@app.route('/locations/<path:locations>')
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


@app.route('/old_distributions/<path:old_distributions>')
def get_courses_by_old_distributions(old_distributions):
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
                [sorted(c.items()) for c in courses.find({"old_distributions": old_distributions.replace("_", " ")})],
                key=lambda k: k[2][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_code":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"old_distributions": old_distributions.replace("_", " ")})],
                key=lambda k: k[1][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "new_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"old_distributions": old_distributions.replace("_", " ")})],
                key=lambda k: k[7][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "old_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"old_distributions": old_distributions.replace("_", " ")})],
                key=lambda k: k[8][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "department":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"old_distributions": old_distributions.replace("_", " ")})],
                key=lambda k: k[4][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "semester":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"old_distributions": old_distributions.replace("_", " ")})],
                key=lambda k: k[11][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_title":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"old_distributions": old_distributions.replace("_", " ")})],
                key=lambda k: k[3][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "professors":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"old_distributions": old_distributions.replace("_", " ")})],
                key=lambda k: k[9][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "locations":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"old_distributions": old_distributions.replace("_", " ")})],
                key=lambda k: k[6][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "schedules":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"old_distributions": old_distributions.replace("_", " ")})],
                key=lambda k: k[10][1])
            return render_template('courses.html', output=output)
        else:
            courses = mongo.db.courselist
            output = [sorted(c.items()) for c in
                      courses.find({"old_distributions": old_distributions.replace("_", " ")})]
            return render_template('courses.html', output=output)
    courses = mongo.db.courselist
    output = [sorted(c.items()) for c in courses.find({"old_distributions": old_distributions.replace("_", " ")})]
    return render_template('courses.html', output=output)


@app.route('/new_distributions/<path:new_distributions>')
def get_courses_by_new_distributions(new_distributions):
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
                [sorted(c.items()) for c in courses.find({"new_distributions": new_distributions.replace("_", " ")})],
                key=lambda k: k[2][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_code":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"new_distributions": new_distributions.replace("_", " ")})],
                key=lambda k: k[1][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "new_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"new_distributions": new_distributions.replace("_", " ")})],
                key=lambda k: k[7][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "old_distributions":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"new_distributions": new_distributions.replace("_", " ")})],
                key=lambda k: k[8][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "department":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"new_distributions": new_distributions.replace("_", " ")})],
                key=lambda k: k[4][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "semester":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"new_distributions": old_distributions.replace("_", " ")})],
                key=lambda k: k[11][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "course_title":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"new_distributions": new_distributions.replace("_", " ")})],
                key=lambda k: k[3][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "professors":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"new_distributions": new_distributions.replace("_", " ")})],
                key=lambda k: k[9][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "locations":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"new_distributions": new_distributions.replace("_", " ")})],
                key=lambda k: k[6][1])
            return render_template('courses.html', output=output)
        elif sorted_query == "schedules":
            output = sorted(
                [sorted(c.items()) for c in courses.find({"new_distributions": new_distributions.replace("_", " ")})],
                key=lambda k: k[10][1])
            return render_template('courses.html', output=output)
        else:
            courses = mongo.db.courselist
            output = [sorted(c.items()) for c in
                      courses.find({"old_distributions": new_distributions.replace("_", " ")})]
            return render_template('courses.html', output=output)
    courses = mongo.db.courselist
    output = [sorted(c.items()) for c in courses.find({"new_distributions": new_distributions.replace("_", " ")})]
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


@app.route('/professors')
def get_professors():
    search_query = request.args.get('search', None)
    courses = mongo.db.courselist
    all_professors = sorted(set([course_dict["professors"] for course_dict in courses.find()]))
    if search_query is not None:
        professors = [professor for professor in all_professors if search_query.replace("+", " ") in professor]
        return render_template('professors.html', output=professors)
    return render_template('professors.html', output=all_professors)


@app.route('/locations')
def get_locations():
    search_query = request.args.get('search', None)
    courses = mongo.db.courselist
    all_locations = sorted(set([course_dict["locations"] for course_dict in courses.find()]))
    if search_query is not None:
        locations = [location for location in all_locations if search_query.replace("+", " ") in location]
        return render_template('locations.html', output=locations)
    return render_template('locations.html', output=all_locations)


@app.route('/course_codes')
def get_course_codes():
    search_query = request.args.get('search', None)
    courses = mongo.db.courselist
    all_course_codes = sorted(set([course_dict["course_code"] for course_dict in courses.find()]))
    if search_query is not None:
        course_codes = [course_code for course_code in all_course_codes if search_query.replace("+", " ") in course_code]
        return render_template('course_codes.html', output=course_codes)
    return render_template('course_codes.html', output=all_course_codes)


@app.route('/old_distributions')
def get_old_distributions():
    search_query = request.args.get('search', None)
    courses = mongo.db.courselist
    all_old_distributions = sorted(set([course_dict["old_distributions"] for course_dict in courses.find()]))
    if search_query is not None:
        old_distributions = [old_distribution for old_distribution in all_old_distributions if search_query.replace("+", " ") in old_distribution]
        return render_template('old_distributions.html', output=old_distributions)
    return render_template('old_distributions.html', output=all_old_distributions)


@app.route('/new_distributions')
def get_new_distributions():
    search_query = request.args.get('search', None)
    courses = mongo.db.courselist
    all_new_distributions = sorted(set([course_dict["new_distributions"] for course_dict in courses.find()]))
    if search_query is not None:
        new_distributions = [new_distribution for new_distribution in all_new_distributions if search_query.replace("+", " ") in new_distribution]
        return render_template('new_distributions.html', output=new_distributions)
    return render_template('new_distributions.html', output=all_new_distributions)


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


@app.route('/api/distribution/<path:distribution>', methods=['GET'])
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


@app.route('/api/course_codes/<path:course_code>', methods=['GET'])
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


@app.route('/api/professors/<path:professors>', methods=['GET'])
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
    app.secret_key = 'thisisatest'
    app.run(host='0.0.0.0', port=5555, debug=False)
