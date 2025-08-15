##we will create sglite3 database locally
#we will inside some initial data (like student table)
#confirm that the table is created and the rows are inserted
##prepare the DB so we can later query it with langchain


import sqlite3
##create a student.db with a student table

#connect to or create a local sqlite DB file
connection= sqlite3.connect("student.db")

## create a cursor object to insert record, create table
cursor = connection.cursor()   ###ta k new table bna skain aur record insert kr skain is main


##now i will define a SQL statement to create table(if not exist)
 ##VARCHAR means variablelengthcharacterstring
table_info ='''

CREATE TABLE IF NOT EXISTS STUDENT(
    NAME VARCHAR(25),       
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INTEGER
    );
'''
##This execution will create STUDENT table
cursor.execute(table_info)

## we will be insurting some sample records 
# Insert Data Science Students
cursor.execute("INSERT INTO STUDENT VALUES('Malik95','Data Science','A',95)")
cursor.execute("INSERT INTO STUDENT VALUES('Bob','Data Science','B',88)")
cursor.execute("INSERT INTO STUDENT VALUES('Charlie','Data Science','A',72)")
cursor.execute("INSERT INTO STUDENT VALUES('Diana','Data Science','C',64)")
cursor.execute("INSERT INTO STUDENT VALUES('Ethan','Data Science','A',91)")

# Insert DevOps Students
cursor.execute("INSERT INTO STUDENT VALUES('Fiona','DevOps','A',78)")
cursor.execute("INSERT INTO STUDENT VALUES('George','DevOps','B',83)")
cursor.execute("INSERT INTO STUDENT VALUES('Hannah','DevOps','A',99)")
cursor.execute("INSERT INTO STUDENT VALUES('Ian','DevOps','C',56)")
cursor.execute("INSERT INTO STUDENT VALUES('Jade','DevOps','B',81)")

# Insert Marketing Students
cursor.execute("INSERT INTO STUDENT VALUES('Kevin','Marketing','A',92)")
cursor.execute("INSERT INTO STUDENT VALUES('Laura','Marketing','B',70)")
cursor.execute("INSERT INTO STUDENT VALUES('Martin','Marketing','C',66)")
cursor.execute("INSERT INTO STUDENT VALUES('Nina','Marketing','A',89)")
cursor.execute("INSERT INTO STUDENT VALUES('Oscar','Marketing','B',73)")

# Insert Sales Students
cursor.execute("INSERT INTO STUDENT VALUES('Paula','Sales','C',58)")
cursor.execute("INSERT INTO STUDENT VALUES('Quentin','Sales','B',79)")
cursor.execute("INSERT INTO STUDENT VALUES('Rebecca','Sales','A',90)")
cursor.execute("INSERT INTO STUDENT VALUES('Sam','Sales','B',67)")
cursor.execute("INSERT INTO STUDENT VALUES('Tara','Sales','C',54)")

# Insert Finance Students
cursor.execute("INSERT INTO STUDENT VALUES('Uma','Finance','A',88)")
cursor.execute("INSERT INTO STUDENT VALUES('Victor','Finance','A',93)")
cursor.execute("INSERT INTO STUDENT VALUES('Wendy','Finance','C',62)")
cursor.execute("INSERT INTO STUDENT VALUES('Xavier','Finance','B',77)")
cursor.execute("INSERT INTO STUDENT VALUES('Yvonne','Finance','A',100)")

# Insert HR Students
cursor.execute("INSERT INTO STUDENT VALUES('Zack','HR','C',48)")
cursor.execute("INSERT INTO STUDENT VALUES('Abel','HR','B',69)")
cursor.execute("INSERT INTO STUDENT VALUES('Bianca','HR','A',87)")
cursor.execute("INSERT INTO STUDENT VALUES('Caleb','HR','A',95)")
cursor.execute("INSERT INTO STUDENT VALUES('Denise','HR','C',60)")

# Insert IT Students
cursor.execute("INSERT INTO STUDENT VALUES('Ernest','IT','B',84)")
cursor.execute("INSERT INTO STUDENT VALUES('Fatima','IT','A',90)")
cursor.execute("INSERT INTO STUDENT VALUES('Gina','IT','B',75)")
cursor.execute("INSERT INTO STUDENT VALUES('Harvey','IT','C',53)")
cursor.execute("INSERT INTO STUDENT VALUES('Iris','IT','A',99)")

# Insert Management Students
cursor.execute("INSERT INTO STUDENT VALUES('Jonas','Management','B',76)")
cursor.execute("INSERT INTO STUDENT VALUES('Kylie','Management','C',65)")
cursor.execute("INSERT INTO STUDENT VALUES('Leon','Management','A',92)")
cursor.execute("INSERT INTO STUDENT VALUES('Macy','Management','B',80)")
cursor.execute("INSERT INTO STUDENT VALUES('Nick','Management','C',55)")

# Insert Operations Students
cursor.execute("INSERT INTO STUDENT VALUES('Olivia','Operations','A',85)")
cursor.execute("INSERT INTO STUDENT VALUES('Pavel','Operations','B',72)")
cursor.execute("INSERT INTO STUDENT VALUES('Rita','Operations','C',61)")
cursor.execute("INSERT INTO STUDENT VALUES('Soren','Operations','A',96)")
cursor.execute("INSERT INTO STUDENT VALUES('Tessa','Operations','B',86)")

# Insert Support Students
cursor.execute("INSERT INTO STUDENT VALUES('Ulysses','Support','C',59)")
cursor.execute("INSERT INTO STUDENT VALUES('Vera','Support','A',94)")
cursor.execute("INSERT INTO STUDENT VALUES('Walter','Support','B',68)")
cursor.execute("INSERT INTO STUDENT VALUES('Ximena','Support','A',97)")
cursor.execute("INSERT INTO STUDENT VALUES('Yuri','Support','C',63)")




##commit changes so they persist
connection.commit()     ##changes permanent ho gye

#(optional) print out inserted records to confirm
##it will display all records

print("Inserted Records:")
data = cursor.execute('''Select * from STUDENT''')

for row in data:
    print(row)

##commmited changes now closing the connection,
connection.close()