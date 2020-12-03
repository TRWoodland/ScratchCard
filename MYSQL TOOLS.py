import pymysql.cursors
from datetime import datetime
import logging
from AwsStuff.sc_creds import AWS_MYSQL_ADD, AWS_MYSQL_USER, AWS_MYSQL_PW

class Mover:
    def __init__(self):

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
            # self.log(self, str(self.scratchcard.gamenumber) + " Error connecting to MYSQL DB.")

    def disconnect(self):
        self.mycursor.close()
        self.connection.close()

    def __repr__(self):
        print(str(self.connection.server_status()))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def main(self):
        self.list_of_logs = list()

        """ GET List of Tables"""
        self.mycursor.execute("SHOW TABLES")
        for x in self.mycursor:
            self.list_of_logs.append(x['Tables_in_scdb'])

        print(self.list_of_logs)
        self.newlist = list()
        for item in self.list_of_logs:
            try:
                self.newlist.append(int(item))
            except ValueError:
                print("nope" + str(item))
        print(self.newlist)


        """ INSERT INTO sc_log"""
        for game in self.newlist:
            print(game)
            self.mycursor.execute(f"INSERT INTO sc_log SELECT * FROM `{game}`;")
            self.connection.commit()

    def cleaner(self):
        self.mycursor.execute(f"SELECT gamenumber FROM main")
        x = self.mycursor.fetchall()
        self.list_games = list()
        for game in x:
            self.list_games.append(game['gamenumber'])

        rows_to_delete = list()
        for game in self.list_games:
            self.mycursor.execute(f"SELECT * FROM sc_log WHERE gnumber={game} ORDER BY remainingtop DESC")
            x = self.mycursor.fetchall()

            tempdates = []

            for rowdata in x:
                if rowdata['lastupdate'] not in tempdates:  # if its a new date
                    tempdates.append(rowdata['lastupdate']) # add to list
                else:
                    rows_to_delete.append(rowdata)          # not a new date
                    print("To delete: " + str(rowdata))

        for row in rows_to_delete:
            print("Deleting: " + str(row))
            # self.mycursor.execute("SHOW ENGINE INNODB STATUS")
            self.mycursor.execute(f"DELETE FROM sc_log WHERE gnumber='{row['gnumber']}' AND "
                                  f"remainingtop='{row['remainingtop']}' AND "
                                  f"lastupdate='{row['lastupdate']}' AND "
                                  f"datestarted='{row['datestarted']}';")
        self.connection.commit()

    def earliest(self):  # set all to earliest datestarted
        self.mycursor.execute(f"SELECT gamenumber FROM main")
        x = self.mycursor.fetchall()
        self.list_games = list()
        for game in x:
            self.list_games.append(game['gamenumber'])

        rows_to_delete = list()
        for game in self.list_games:
            self.mycursor.execute(f"SELECT * FROM sc_log WHERE gnumber={game} ORDER BY 'datestarted' DESC")
            gameset = self.mycursor.fetchall()

            """ Get earliest datestarted from game"""
            tempdate = datetime.now().date()
            for rowdata in gameset:
                if rowdata['datestarted'] < tempdate:
                    tempdate = rowdata['datestarted']

            """ update all gameset with oldest datestarted"""
            self.mycursor.execute(f"UPDATE sc_log SET datestarted='{tempdate}' WHERE gnumber={game};")
            self.connection.commit()

    def duplicate_rt(self):
        self.mycursor.execute(f"SELECT gamenumber FROM main")
        x = self.mycursor.fetchall()
        self.list_games = list()
        for game in x:
            self.list_games.append(game['gamenumber'])

        rows_to_delete = []

        for game in self.list_games:
            self.mycursor.execute(f"SELECT * FROM sc_log WHERE gnumber={game} ORDER BY 'remainingtop' DESC")
            gameset = self.mycursor.fetchall()

            rt = []
            for rowdata in gameset:
                if rowdata['remainingtop'] not in rt:
                    rt.append(rowdata['remainingtop'])
                else:
                    rows_to_delete.append(rowdata)

            for row in rows_to_delete:
                print("Deleting: " + str(row))
                # self.mycursor.execute("SHOW ENGINE INNODB STATUS")
                self.mycursor.execute(f"DELETE FROM sc_log WHERE gnumber='{row['gnumber']}' AND "
                                      f"remainingtop='{row['remainingtop']}' AND "
                                      f"lastupdate='{row['lastupdate']}' AND "
                                      f"datestarted='{row['datestarted']}';")
            self.connection.commit()

    def the_dead(self):
        """ MOVE INFO FROM MAIN AND LOGS"""
        """ TO RECORD HOW LONG CARDS SELL FOR"""
        pass

m = Mover()
m.connect()
# m.main()
# m.cleaner()
# m.earliest()
m.duplicate_rt()
m.disconnect()



