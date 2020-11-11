class info():
    def __init__(self):
        self.info1 = 1
        self.info2 = 'time'
        print 'initialised'

class MainFrame():
    def __init__(self):
        a=info()
        print a.info1
        b=page1(a)
        c=page2(a)
        print a.info1

class page1():
    def __init__(self, information):
        self.info=information
        self.info.info1=3

class page2():
    def __init__(self, information):
        self.info=information
        print self.info.info1

t=MainFrame()