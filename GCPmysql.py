# pi
# root or scratchbot
# t1ck2099
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='192.168.1.124',
                             user='scratchbot',
                             password='t1ck2099',
                             db='scratchdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor
                             )  # errors to catch: pymysql.err.OperationalError:
