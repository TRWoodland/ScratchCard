# pip install mysql-connector-python
import mysql.connector

# connect to mySQL
def sql_connection():
    db = mysql.connector.connect(
        host="localhost",
        user="godda",
        passwd="brannagon")
    return db

def sql_connection_database(selected_database):
    db = mysql.connector.connect(
        host="localhost",
        user="godda",
        passwd="brannagon",
        database=selected_database)
    return db

def create_database(db, database_name):
    mycursor = db.cursor()
    mycursor.execute("CREATE DATABASE " + database_name)
    return mycursor

# databases = testdatabase

db = sql_connection_database("testdatabase")
mycursor = db.cursor()

# VARCHAR(50)
# smallint # uses less memory
# UNSIGNED # always going to be a positive number (less memory)
# int PRIMARY KEY AUTO_INCREMENT
#def create_table(CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)

def describe_table(mycursor, table):
    mycursor.execute("DESCRIBE " + table)
    for x in mycursor:
        print(x)

# add to DB
mycursor.execute("INSERT INTO Person (name, age) VALUES (%s,%s)", "Bob", 99)
# commit to DB
db.commit()

# select everything from Person
mycursor.execute("SELECT * FROM Person")

