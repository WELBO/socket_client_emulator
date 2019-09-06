from api import API
import time, threading

url = "https://sky.welbo.eu"
class APP:
    
    def onAuthenticated(self):
        print "AUTHENTICATION SUCCESS"
        self.api.onPosition({"coords": {
            "x": 1,
            "y": 2
        }})
        # print(time.ctime())
        threading.Timer(3, self.onAuthenticated).start()

    def onAuthenticationFailed(self):
        print "FAILED TO AUTHENTICATE"

    def onReAuthenticated(self):
        print "REAUTHENTICATED"

    def start(self):
        self.api = API({} , url, self.onAuthenticated, self.onAuthenticationFailed, self.onReAuthenticated)