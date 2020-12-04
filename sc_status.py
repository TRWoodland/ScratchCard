import pymysql.cursors
import logging
from AwsStuff.sc_creds import AWS_MYSQL_ADD, AWS_MYSQL_USER, AWS_MYSQL_PW

class SC_Status:
    def __init__(self):

        if len(logging.getLogger().handlers) > 0:
            # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
            # `.basicConfig` does not execute. Thus we set the level directly.
            logging.getLogger().setLevel(logging.INFO)
        else:
            logging.basicConfig(level=logging.INFO)

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
            self.log(self, "Error connecting to MYSQL DB trying to get list of dead games.")

    def disconnect(self):
        self.mycursor.close()
        self.connection.close()

    """ GET LIST OF DEAD GAMES """
    def bring_out_the_dead(self):       # monty python joke

        self.mycursor.execute(f"SELECT gamenumber FROM dead")
        dead = self.mycursor.fetchall()
        list_of_dead = list()
        for game in dead:
            list_of_dead.append(game['gamenumber'])

        return list_of_dead

    def bring_out_the_living(self):

        self.mycursor.execute(f"SELECT gamenumber FROM main")
        alive = self.mycursor.fetchall()
        alive_list = list()

        for game in alive:
            alive_list.append(game['gamenumber'])

        return alive_list
    
    def get_remainingtops(self):
        alive_list = self.bring_out_the_living()
        dead_list = self.bring_out_the_dead()

        """ Remove dead from alive """
        for game in alive_list:
            if game in dead_list:
                print(f"GN {game} needs to be removed from main as its dead")
                alive_list.remove(game)

        dict_of_alive_rt = dict()
        for game in alive_list:
            self.mycursor.execute(f"SELECT remainingtop FROM sc_log "
                                  f"WHERE gnumber = {game} "
                                  f"ORDER BY remainingtop "
                                  f"LIMIT 1;")
            rt = self.mycursor.fetchone()
            if not rt:          # if nothing found
                print(f"GN {game} missing RT from sc_log")
            else:
                rt = rt['remainingtop']
                dict_of_alive_rt[game] = rt
        return dict_of_alive_rt, dead_list

# s = SC_Status()
# s.connect()
# s.get_remainingtops()
# s.disconnect()