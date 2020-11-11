class info():
    def __init__(self):
        self.game = 1
        self.number = 'time'
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
        print(self.info.game)
        print(self.info.number)



t=MainFrame()