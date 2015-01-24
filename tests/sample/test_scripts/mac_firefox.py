import mechanize
import time

class Transaction(object):
    # def __init__(self):
        # do per-user user setup here
        # this gets called once on user creation
        # pass

    def run(self):
        # create a Browser instance
        br = mechanize.Browser()
        # don't bother with robots.txt
        br.set_handle_robots(False)
        # add a custom header so wikipedia allows our requests
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:35.0) Gecko/20100101 Firefox/35.0')]

        # start the timer
        start_timer = time.time()
        # submit the request
        resp = br.open('http://www.wikipedia.org/')
        resp.read()
        # stop the timer
        latency = time.time() - start_timer

        # store the custom timer
        self.custom_timers['Load_Front_Page'] = latency

        # verify responses are valid
        assert (resp.code == 200), 'Bad Response: HTTP %s' % resp.code