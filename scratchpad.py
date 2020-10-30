string = r"""<a href="https://www.cdn-national-lottery.co.uk/c/i/page/scratchcards/popup/winterwonderlines-2020.jpg~999e" target="_blank" title="This image will open in a new window"><img alt="" src="https://www.cdn-national-lottery.co.uk/c/i/page/scratchcards/thumbnails/winterwonderlines-2020-thumbnail.jpg~453d"/></a>',<a href="/c/i/page/scratchcards/popup/100loaded_2020.jpg~8817" target="_blank" title="This image will open in a new window"><img alt="" src="/c/i/page/scratchcards/thumbnails/100loaded_2020-thumbnail.jpg~c9f5"/></a>
qwe[]"""
import logging

from Logger import SC_Logfile

l = SC_Logfile()

class Pet:
    def __init__(self, bob):
        self.bob=bob
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.FileHandler('test_log.log', mode='w'))

        if __name__ == '__main__':
            # call getLogger again with a name to tag subsequent log statements
            logger = logging.getLogger(__name__)
            logger.info('Importing class')
            t = TestClass()
            t.make_call()
            t.make_another_call()
            logger.info('End')
    def print(self):
        print("THING")
