# pip install mysql-connector-python
import mysql.connector
from datetime import datetime


# connect to mySQL
db = mysql.connector.connect(
        host="localhost",
        user="godda",
        passwd="brannagon",
        database="testdatabase")

mycursor = db.cursor(buffered=True)

# mycursor.execute("CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")

