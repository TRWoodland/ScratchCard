

def con(f):    # The first argument is the wrapper
    def wrapper(*args, **kwargs):
        print("Connecting to DB")

        f(*args, **kwargs)
        print("Disconnecting from DB")

    """ this would call the wrapper """
    # return wrapper()
    """ this just returns the object """
    return wrapper

@con
def something(x):

    print("Submitted: " + str(x))

@con
def func3():
    print("I am func3")

def connect(self):
    try:
        self.connection = mysql.connector.connect(host='192.168.1.124',
                                                  user='scbot',
                                                  password='t1ck2099',
                                                  db='scdb'
                                                  )
        self.mycursor = self.connection.cursor(dictionary=True)
        self.mycursor.execute("USE scdb;")

    except mysql.connector.Error as error:
        print("Error connecting to MYSQL DB")
        self.module_logger.error(str(self.scratchcard.gamenumber) + " Error connecting to MYSQL DB.")
def disconnect(self):
    self.mycursor.close()
    self.connection.close()

something("qwer")
