# pi
# root or scbot
# t1ck2099

import pymysql.cursors

# Connect to the database

class SC_Mysql:
    def __init__(self):
        pass

    """ end of INIT """

    def __repr__(self):
        print("What am I")

    """ end of REPR """

    def connect_to_mysql(self):
        # Connect to the database
        connection = pymysql.connect(host='192.168.1.124',
                                          user='scbot',
                                          password='t1ck2099',
                                          db="scdb",
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
        return connection

    def create_new_record(self, gamename="something", table="sc_table"):
        connection = self.connect_to_mysql()
        try:
            with connection.cursor() as cursor:
                # variables
                gamename = "something"

                # Create a new record
                sql = "INSERT INTO `sc_table` (gamename) VALUES (%s)"
                values = (gamename)
                cursor.execute(sql, values)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            print(cursor.rowcount, "records inserted")
        finally:
            pass
            connection.close()


    def create_many_records(self, gamename="something", table="sc_table"):
        connection = self.connect_to_mysql()
        try:
            with connection.cursor() as cursor:
                # variables
                gamename = "something"

                # Create new records
                sql = "INSERT INTO `sc_table` (gamename) VALUES (%s)"
                values = (gamename,
                          "another",
                          "andanother",
                          "too many",
                          "some more")
                cursor.executemany(sql, values)     # MANY

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            print(cursor.rowcount, "records inserted")
        finally:
            connection.close()

    def read_single_record(self):
        connection = self.connect_to_mysql()
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `gameID`, `gamename` FROM `sc_table` WHERE `gameID`=%s"
                cursor.execute(sql, ('123',))
                result = cursor.fetchone()
                print(result)
            connection.commit()
        finally:
            connection.close()

    def record_exists(self, table, gameID):
        table = table
        gameID = gameID
        connection = self.connect_to_mysql()
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `gameID`, `gamename` FROM `sc_table` WHERE `gameID`=%s"
                cursor.execute(sql, ('123',))
                result = cursor.fetchone()
                print(result)
            connection.commit()
        finally:
            connection.close()


    def create_new_table(self, newtablename):
        connection = self.connect_to_mysql()

        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = f"CREATE TABLE {newtablename} (gameID int PRIMARY KEY AUTO_INCREMENT, gamename VARCHAR(50)"
                cursor.execute(sql)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        finally:
            connection.close()

    def table_exists(self, table="sc_table"):
        table = table   # table to searchf or
        connection = self.connect_to_mysql()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""SHOW TABLES""")
                results = cursor.fetchall()

            print('All existing tables:', results)  # Returned as a list of tuples
            results_list = []
            for d in results:                # list of dicts
                for key, value in d.items():         # dictionary
                    results_list.append(value)  # copy value
            print('All existing tables as list:', results_list)  # As a list

            if table in results_list:
                print(table, 'was found!')
                return True
            else:
                print(table, 'was NOT found!')
                return False
        finally:
            connection.close()

    def delete_table(self, table):
        pass

    def delete_record(self, table, gameID:
        pass


sc = SC_Mysql()
# sc.create_new_record()
# sc.create_many_records()
# sc.table_exists()
sc.read_single_record()
#sc.read_single_record()













    # def create_table(self, tablename, user):
    #     self.mycursor.execute("CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")
    #     self.mycursor.execute("CREATE TABLE sc_table (gameID int PRIMARY KEY AUTO_INCREMENT, gamename VARCHAR(50)")
    #
    # def describe_table(self):
    #     # to view all tables
    #     self.mycursor.execute("SHOW TABLES")
    #     # to view table differences
    #     #self.mycursor.execute("DESCRIBE sc_table")
    #
    #     tables = self.mycursor.fetchall()  # return data from last query
    #     print(tables)
    #     print(str(tables[0]))
    #
    #
    #     # for tablename in self.mycursor:
    #     #     print(tablename)
    #     #     #print(str(tablename) + "details: ")
    #     #     #self.mycursor.execute(f"DESCRIBE sc_table")
    #
    # def show_databases(self):
    #     self.mycursor.execute("SHOW DATABASES;")
    #
    # def use_db(self):
    #     self.mycursor.execute("USE 'scratchdb';")
    #
    # def stuff(self):
    #     pass



# from sc_mysql import SC_Mysql
