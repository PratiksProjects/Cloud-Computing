#!flask/bin/python
from __future__ import print_function
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask import render_template, redirect


import MySQLdb

import sys
    
app = Flask(__name__, static_url_path="")
USERNAME = 'root'
PASSWORD = 'password'
DB_NAME = 'DBECE4813'

#new class created as a dynamic class
class Dynamo(object):
    pass

#method which returns details of a student given student_id
def get_student_details(student_id):
    cur = MySQLdb.connect (host = "",
                                user = USERNAME,
                                passwd = PASSWORD,
                                db = DB_NAME, 
                                port = 3306
                            )
    conn = cur.cursor ()
    conn.execute("SELECT * FROM Student WHERE sID = %s;",(student_id,))
    item = conn.fetchone()

    student = Dynamo()
    student.ID = item[0]
    student.Name = item[1]
    student.LastName = item[2]
    student.Major = item[3]
    student.GPA = item[4]
    conn.close()
    
    return student
#home page shows list of all students
@app.route('/', methods=['GET'])
def home_page():
    cur = MySQLdb.connect (host = "",
                                user = USERNAME,
                                passwd = PASSWORD,
                                db = DB_NAME, 
                                port = 3306
                            )
    conn = cur.cursor ()
    conn.execute("SELECT * FROM Student;")
    results = conn.fetchall()
    studentlist=[]
    for item in results:
        student={}
        student['ID'] = item[0]
        student['Name'] = item[1]
        student['LastName'] = item[2]
        studentlist.append(student)
    
    conn.close()        
    return render_template('index.html', students=studentlist)

#route for adding a student into the database and view
@app.route('/student/add', methods=['GET', 'POST'])
def student_add_page():
    if request.method == 'POST':    
        result = request.form

        statement = "INSERT INTO Student(sId, Name, LastName, Major, GPA) VALUES ("+\
                    request.form['sId']+", '"+\
                    request.form['Name']+"', '"+\
                    request.form['LastName']+"', '"+\
                    request.form['Major']+"', "+\
                    request.form['GPA']+");";
        cur = MySQLdb.connect (host = "",
                            user = USERNAME,
                            passwd = PASSWORD,
                            db = DB_NAME, 
                            port = 3306
                        )
        conn = cur.cursor ()
        conn.execute(statement);
        cur.commit()
        conn.close()

        return redirect('/')
    else:
        return render_template('add.html')

#route for deleting a student
@app.route('/student/delete/<int:student_id>', methods=['GET'])
def delete_student_process(student_id):
    cur = MySQLdb.connect (host = "",
                                user = USERNAME,
                                passwd = PASSWORD,
                                db = DB_NAME, 
                                port = 3306
                            )
    conn = cur.cursor ()
    conn.execute("DELETE FROM Student WHERE sId="+str(student_id)+";");
    cur.commit()
    conn.close()
    
    return redirect('/')
#returns details of a particular student
@app.route('/student/details/<int:student_id>', methods=['GET'])
def student_details_page (student_id):
    student = get_student_details(student_id)
    return render_template('details.html', student = student)
#udpates student information
@app.route('/student/update/<int:student_id>', methods=['GET', 'POST'])
def student_update(student_id):
    if request.method == 'POST':    
        result = request.form
        cur = MySQLdb.connect (host = "",
                                    user = USERNAME,
                                    passwd = PASSWORD,
                                    db = DB_NAME, 
                                    port = 3306
                                )
        conn = cur.cursor ()
        statement = "UPDATE Student SET Name = %s, LastName = %s, Major = %s, GPA = %s WHERE sID = %s"
        
        result = conn.execute(statement,(request.form['Name'],request.form['LastName'],request.form['Major'],request.form['GPA'], student_id));
        cur.commit()
        conn.close()

        return redirect('/')
    else:
        student = get_student_details(student_id)
        return render_template('update.html', student = student)
#route listing all courses
@app.route('/course', methods=['GET', 'POST'])
def courses_page():
    cur = MySQLdb.connect (host = "",
                                user = USERNAME,
                                passwd = PASSWORD,
                                db = DB_NAME, 
                                port = 3306
                            )
    conn = cur.cursor ()
    conn.execute("SELECT * FROM Course;");
    results = conn.fetchall()
    courselist=[]
    for item in results:
        course={}
        course['ID'] = item[0]
        course['Name'] = item[1]
        courselist.append(course)
        
    conn.execute("SELECT * FROM Student;");
    results = conn.fetchall()
    studentlist=[]
    for item in results:
        student={}
        student['ID'] = item[0]
        studentlist.append(student)
        
    conn.close()
    return render_template('courses.html', courses = courselist, students = studentlist)
#route for adding a course
@app.route('/course/add', methods=['POST'])
def add_course():
    result = request.form
    cur = MySQLdb.connect (host = "",
                                user = USERNAME,
                                passwd = PASSWORD,
                                db = DB_NAME, 
                                port = 3306
                            )
    conn = cur.cursor ()
    statement = "INSERT INTO Course(cId, cName) VALUES (%s,%s);"

    conn.execute(statement,(request.form['courseID'],request.form['courseName'],))
    cur.commit()
    conn.close()
    
    return redirect('/course')
#route for adding a student to a course
@app.route('/course/addStudent', methods=['POST'])
def add_student():
    result = request.form
    cur = MySQLdb.connect (host = "",
                                user = USERNAME,
                                passwd = PASSWORD,
                                db = DB_NAME, 
                                port = 3306
                            )
    conn = cur.cursor ()
    statement = "INSERT INTO Takes(sId, cId, semester, year) VALUES (%s,%s,%s,%s);"

    conn.execute(statement,(request.form['studentID'],request.form['courses'],request.form['semester'],request.form['year'],))
    cur.commit()
    conn.close()
    
    return redirect('/course')
#route for students enrolled in a particular course
@app.route('/course/enrolled/<int:course_id>', methods=['GET'])
def get_enrolled_students(course_id):
    statement = "SELECT Takes.cId, Takes.sId, Takes.semester, Takes.year, Student.Name, Student.LastName FROM Takes Join Student ON Student.sId = Takes.sId WHERE Takes.cId = %s;"
    cur = MySQLdb.connect (host = "",
                                user = USERNAME,
                                passwd = PASSWORD,
                                db = DB_NAME, 
                                port = 3306
                            )
    conn = cur.cursor ()
    conn.execute(statement,(course_id,))
    results = conn.fetchall()
    studentlist=[]
    
    for item in results:
        student={}
        student['ID'] = item[1]
        student['semester'] = item[2]
        student['year'] = item[3]
        student['name'] = item[4]
        student['lastName'] = item[5]
        studentlist.append(student)
        
    cur.commit()
    conn.close()
    
    return render_template('enrolled.html', students = studentlist, course_id = course_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    
