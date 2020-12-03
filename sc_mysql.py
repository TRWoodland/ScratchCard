import pymysql.cursors
from datetime import datetime, timedelta
import logging
from AwsStuff.sc_creds import AWS_MYSQL_ADD, AWS_MYSQL_USER, AWS_MYSQL_PW
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
            self.connection = pymysql.connect(AWS_MYSQL_ADD,
                                              user=AWS_MYSQL_USER,
                                              passwd=AWS_MYSQL_PW,
                                              db="scdb",
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor,
                                              connect_timeout=5)
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
                              "pdf TINYTEXT NOT NULL,"
                              "status BOOLEAN)"
                              )

        self.connection.commit()

    def create_child(self):
        self.mycursor.execute(f"CREATE TABLE sc_log (gnumber SMALLINT(5) UNSIGNED NOT NULL, FOREIGN KEY (gnumber) REFERENCES main(gamenumber),"
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
        self.mycursor.execute(f"SELECT * FROM main WHERE gamenumber = {self.scratchcard.gamenumber}")
        x = self.mycursor.fetchall()
        if not x:  # if nothing found
            print(f"No rows found with: {self.scratchcard.gamenumber}")
            return False
        else:
            print(f"Row found with: {self.scratchcard.gamenumber}")
            return True

    def exists_child(self):  # gets the number of rows affected by the command executed
        self.mycursor.execute(f"SELECT EXISTS(SELECT * FROM `{self.scratchcard.gamenumber}` "
                              f"WHERE gnumber = {self.scratchcard.gamenumber});")
        row_count = self.mycursor.rowcount
        if row_count != 0:
            print(f"No rows found with: {self.scratchcard.gamenumber}")
            return False
        else:
            print(f"Number of Rows found with: {self.scratchcard.gamenumber} are {row_count}")
            return True

    def return_row(self, table="main"):
        self.mycursor.execute(f"(SELECT * FROM {table} "
                              f"WHERE gamenumber = {self.scratchcard.gamenumber});")
        return self.mycursor.fetchone()

    def update_row(self, table):    # NOT YET USED
        self.mycursor.execute(f"(UPDATE `{table}` SET remaingtop=`{self.scratchcard.remainingtop}` "
                              f"WHERE gamenumber = {self.scratchcard.gamenumber});")

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
        sql = f"INSERT INTO sc_log (gnumber, remainingtop, lastupdate, datestarted) VALUES (%s, %s, %s, %s)"
        val = (self.scratchcard.gamenumber, self.scratchcard.remainingtop,
               self.scratchcard.lastupdate, self.scratchcard.datestarted)
        self.mycursor.execute(sql, val)
        self.connection.commit()

    def remaining_top(self):     # find rows that match remainingtop
        self.mycursor.execute(f"SELECT * FROM sc_log  WHERE gnumber={self.scratchcard.gamenumber} ORDER BY remainingtop ASC LIMIT 1")
        rt_int = self.mycursor.fetchone()
        if rt_int:      # if rt_int is not None TODO: OR statement needed
            if 'remainingtop' in rt_int:
                rt_int = rt_int['remainingtop']
                print(f"{self.scratchcard.gamenumber} Remaingtop found")
                return True, rt_int
        else:
            print(f"{self.scratchcard.gamenumber} No Remainingtop found.")
            return False, rt_int

    def latest_date(self):
        self.mycursor.execute(f"SELECT lastupdate FROM sc_log WHERE gnumber = {self.scratchcard.gamenumber} ORDER BY lastupdate DESC LIMIT 1;")
        ld = self.mycursor.fetchone()
        ld = ld['lastupdate']
        return ld

    def update_child(self):
        self.mycursor.execute(f"UPDATE sc_log SET remainingtop = {self.scratchcard.remainingtop} WHERE gnumber = {self.scratchcard.gamenumber} AND lastupdate='{datetime.now().date()}';")
        self.connection.commit()

    def date_started(self):
        self.mycursor.execute(f"(SELECT * FROM sc_log WHERE gnumber={self.scratchcard.gamenumber} ORDER BY datestarted ASC LIMIT 1);")
        ds = self.mycursor.fetchone()
        if ds:      # if ds is not None
            if 'datestarted' in ds:                                 # if ds exists
                if ds['datestarted'] < datetime.now().date():       # and is less than todays date
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

        if not self.table_exist("sc_log"):    # if no child table
            self.create_child()

        """ get earliest DATESTARTED from GAME on sc_log SHEET """
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
                """ HAS THERE BEEN A LOGGING TODAY? """
                if self.latest_date() == datetime.now().date():
                    """UPDATE TODAYS LOG WITH NEW DATA """
                    self.update_child()
                else:
                    """ ADD NEW ENTRY TO TABLE """
                    self.insert_child()

        """ Alive or Dead """
        self.mycursor.execute(f"SELECT * FROM main WHERE status IS NULL OR status = 1")     # select all alive or null
        alive = self.mycursor.fetchall()

        for x in alive:                                                         # iterating through unknown status games
            self.mycursor.execute(f"SELECT * FROM sc_log WHERE gnumber = {x['gamenumber']} AND remainingtop = 0")  # remainingtop == 0
            if len(self.mycursor.fetchall()) > 1:  # if anything found
                print(f"Remainingtop 0, GN:{x['gamenumber']} setting main to dead")
                self.mycursor.execute(f"""UPDATE main SET status=0 WHERE gamenumber={x['gamenumber']}""")

            else:
                self.mycursor.execute(f"""UPDATE main SET status=1 WHERE gamenumber={x['gamenumber']}""")
            self.connection.commit()

        """ Move dead to Deadform """
    def create_dead(self):
        if not self.table_exist('dead'):        # if table doesn't exist
            self.mycursor.execute("CREATE TABLE dead (gamenumber SMALLINT UNSIGNED NOT NULL, PRIMARY KEY (gamenumber),"
                                  "odds_at_launch TINYTEXT,"
                                  "total_cards_at_launch INT UNSIGNED,"
                                  "top_prizes_at_launch INT UNSIGNED,"
                                  "datestarted DATE,"
                                  "finaldate DATE,"
                                  "daysran SMALLINT UNSIGNED);"
                                  )

            self.connection.commit()

    def move_dead(self):
        """ List of dead games"""
        self.mycursor.execute(f"SELECT gamenumber FROM dead;")
        results = self.mycursor.fetchall()
        deadgames = list()
        for game in results:
            deadgames.append(game['gamenumber'])

        """ list of newly dead games """
        self.mycursor.execute(f"SELECT gamenumber FROM main WHERE status = 0;")
        results = self.mycursor.fetchall()
        newdeadgames = list()
        for game in results:
            newdeadgames.append(game['gamenumber'])

        for game in newdeadgames:
            if game in deadgames:   # if game already in dead sheet
                print("if game already in dead sheet")
                self.mycursor.execute(f"UPDATE dead, main SET dead.odds_at_launch = main.odds_at_launch, "
                                      f"dead.total_cards_at_launch = main.total_cards_at_launch "
                                      f"WHERE main.gamenumber = {game};")
            else:                   # game not on dead sheet yet
                print("game not on dead sheet yet")
                self.mycursor.execute(f"INSERT INTO dead (gamenumber, odds_at_launch, total_cards_at_launch)"
                                      f"SELECT gamenumber, odds_at_Launch, total_cards_at_launch"
                                      f"FROM main WHERE status = 0;")

        self.connection.commit()

        """ GET LIST OF GAMES ON dead """
        deadgames = list(set(deadgames) | set(newdeadgames))    # merge lists
        """ GET LIST OF GAMES ON sc_log """
        self.mycursor.execute(f"SELECT gnumber FROM sc_log;")
        results = self.mycursor.fetchall()
        games_logging = list()
        for game in results:
            games_logging.append(game['gnumber'])

        for game in deadgames:
            if game in games_logging:
                print(f"processing {game}")
                self.mycursor.execute(f"SELECT datestarted FROM sc_log WHERE gnumber = {game} "
                                      f"ORDER BY 'datestarted' ASC LIMIT 1;")
                datestarted = self.mycursor.fetchone()
                datestarted = datestarted['datestarted']

                self.mycursor.execute(f"SELECT lastupdate FROM sc_log WHERE gnumber = {game} "
                                      f"ORDER BY 'lastupdate' DESC LIMIT 1;")
                finaldate = self.mycursor.fetchone()
                finaldate = finaldate['lastupdate']

                self.mycursor.execute(f"SELECT remainingtop FROM sc_log WHERE gnumber = {game} "
                                      f"ORDER BY 'remainingtop' DESC LIMIT 1;")
                top_prizes_at_launch = self.mycursor.fetchone()
                top_prizes_at_launch = top_prizes_at_launch['remainingtop']

                " TIME GAME RAN FOR"
                daysran = finaldate - datestarted
                daysran = daysran.days

                """ UPDATE dead """
                print(f"Updating dead with {game}, {top_prizes_at_launch}, {datestarted}, {finaldate}, {daysran}")
                self.mycursor.execute(f"UPDATE dead SET top_prizes_at_launch={top_prizes_at_launch}, "
                                      f"datestarted = {datestarted}, "
                                      f"finaldate = {finaldate}, "
                                      f"daysran = {daysran} "
                                      f"WHERE gamenumber = {game};")

                self.connection.commit()
                """ DELETE from sc_log """
                self.mycursor.execute(f"DELETE FROM sc_log WHERE gnumber = {game};")
                self.connection.commit()

                """ DELETE FROM MAIN """
                print("DELETE FROM main WHERE status = 0;")
                self.mycursor.execute(f"DELETE FROM main WHERE gamenumber = {game} AND status = 0;")
                self.connection.commit()

        self.disconnect()


