import matplotlib.ticker as mtick
import pymysql.cursors
from matplotlib import pyplot as plt
import logging
import tempfile
import os
import matplotlib.transforms as mtrans

class SC_Megaplot:
    def __init__(self, list_of_sc):
        self.list_of_sc = list_of_sc

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

    def build_plot(self):
        colours = ["#FF6C11", "#FF3864", "#2DE2E6", "#FF0000", "#023788",
                   "#650D89", "#F9C80E", "#00ff00", "#afeeee", "#FD6A02"]
        markers = [".", ",", "o", "1", "2", "3", "4", "P", "*", "+"]
        lines = ["solid", "dashed", "dashdot", "dotted", "solid", "dashed", "dashdot", "dotted", "solid", "dashed"]
        legend_list = list()

        plt.style.use('dark_background')
        fig = plt.figure(figsize=(8.0, 5.0))
        ax = fig.add_subplot(111)

        for index, game in enumerate(self.list_of_sc):
            ax.plot(game.x_dates, game.y_rt, linestyle=lines[index], color=colours[index], marker=markers[index])
            legend_list.append(f"GN: {game.gamenumber}. 1 in {game.odds_of_win} chance.")
            print(game.odds_of_win)

        ax.tick_params(axis='y', colors='#FF1690')
        ax.tick_params(axis='x', colors='#36CDC4')

        ax.spines['bottom'].set_color('#36CDC4')
        ax.spines['top'].set_color('#36CDC4')
        ax.spines['right'].set_color('#36CDC4')
        ax.spines['left'].set_color('#36CDC4')
        ax.yaxis.label.set_color('#36CDC4')

        plt.legend(legend_list, fontsize="x-small")

        plt.ylabel("Remaining Winning Top Cards")
        plt.title(f"Best Odds: GN{self.list_of_sc[0].gamenumber}: "
                  f"{self.list_of_sc[0].gamename}, 1 in {self.list_of_sc[0].odds_of_win}")
        plt.tight_layout()
        fig.autofmt_xdate()

        fn = os.path.join(tempfile.gettempdir(), "megaplot.jpg")
        plt.savefig(fn, format='jpeg', dpi=100, bbox_inches='tight')
