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
            return render_template('index.html', output=output)
    courses = mongo.db.courselist
    output = [sorted(c.items()) for c in courses.find()]
    return render_template('index.html', output=output)


@app.route('/api/courses', methods=['GET'])
def get_all_courses():
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
def get_courses_by_department(department):
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
def get_courses_by_distribution(distribution):
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
def get_semester_by_season(season):
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
def get_courses_by_crn(course_registration_number):
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
def get_courses_by_code(course_code):
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
def get_courses_by_professor(professors):
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
def get_courses_by_location(location):
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
    app.run(debug=False)
