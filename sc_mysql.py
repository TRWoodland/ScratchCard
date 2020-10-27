# pi
# root or scratchbot
# t1ck2099

import mysql.connector

# Connect to the database

class SC_Mysql:
    def __init__(self):
        self.db = mysql.connector.connect(host='192.168.1.124',
                                             user='scbot',
                                             password='t1ck2099',
                                             db='scdb'
                                             )
        self.mycursor = self.db.cursor()

        self.mycursor.execute("USE scdb;")

    """ end of INIT """

    def __repr__(self):
        print("What am I")

    """ end of REPR """

    def create_table(self, tablename, user):
        self.mycursor.execute("CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")
        self.mycursor.execute("CREATE TABLE sc_table (gameID int PRIMARY KEY AUTO_INCREMENT, gamename VARCHAR(50)")

    def describe_table(self):

        self.mycursor.execute("SHOW TABLES")

        tables = self.mycursor.fetchall()  # return data from last query
        for table in tables:
            print(str(table))  # to show table
        #
        # """ Another method"""
        # to view all tables
        self.mycursor.execute("SHOW TABLES")
        #
        for tablename in self.mycursor:
            print(str(tablename[0]) + " details: ")
            self.mycursor.execute(f"DESCRIBE {tablename[0]}")

    def show_databases(self):
        self.mycursor.execute("SHOW DATABASES;")

    def use_db(self):
        self.mycursor.execute("USE 'scratchdb';")

    def stuff(self):
        pass



# from sc_mysql import SC_Mysql
sc = SC_Mysql()
sc.describe_table()