# pip install mysql-connector-python
# AWS mySQL admin sp00nfuture instance scratchcardDB port3306
import mysql.connector
# "database-1.cviu5dc5mrn3.eu-west-2.rds.amazonaws.com"

# def sql_connection():
#     db = sc_mysql.connector.connect(host="scratchcardDB.cviu5dc5mrn3.eu-west-2.rds.amazonaws.com", port=3306, user="admin", passwd="t1ck2099", database="scratchcardDB")
#     return db
# db = sql_connection()
# mycursor = db.cursor()
#

# connect to mySQL
def mysql():
    db = mysql.connector.connect(host='192.168.1.124',
                                      user='scbot',
                                      password='t1ck2099',
                                      db='scdb'
                                      )
    mycursor = db.cursor()
    mycursor.execute("USE scdb;")
    return mycursor
mycursor = mysql()

# Connect to Database
# def sql_connection_database(selected_database):
#     db = mysql.connector.connect(
#         host="localhost",
#         user="godda",
#         passwd="brannagon",
#         database=selected_database)
#     return db

#db = sql_connection_database("testdatabase")
#mycursor = db.cursor()

def create_database(cursor, database_name):
    cursor.execute("CREATE DATABASE " + database_name)


# databases = testdatabase



# Creating a table
# https://dev.mysql.com/doc/refman/8.0/en/data-types.html
# VARCHAR(50)
# smallint # uses less memory. 32767 max
# UNSIGNED # Will this field ever contain a negative value? If no, then you want an UNSIGNED data type.
# int PRIMARY KEY AUTO_INCREMENT
#mycursor.execute("CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")

def show_tables(cursor):
    cursor.execute("SHOW TABLES")
    for x in cursor:
        print(x)
show_tables(mycursor)

def describe_table(cursor, table):
    cursor.execute("DESCRIBE " + table)
    for x in cursor:
        print(x)
describe_table(mycursor, "person")

# to print all databases
def show_databases(cursor):
    cursor.execute("SHOW DATABASES")
    print(cursor.fetchall())
show_databases(mycursor)


def select_database(cursor, database):
    cursor.execute(f"USE {database}")
select_database(mycursor, "testdatabase")


# add to DB
mycursor.execute("INSERT INTO person (name, age) VALUES (%s,%s)",
                 ("Bob", 99))
# commit to DB
db.commit()

# select everything from person
# print everything from person
def select_all_print(cursor, table):
    cursor.execute("SELECT * FROM " + table)
    for x in cursor:
        print(x)
select_all_print(mycursor, "person")

# examples
# ENUM means select one.
# mycursor.execute("CREATE TABLE test (name VARCHAR(50) NOT NULL, created datetime NOT NULL, gender ENUM('M','F','O') NOT NULL , id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
# mycursor.execute("INSERT INTO test (name, created, gender) VALUES (%s,%s,%s)", ("TIM", datetime.now(), "M"))
# mycursor.execute("INSERT INTO test (name, created, gender) VALUES (%s,%s,%s)", ("TIM", datetime.now(), "M"))
# mycursor.execute("INSERT INTO test (name, created, gender) VALUES (%s,%s,%s)", ("John", datetime.now(), "F"))

# select all males
mycursor.execute("SELECT * FROM test WHERE gender = 'M'")
for x in mycursor:
    print(x)

# select all males
mycursor.execute("SELECT * FROM test WHERE gender = 'F' ORDER BY id DESC")
for x in mycursor:
    print(x)

# select specific fields
mycursor.execute("SELECT id, name FROM test")
for x in mycursor:
    print(x)

# alter
mycursor.execute("ALTER TABLE test ADD COLUMN food VARCHAR(50) NOT NULL")
# delete column
mycursor.execute("ALTER TABLE test DROP food")
# rename
mycursor.execute("ALTER TABLE test CHANGE name first_name VARCHAR(50) NOT NULL")

mycursor.execute("INSERT INTO main (name, age) VALUES (%s,%s)",
                 ("Bob", 99))


# Foreign key creation
Q1 = "CREATE TABLE Users (id int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), passwd VARCHAR(50))"
Q2 = "CREATE TABLE Scores (user_id int PRIMARY KEY, FOREIGN KEY(user_id) REFERENCES Users(id), game1 int DEFAULT 0, game2 int DEFAULT 0)"
mycursor.execute(Q1)
mycursor.execute(Q2)

mycursor.execute("SHOW TABLES")
for x in mycursor:
    print(x)


# adding many users at once
user_list = [("Picard", "bald"),
            ("Riker", "boobies"),
            ("Worf", "kaplah")]
score_list = [(23, 34),
            (45, 55),
            (66, 77)]
Q3 = "INSERT INTO users (name, passwd) VALUES (%s, %s)"
Q4 = "INSERT INTO scores (user_id, game1, game2) VALUES (%s, %s, %s)"

for x, user in enumerate(user_list):
    mycursor.execute(Q3, user)
    last_id = mycursor.lastrowid # the id of the last accessed
    mycursor.execute(Q4, (last_id,) + score_list[x])

mycursor.execute("SELECT * FROM scores")
for x in mycursor:
    print(x)