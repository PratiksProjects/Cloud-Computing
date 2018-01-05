#!flask/bin/python
from __future__ import print_function
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask import render_template, redirect


import sqlite3

import sys
    
app = Flask(__name__, static_url_path="")

class Dynamo(object):
    pass
    
def get_student_details(student_id):
    conn = sqlite3.connect('ece4813-lab3-college.sqlite')
    results = conn.execute("SELECT * FROM student WHERE sID = (?);",(student_id,))
    item = results.fetchone()

    student = Dynamo()
    student.ID = item[0]
    student.Name = item[1]
    student.LastName = item[2]
    student.Major = item[3]
    student.GPA = item[4]
    conn.close()
    
    return student
    
@app.route('/', methods=['GET'])
def home_page():
    conn = sqlite3.connect('ece4813-lab3-college.sqlite')
    results = conn.execute("SELECT * FROM student;");
    
    studentlist=[]
    for item in results:
        student={}
        student['ID'] = item[0]
        student['Name'] = item[1]
        student['LastName'] = item[2]
        studentlist.append(student)
    
    conn.close()        
    return render_template('index.html', students=studentlist)


@app.route('/student/add', methods=['GET', 'POST'])
def student_add_page():
    if request.method == 'POST':    
        result = request.form

        conn = sqlite3.connect('ece4813-lab3-college.sqlite')
        statement = "INSERT INTO Student(sId, Name, LastName, Major, GPA) VALUES ("+\
                    request.form['sId']+", '"+\
                    request.form['Name']+"', '"+\
                    request.form['LastName']+"', '"+\
                    request.form['Major']+"', "+\
                    request.form['GPA']+");";
        
        result = conn.execute(statement);
        conn.commit()
        conn.close()

        return redirect('/')
    else:
        return render_template('add.html')


@app.route('/student/delete/<int:student_id>', methods=['GET'])
def delete_student_process(student_id):
    
    conn = sqlite3.connect('ece4813-lab3-college.sqlite')
    results = conn.execute("DELETE FROM Student WHERE sId="+str(student_id)+";");
    conn.commit()
    
    return redirect('/')

@app.route('/student/details/<int:student_id>', methods=['GET'])
def student_details_page (student_id):
    student = get_student_details(student_id)
    return render_template('details.html', student = student)
    
@app.route('/student/update/<int:student_id>', methods=['GET', 'POST'])
def student_update(student_id):
    if request.method == 'POST':    
        result = request.form

        conn = sqlite3.connect('ece4813-lab3-college.sqlite')
        statement = "UPDATE Student SET sID = (?), Name = (?), LastName =(?), Major = (?), GPA = (?) WHERE sID = (?)"
        
        result = conn.execute(statement,(request.form['sId'],request.form['Name'],request.form['LastName'],request.form['Major'],request.form['GPA'], student_id));
        conn.commit()
        conn.close()

        return redirect('/')
    else:
        student = get_student_details(student_id)
        print(student)
        return render_template('update.html', student = student)

@app.route('/course', methods=['GET', 'POST'])
def courses_page():
    conn = sqlite3.connect('ece4813-lab3-college.sqlite')
    results = conn.execute("SELECT * FROM course;");
    
    courselist=[]
    for item in results:
        course={}
        course['ID'] = item[0]
        course['Name'] = item[1]
        courselist.append(course)
        
    results = conn.execute("SELECT * FROM student;");
    studentlist=[]
    for item in results:
        student={}
        student['ID'] = item[0]
        studentlist.append(student)
        
    conn.close()
    return render_template('courses.html', courses = courselist, students = studentlist)

@app.route('/course/add', methods=['POST'])
def add_course():
    result = request.form

    conn = sqlite3.connect('ece4813-lab3-college.sqlite')
    statement = "INSERT INTO Course(cId, cName) VALUES ((?),(?));"

    result = conn.execute(statement,(request.form['courseID'],request.form['courseName'],))
    conn.commit()
    conn.close()
    
    return redirect('/course')

@app.route('/course/addStudent', methods=['POST'])
def add_student():
    result = request.form

    conn = sqlite3.connect('ece4813-lab3-college.sqlite')
    statement = "INSERT INTO Takes(sId, cId, semester, year) VALUES ((?),(?),(?),(?));"

    result = conn.execute(statement,(request.form['studentID'],request.form['courses'],request.form['semester'],request.form['year'],))
    conn.commit()
    conn.close()
    
    return redirect('/course')
    
@app.route('/course/enrolled/<int:course_id>', methods=['GET'])
def get_enrolled_students(course_id):

    conn = sqlite3.connect('ece4813-lab3-college.sqlite')
    statement = "SELECT Takes.cId, Takes.sId, Takes.semester, Takes.year, Student.Name, Student.LastName FROM Takes Join Student ON Student.sId = Takes.sId WHERE Takes.cId = (?);"

    results = conn.execute(statement,(course_id,))
    studentlist=[]
    
    for item in results:
        student={}
        student['ID'] = item[1]
        student['semester'] = item[2]
        student['year'] = item[3]
        student['name'] = item[4]
        student['lastName'] = item[5]
        studentlist.append(student)
        
    conn.commit()
    conn.close()
    
    return render_template('enrolled.html', students = studentlist, course_id = course_id)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
