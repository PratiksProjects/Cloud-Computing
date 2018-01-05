from texttable import Texttable
import MySQLdb

USERNAME = 'root'
PASSWORD = 'password'
DB_NAME = 'DBECE4813'

print "Connecting to RDS instance"

#Insert host url from RDS
conn = MySQLdb.connect (	host = "",
                        	user = USERNAME,
                        	passwd = PASSWORD,
                        	db = DB_NAME, 
							port = 3306
						)

print "Connected to RDS instance"

cursor = conn.cursor ()
cursor.execute ("SELECT VERSION()")
row = cursor.fetchone ()
print "server version:", row[0]


print "\nCreating Table Student. Adding 5 Students to the table"
cursor.execute ("CREATE TABLE Student(sId INT NOT NULL, Name TEXT NOT NULL, LastName TEXT NOT NULL, Major TEXT NOT NULL, GPA FLOAT, PRIMARY KEY (sId)) ")

cursor.execute ("INSERT INTO Student VALUES(100, 'John', 'Martin', 'CS', 3)")
cursor.execute ("INSERT INTO Student VALUES(101, 'David', 'Kennerly', 'ECE', 3.5)")
cursor.execute ("INSERT INTO Student VALUES(102, 'Bob', 'Reeves', 'CS', 3.9)")
cursor.execute ("INSERT INTO Student VALUES(103, 'Alex', 'Han', 'CS', 3.6)")
cursor.execute ("INSERT INTO Student VALUES(104, 'Martin', 'Lorenz', 'ECE', 3.1)")

cursor.execute("SELECT * FROM Student")
rows = cursor.fetchall()

print "\nPrinting Students:"

table = Texttable()
content_table = [['Student ID', 'Name', 'Last Name', 'Major', 'GPA']]

for row in rows:
	content_table.append([int(row[0]), row[1], row[2], row[3], row[4]])

table.add_rows(content_table)
print table.draw()

#print "\nDropping Table..."
#cursor.execute ("DROP TABLE Student")
#print "\nTable Dropped\n"

cursor.close()
conn.close()
