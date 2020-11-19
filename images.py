from matplotlib import pyplot as plt
from matplotlib import ticker
import matplotlib.ticker as mtick
import pymysql.cursors
from datetime import datetime
import logging

# use this version pip install numpy==1.19.3

# class Images:
#     def __init__(self, x_dates, y_rt):
#         self.x_dates = x_dates
#         self.y_rt = y_rt
#
#
#         if len(logging.getLogger().handlers) > 0:
#             # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
#             # `.basicConfig` does not execute. Thus we set the level directly.
#             logging.getLogger().setLevel(logging.INFO)
#         else:
#             logging.basicConfig(level=logging.INFO)
#
#     @staticmethod
#     def log(cls, string):
#         logging.error(string)
#         print(string)
#
#     def connect(self):
#         try:
#             REGION = 'eu-west-2a'
#             port = 3306
#             self.connection = pymysql.connect(r"""scdb.cviu5dc5mrn3.eu-west-2.rds.amazonaws.com""",
#                                               user="goddamuglybob",
#                                               passwd="t1ck2099",
#                                               db="scdb",
#                                               charset='utf8mb4',
#                                               cursorclass=pymysql.cursors.DictCursor,
#                                               connect_timeout=5)
#
#             # self.connection = pymysql.connect(host='192.168.1.124',
#             #                              user='scbot',
#             #                              password='t1ck2099',
#             #                              db='scdb',
#             #                              charset='utf8mb4',
#             #                              cursorclass=pymysql.cursors.DictCursor)
#             self.mycursor = self.connection.cursor()
#
#         except self.connection.Error as error:
#             print("Error connecting to MYSQL DB")
#             self.log(self, "Images Error connecting to MYSQL DB.")
#
#     def disconnect(self):
#         self.mycursor.close()
#         self.connection.close()
#
#     def __repr__(self):
#         print(str(self.connection.server_status()))
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.disconnect()
#
#     """END OF IMAGE"""


try:
    REGION = 'eu-west-2a'
    port = 3306
    connection = pymysql.connect(r"""scdb.cviu5dc5mrn3.eu-west-2.rds.amazonaws.com""",
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
    mycursor = connection.cursor()

except connection.Error as error:
    print("Error connecting to MYSQL DB")

gamenumber = 1268

x_dates = []  # horizontal
y_rt = []

mycursor.execute(f"SELECT remainingtop, lastupdate FROM `{gamenumber}` ORDER BY remainingtop DESC;")
results = mycursor.fetchall()
for result in results:
    x_dates.append(result['lastupdate'])
    y_rt.append(result['remainingtop'])
print(x_dates)    # datetime object
print(y_rt)

mycursor.execute(f"SELECT datestarted FROM `{gamenumber}` ORDER BY remainingtop ASC;")
datestarted = mycursor.fetchone()
datestarted = datestarted['datestarted']
print(datestarted)  # datetimeobject

mycursor.execute(f"SELECT total_cards_at_launch FROM main WHERE gamenumber = {gamenumber};")
total_cards_at_launch = mycursor.fetchone()
total_cards_at_launch = total_cards_at_launch['total_cards_at_launch']
print(total_cards_at_launch)

""" Projecting 75% of cards sold over 2 months """
# cards sold per day
per_day_est = int((total_cards_at_launch * .75) / 60)
per_day_list = []
for index, value in enumerate(x_dates):                                   # for each item in x_dates
    per_day_list.append(int(total_cards_at_launch - (per_day_est * index)))
print(per_day_est)
print(per_day_list)

""" Odds of Winning """
odds_of_win = "Estimated Odds of Winning: 1 in " + str(per_day_list[-1] / y_rt[-1])


plt.style.use('dark_background')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x_dates, y_rt, color="#FF1690", marker="o", label = f"Remaining top prizes: {y_rt[-1]}")
ax.set_xlabel(odds_of_win, fontsize=14)
#ax.set_ylabel("remainingtop", color="#FF1690", fontsize=14)
ax.tick_params(axis='y', colors='#FF1690')
ax.tick_params(axis='x', colors='#36CDC4')

ax2 = ax.twinx()
ax2.plot(x_dates, per_day_list, "k--", color="#5C2686", marker="o", label = f"Estimated cards left: {per_day_list[-1]}")
#ax2.set_ylabel("Estimated Cards Sold", color="#5C2686", fontsize=14)
ax2.tick_params(axis='y', colors='#5C2686')

yticks = mtick.PercentFormatter(xmax=total_cards_at_launch)
ax2.y_rt.set_major_formatter(yticks)

lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0)


ax2.spines['bottom'].set_color('#36CDC4')
ax2.spines['top'].set_color('#36CDC4')
ax2.spines['right'].set_color('#36CDC4')
ax2.spines['left'].set_color('#36CDC4')
plt.tight_layout()
plt.show()
# save the plot as a file
# fig.savefig('two_different_y_axis_for_single_python_plot_with_twinx.jpg',
#             format='jpeg',
#             dpi=100,
#             bbox_inches='tight')






# plt.title("Scratchcard Actual Odds")
#plt.show()







d1 = [32,41, 56,67,78,12,34,56,78,89]  # x
d2 = [10,20,30,40,50,60,70,80,90,99]



# import matplotlib.ticker as mtick
# from matplotlib.ticker import PercentFormatter
#
# # df = pd.DataFrame(np.random.randn(100, 5))
# # fig = plt.figure()
# # ax = fig.add_subplot(1, 1, 1)
# ax.plot(x_dates, y_rt)
# yticks = mtick.PercentFormatter(xmax=4712)
# ax.y_rt.set_major_formatter(yticks)
# # plt.show()



