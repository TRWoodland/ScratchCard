import matplotlib.ticker as mtick
import pymysql.cursors
from matplotlib import pyplot as plt
import logging
import tempfile
import os

class SC_Plot:
    def __init__(self, gamenumber):
        self.gamenumber = gamenumber
        self.x_dates = list()       # horizontal
        self.y_rt = list()          # vert
        self.per_day_list = list()  # vert2
        self.per_day_est = int()
        self.datestarted = None
        self.total_cards_at_launch = int()
        self.per_day_list = list()
        self.odds_of_win = int()
        self.gamename = str()

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
            self.log(self, str(self.gamenumber) + " Error connecting to MYSQL DB.")

    def disconnect(self):
        self.mycursor.close()
        self.connection.close()

    # def __repr__(self):
    #     print(str("Plot Class. Gamenumber: " +str(self.gamenumber)))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
    
    def get_data(self):
        # lastupdate & remainingtop, x_dates, y_rt
        self.mycursor.execute(f"SELECT remainingtop, lastupdate FROM `{self.gamenumber}` ORDER BY remainingtop DESC;")
        results = self.mycursor.fetchall()
        for result in results:
            self.x_dates.append(result['lastupdate'])
            self.y_rt.append(result['remainingtop'])

        # datestarted
        self.mycursor.execute(f"SELECT datestarted FROM `{self.gamenumber}` ORDER BY remainingtop ASC;")
        self.datestarted = self.mycursor.fetchone()
        self.datestarted = self.datestarted['datestarted']

        # total_cards_at_launch
        self.mycursor.execute(f"SELECT total_cards_at_launch FROM main WHERE gamenumber = {self.gamenumber};")
        self.total_cards_at_launch = self.mycursor.fetchone()
        self.total_cards_at_launch = self.total_cards_at_launch['total_cards_at_launch']

        # gamename
        self.mycursor.execute(f"SELECT gamename FROM main WHERE gamenumber = {self.gamenumber};")
        self.gamename = self.mycursor.fetchone()
        self.gamename = self.gamename['gamename']

        print("x_dates: " + str(self.x_dates) + "\ny_rt: " + str(self.y_rt) +
              "\ndatestarted: " + str(self.datestarted) + "\ntotal_cards_at_launch: " + str(self.total_cards_at_launch))


    def calc_odds(self):
        """ Projecting 75% of cards sold over 2 months """
        # cards sold per day
        per_day_est = int((self.total_cards_at_launch * .75) / 60)
        for index, value in enumerate(self.x_dates):                                    # for each item in x_dates
            self.per_day_list.append(int(self.total_cards_at_launch - (per_day_est * index)))

        """ Odds of Winning """
        self.odds_of_win = int(self.per_day_list[-1] / self.y_rt[-1])
        self.odds_of_win_str = f"Gamenumber: {self.gamenumber}\nEst Odds of Winning: 1 in " + str(self.odds_of_win)

        print("per_day_est: " + str(per_day_est) + "\nper_day_list: " + str(self.per_day_list) + str(self.odds_of_win_str))
        # return self.gamenumber, self.odds_of_win

    def odds(self):
        return self.odds_of_win

    def gnumber(self):
        return self.gamenumber

    def build_plot(self):
        plt.style.use('dark_background')
        fig = plt.figure()
        ax = fig.add_subplot(111)

        """ Primary X & Y, dates & remainingtop """
        ax.plot(self.x_dates, self.y_rt, color="#FF1690", marker="o", label=f"Remaining top prizes: {self.y_rt[-1]}")
        ax.set_xlabel(self.odds_of_win_str, fontsize=14)
        # ax.set_ylabel("remainingtop", color="#FF1690", fontsize=14)
        ax.tick_params(axis='y', colors='#FF1690')
        ax.tick_params(axis='x', colors='#36CDC4')

        """ Secondary X & Y, dates & % sold per day """
        ax2 = ax.twinx()
        ax2.plot(self.x_dates, self.per_day_list, "k--", color="#5C2686", marker="o",
                 label=f"Estimated cards left: {self.per_day_list[-1]}")
        # ax2.set_ylabel("Estimated Cards Sold", color="#5C2686", fontsize=14)
        ax2.tick_params(axis='y', colors='#5C2686')

        """ Percentage """
        yticks = mtick.PercentFormatter(xmax=self.total_cards_at_launch)
        ax2.yaxis.set_major_formatter(yticks)

        """ Legend & colour """
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc=0)

        ax2.spines['bottom'].set_color('#36CDC4')
        ax2.spines['top'].set_color('#36CDC4')
        ax2.spines['right'].set_color('#36CDC4')
        ax2.spines['left'].set_color('#36CDC4')

        plt.tight_layout()
        fig.autofmt_xdate()
        # plt.show()

        """ save plot """
        # save the plot as a file
        fn = os.path.join(tempfile.gettempdir(), str(self.gamenumber) + ".jpg")
        plt.savefig(fn, format='jpeg', dpi=100, bbox_inches='tight')
        print(fn)

    def process(self):
        self.connect()
        self.get_data()
        self.calc_odds()
        self.build_plot()
        self.disconnect()

# 1268
