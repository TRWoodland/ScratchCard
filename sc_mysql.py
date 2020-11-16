import pymysql.cursors
from datetime import datetime
import logging

class SC_Mysql:
    def __init__(self, scratchcard):
        self.scratchcard = scratchcard

        if len(logging.getLogger().handlers) > 0:
            # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
            # `.basicConfig` does not execute. Thus we set the level directly.
            logging.getLogger().setLevel(logging.INFO)
        else:
            logging.basicConfig(level=logging.INFO)

    """ CHILD TABLE HYPHEN ` REQUIRED ONLY WHEN REFERRING TO GAMENUMBER TABLES"""

    """ end of INIT """

    @staticmethod
    def log(cls, string):
        logging.error(string)
        print(string)

    def connect(self):
        try:
            REGION = 'eu-west-2a'
            port = 3306
            self.connection = pymysql.connect(r"""scdb.cviu5dc5mrn3.eu-west-2.rds.amazonaws.com""",
                                              user="goddamuglybob",
                                              passwd="t1ck2099",
                                              db="scdb",
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor,
                                              connect_timeout=5)

            # self.connection = pymysql.connect(host='192.168.1.124',
            #                              user='scbot',
            #                              password='t1ck2099',
            #                              db='scdb',
            #                              charset='utf8mb4',
            #                              cursorclass=pymysql.cursors.DictCursor)
            self.mycursor = self.connection.cursor()

        except self.connection.Error as error:
            print("Error connecting to MYSQL DB")
            self.log(self, str(self.scratchcard.gamenumber) + " Error connecting to MYSQL DB.")

    def disconnect(self):
        self.mycursor.close()
        self.connection.close()

    def __repr__(self):
        print(str(self.connection.server_status()))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

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
            if x['Tables_in_scdb'] == str(table):
                print("Table found in DB: " + str(table))
                return True
        print("Table not found in DB: " + str(table))
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

        self.mycursor.execute(f"SELECT * FROM main WHERE gamenumber = {self.scratchcard.gamenumber}")
        x = self.mycursor.fetchall()
        if not x:  # if nothing found
            print(f"No rows found with: {self.scratchcard.gamenumber}")
            return False
        else:
            print(f"Row found with: {self.scratchcard.gamenumber}")
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

        if 'remainingtop' in rt_int:
            rt_int = rt_int['remainingtop']
            print(f"{self.scratchcard.gamenumber} Remaingtop found")
            return True, rt_int
        else:
            print(f"{self.scratchcard.gamenumber} No Remainingtop found.")
            return False, rt_int


    def date_started(self):
        self.mycursor.execute(f"(SELECT * FROM `{self.scratchcard.gamenumber}` ORDER BY datestarted ASC LIMIT 1);")
        ds = self.mycursor.fetchone()

        if 'datestarted' in ds:                                 # if ds exists
            if ds['datestarted'] < datetime.now().date():  # and is less than todays date
                ds = ds['datestarted']                          # get datestarted
                print(f"{self.scratchcard.gamenumber} Datestarted found")
                return ds
        else:
            ds = datetime.now().date()                          # new datestarted
            print(f"{self.scratchcard.gamenumber} Datestarted not found. creating new datestarted")
            return ds

    def process(self):
        self.connect()  # connect to db

        """ CREATE MAIN IF NOT EXIST"""
        if not self.table_exist("main"):
            self.create_main()

        """ IS GAMENUMBER IN MAIN"""
        if not self.exists_main():                          # if gamenumber not in main
            self.insert_main()
            # add to main

        """ IS THERE A GAMENUMBER SHEET """
        if not self.table_exist(self.scratchcard.gamenumber):    # if no child table
            self.create_child()
            # create child
        """ get earliest DATESTARTED FROM GAMENUMBER SHEET """
        self.scratchcard.datestarted = self.date_started()

        """ LASTUPDATE """
        self.scratchcard.lastupdate = datetime.today().strftime("%Y-%m-%d")

        """ IS REMAININGTOP THE SAME AS CURRENT NUMBER ON SHEET """
        rt_status, rt_int = self.remaining_top()
        if not rt_status:    # if false nothing found, just insert into table
            print(self.scratchcard.gamenumber, self.scratchcard.remainingtop,
                  self.scratchcard.lastupdate, self.scratchcard.datestarted)
            self.insert_child()
        else:
            if self.scratchcard.remainingtop < rt_int:      # if new RT is less than what is currently on the table
                """ ADD NEW ENTRY TO TABLE """
                self.insert_child()
        self.disconnect()


