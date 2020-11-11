# pi
# root or scratchbot
# t1ck2099

import mysql.connector
from datetime import datetime
# Connect to the database
import logging

class SC_Mysql:
    def __init__(self, scratchcard):
        self.scratchcard = scratchcard

        self.module_logger = logging.getLogger('Scraper.SC_Mysql')
        self.module_logger.error("SOMETHING")

    """ CHILD TABLE HYPHEN `` """

    """ end of INIT """

    def connect(self):
        try:
            self.connection = mysql.connector.connect(host='192.168.1.124',
                                                      user='scbot',
                                                      password='t1ck2099',
                                                      db='scdb'
                                                      )
            self.mycursor = self.connection.cursor(dictionary=True, buffered=True)
            self.mycursor.execute("USE scdb;")

        except mysql.connector.Error as error:
            print("Error connecting to MYSQL DB")
            self.module_logger.error(str(self.scratchcard.gamenumber) + " Error connecting to MYSQL DB.")

    def disconnect(self):
        self.mycursor.close()
        self.connection.close()


    def __repr__(self):
        print("What am I")

    """ end of REPR """

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mycursor.close()
        self.connection.close()

    def create_main(self):
        self.mycursor.execute("CREATE TABLE main (gamenumber SMALLINT UNSIGNED NOT NULL, PRIMARY KEY (gamenumber),"
                              "gamename TINYTEXT NOT NULL,"
                              "odds_at_launch TINYTEXT NOT NULL,"
                              "total_cards_at_launch INT UNSIGNED NOT NULL,"
                              "cost SMALLINT UNSIGNED NOT NULL,"
                              "bigprize INT UNSIGNED NOT NULL,"
                              "image TINYTEXT NOT NULL,"
                              "pdf_url TINYTEXT NOT NULL,"
                              "pdf TINYTEXT NOT NULL)"
                              )
        self.connection.commit()

    def create_child(self):
        self.mycursor.execute(f"CREATE TABLE `{self.scratchcard.gamenumber}` (gnumber SMALLINT(5) UNSIGNED NOT NULL, FOREIGN KEY (gnumber) REFERENCES main(gamenumber),"
                              "remainingtop SMALLINT UNSIGNED NOT NULL,"
                              "lastupdate DATE,"
                              "datestarted DATE);")
        self.connection.commit()

    def list_of_tables(self):
        tables = []
        for table in [tables[0] for tables in self.mycursor.fetchall()]:
            # print(table)
            tables.append(table)
        return tables

    def table_exist(self, table):
        self.mycursor.execute("SHOW TABLES")
        for x in self.mycursor:
            if x['Tables_in_scdb'] == table:
                print("Table found in DB: " + table)
                return True
        print("Table not found in DB: " + table)
        return False

    def describe_table(self):
        self.mycursor.execute("SHOW TABLES")
        tables = self.mycursor.fetchall()  # return data from last query
        for table in tables:
            print(str(table))  # to show table
        """ Another method"""
        # to view all tables
        self.mycursor.execute("SHOW TABLES")
        for tablename in self.mycursor:
            print(str(tablename[0]) + " details: ")
            self.mycursor.execute(f"DESCRIBE {tablename[0]}")

    def no_of_rows(self, table):
        self.mycursor.execute(f"SELECT * FROM {table}")
        print("Total number of rows in Laptop is: ", self.mycursor.rowcount)

    def show_databases(self):
        self.mycursor.execute("SHOW DATABASES;")

    def use_db(self):
        self.mycursor.execute("USE 'scratchdb';")

    def exists_main(self):  # gets the number of rows affected by the command executed
        # self.mycursor.execute("SELECT EXISTS(SELECT * FROM main WHERE gamenumber=%s);")

        self.mycursor.execute(f"SELECT EXISTS(SELECT * FROM main WHERE gamenumber = {self.scratchcard.gamenumber});")

        row_count = self.mycursor.rowcount
        if row_count == 0:
            print(f"No rows found with: {self.scratchcard.gamenumber}")
            return False
        else:
            print(f"Number of Rows found with: {self.scratchcard.gamenumber} are {row_count}")
            return True

    def exists_child(self):  # gets the number of rows affected by the command executed
        self.mycursor.execute(f"SELECT EXISTS(SELECT * FROM `{self.scratchcard.gamenumber}` WHERE gnumber = {self.scratchcard.gamenumber});")
        row_count = self.mycursor.rowcount
        if row_count != 0:
            print(f"No rows found with: {self.scratchcard.gamenumber}")
            return False
        else:
            print(f"Number of Rows found with: {self.scratchcard.gamenumber} are {row_count}")
            return True

    def return_row(self, table="main"):
        self.mycursor.execute(f"(SELECT * FROM {table} WHERE gamenumber = {self.scratchcard.gamenumber});")
        return self.mycursor.fetchone()

    def update_row(self, table):    # NOT YET USED
        self.mycursor.execute(f"(UPDATE `{table}` SET remaingtop=`{self.scratchcard.remainingtop}` WHERE gamenumber = {self.scratchcard.gamenumber});")

    def insert_main(self):
        print(str(type(self.scratchcard.gamenumber)))
        print(str(type(self.scratchcard.gamename)))
        print(str(type(self.scratchcard.odds_at_launch)))
        print(str(type(self.scratchcard.total_cards_at_launch)))
        print(str(type(self.scratchcard.cost)))
        print(str(type(self.scratchcard.bigprize)))
        print(str(type(self.scratchcard.image)))
        print(str(type(self.scratchcard.pdf_url)))
        print(self.scratchcard.gamenumber, self.scratchcard.gamename, self.scratchcard.odds_at_launch,
               self.scratchcard.total_cards_at_launch, self.scratchcard.cost, self.scratchcard.bigprize,
               self.scratchcard.image, self.scratchcard.pdf_url, self.scratchcard.pdf)


        sql = "INSERT INTO main (gamenumber, gamename, odds_at_launch, total_cards_at_launch, cost, bigprize, image, " \
              "pdf_url, pdf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (self.scratchcard.gamenumber, self.scratchcard.gamename, self.scratchcard.odds_at_launch,
               self.scratchcard.total_cards_at_launch, self.scratchcard.cost, self.scratchcard.bigprize,
               self.scratchcard.image, self.scratchcard.pdf_url, self.scratchcard.pdf)
        self.mycursor.execute(sql, val)
        self.connection.commit()

    def insert_child(self):
        sql = f"INSERT INTO `{self.scratchcard.gamenumber}` (gnumber, remainingtop, lastupdate, datestarted) VALUES (%s, %s, %s, %s)"
        val = (self.scratchcard.gamenumber, self.scratchcard.remainingtop,
               self.scratchcard.lastupdate, self.scratchcard.datestarted)
        self.mycursor.execute(sql, val)

        self.connection.commit()

    def remaining_top(self):     # find rows that match remainingtop
        self.mycursor.execute(f"SELECT * FROM `{self.scratchcard.gamenumber}` ORDER BY remainingtop ASC LIMIT 1")
        rt_int = self.mycursor.fetchone()

        if rt_int != 0:
            print(f"{self.scratchcard.gamenumber} No Remainingtop found.")
            return False, rt_int
        else:
            print(f"{self.scratchcard.gamenumber} Remaingtop found")
            rt_int = rt_int['remainingtop']
            return True, rt_int

    def date_started(self):
        self.mycursor.execute(f"(SELECT * FROM `{self.scratchcard.gamenumber}` ORDER BY datestarted ASC LIMIT 1);")
        ds = self.mycursor.fetchone()
        if ds != 0:
            print(f"{self.scratchcard.gamenumber} Datestarted not found. creating new datestarted")
            ds = datetime.today().strftime("%Y-%m-%d")
            return ds
        else:
            print(f"{self.scratchcard.gamenumber} Datestarted found")
            ds = ds['datestarted']
            return ds

    def process(self):
        self.connect() # connect to db

        print(""" CREATE MAIN IF NOT EXIST""")
        if not self.table_exist("main"):
            self.create_main()

        print(""" IS GAMENUMBER IN MAIN""")
        if not self.exists_main():                          # if gamenumber not in main
            self.insert_main()
            # add to main

        print(""" IS THERE A GAMENUMBER SHEET """)
        if not self.table_exist(f"{self.scratchcard.gamenumber}"):    # if no child table
            self.create_child()
            # create child
        print( """ get earliest DATESTARTED FROM GAMENUMBER SHEET """)
        self.scratchcard.datestarted = self.date_started()

        print(""" LASTUPDATE """)
        self.scratchcard.lastupdate = datetime.today().strftime("%Y-%m-%d")

        print(""" IS REMAININGTOP THE SAME AS CURRENT NUMBER ON SHEET """)

        rt_status, rt_int = self.remaining_top()
        if not rt_status:    # if false nothing found, just insert into table
            print(self.scratchcard.gamenumber, self.scratchcard.remainingtop,
                  self.scratchcard.lastupdate, self.scratchcard.datestarted)
            self.insert_child()
        else:
            if self.scratchcard.remainingtop < rt_int:      # if new RT is less than what is currently on the table
                """ ADD NEW ENTRY TO TABLE """
                #self.scratchcard.remainingtop = rt_int
                print(self.scratchcard.gamenumber, self.scratchcard.remainingtop,
                      self.scratchcard.lastupdate, self.scratchcard.datestarted)
                self.insert_child()
    #self.process()


#

b = 1
if b == 2:
    import mysql.connector
    from datetime import datetime
    # Connect to the database
    import logging

    gamenumber = 1213
    gamename = "12 Months Richer"
    odds_at_launch = "1 in 3.35"
    total_cards_at_launch = 13564320
    cost = 5.0
    bigprize = 1200000.0
    image = r"""https: // www.cdn - national - lottery.co.uk / c / i / page / scratchcards / popup / 12
    monthsricher.jpg"""
    pdf_url = r"""https: // www.national - lottery.co.uk / c / files / scratchcards / 12
    monthsricher.pdf"""
    pdf = "monthsricher.pdf"
    remainingtop = 3
    lastupdate = datetime.today().strftime("%Y-%m-%d")
    datestarted = datetime.today().strftime("%Y-%m-%d")

    connection = mysql.connector.connect(host='192.168.1.124',
                                         user='scbot',
                                         password='t1ck2099',
                                         db='scdb'
                                         )
    mycursor = connection.cursor(dictionary=True, buffered=True)
    mycursor.execute("USE scdb;")


    def con(f):  # The first argument is the wrapper
        def wrapper():
            print("Connecting to DB")
            f()
            print("Disconnecting from DB")

    @con
    def something(bob):
        print(bob)
    something("qwerty")



# # from sc_mysql import SC_Mysql
# """ DUMMY DATA """
# gamenumber = 1234
# gamename = "test"
# odds_at_launch = "1 in 4321"
# total_cards_at_launch = 123456
# cost = 1.5
# bigprize = 500.5
# image = r"""https://www.cdn-national-lottery.co.uk/c/i/page/scratchcards/popup/12monthsricher.jpg~1c5c"""
# pdf_url = r"""https://www.cdn-national-lottery.co.uk/c/i/page/scratchcards/popup/12monthsricher.jpg~1c5c"""
# pdf = r"""https://www.cdn-national-lottery.co.uk/c/i/page/scratchcards/popup/12monthsricher.jpg~1c5c"""
# remainingtop = 321
# lastupdate = datetime.today().strftime("%Y-%m-%d")
# datestarted = datetime.today().strftime("%Y-%m-%d")
#
# sc = SC_Mysql(gamenumber, gamename, odds_at_launch, total_cards_at_launch, cost, bigprize, image,
#                  pdf_url, pdf, remainingtop, lastupdate, datestarted)
#
#
# if "main" not in sc.list_of_tables():
#     sc.create_main()
# if sc.gamenumber not in sc.list_of_tables():
#     sc.create_child()
#
# # check is on main. add to main
#
# if sc.remainingtop == 0:
#     pass
#     #updatemain
#     #updatesheet
#
#
# #sc.create_table()
# #sc.describe_table()
#
# tablelist = []
#
# for table in [tables[0] for tables in mycursor.fetchall()]:
#     tablelist.append(table)
#
#
#
#
# """ FUNCTIONS """
# # connect to mySQL
# def connect_mysql(database="scdb"):
#     db = mysql.connector.connect(host='192.168.1.124',
#                                       user='scbot',
#                                       password='t1ck2099',
#                                       db='scdb'
#                                       )
#     mycursor = db.cursor()
#     mycursor.execute("USE scdb;")
#     return db, mycursor
# db, mycursor = connect_mysql()
#
# # to print all databases
# def show_databases(c):
#     c.execute("SHOW DATABASES")
#     print(c.fetchall())
# #show_databases(mycursor)
#
# # select database
# def select_database(c, database="scdb"):
#     c.execute(f"USE {database}")
# #select_database(mycursor)
#
# # create_database
# def create_database(c, database_name):
#     c.execute("CREATE DATABASE " + database_name)
#
# def show_tables(c):
#     c.execute("SHOW TABLES")
#     for x in c:
#         print(x)
# #show_tables(mycursor)
#
# def describe_table(c, table="main"):
#     c.execute("DESCRIBE " + table)
#     for x in c:
#         print(x)
# #describe_table(mycursor)
#
#
#
#
#
# # add to DB
# #mycursor.execute("INSERT INTO person (name, age) VALUES (%s,%s)",
# #                 ("Bob", 99))
#
# # COMMIT
# db.commit()