from threading import Thread
import time 

class SocketThread(Thread):
    def __init__(self, socket):
        Thread.__init__(self)
        self.socket = socket
        self.shouldRun = True

    def run(self):
        while self.shouldRun:
            try:
                self.socket.sleep(1)
            except Exception as e:
                print "Socket not connected..." + str(e)

    def stop(self):
        self.shouldRun = False
class FeathersObj(object):
    def __init__(self, deps, url, onAuthenticated, onAuthenticationFailed, onReAuthenticated):
        self.sio = deps['socketio'].Client(reconnection=True, reconnection_delay=300, reconnection_delay_max=0.3, engineio_logger=True)
        #self.app.listen(5000)
        self.url = url
        self.sio.connect(url)
        self.onAuthenticatedCb = onAuthenticated
        self.onAuthenticationFailedCb = onAuthenticationFailed
        self.onReAuthenticatedCb =  onReAuthenticated
        self.initialAuthentication = False
        self.authenticated = False
        self.connected = False
        self.socket = SocketThread( self.sio )
        self.socket.start()
        
        @self.sio.event
        def connect():
            print 'connected to feathers  server!'
            self.connected = True
            self.authenticate()
            

        @self.sio.event
        def disconnect():
            print("I'm disconnected!")
            self.connected = False
            self.authenticated = False

    def authenticate(self):
        def onAuthenticated(msg, res):
            print(res)
            print "authenticated to feathers!"
            self.authenticated = True
            if not self.initialAuthentication:
                self.onAuthenticatedCb()
                self.initialAuthentication = True
                
            else:
                print "============== reconnection successful =============="
                self.onReAuthenticatedCb()    

        print "authenticating to feathers.."
        accessToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6ImFjY2VzcyJ9.eyJ1c2VySWQiOiI1ZDZjZDk3ZmRkMDUwNjNjYTAzMWNiYTMiLCJpYXQiOjE1Njc2MDIxMjUsImV4cCI6MTU2NzY4ODUyNSwiYXVkIjoiaHR0cHM6Ly95b3VyZG9tYWluLmNvbSIsImlzcyI6ImZlYXRoZXJzIiwic3ViIjoiYW5vbnltb3VzIiwianRpIjoiMThlMjVlYTMtNzAxMS00OWFjLWEwMGYtYzg1YTM4NzRhY2NiIn0.kSiQ1nXg3sTJkQQaxdzv3q3U62iNEuDC8fFgTHhfUVA"
        connectionObject = { 'strategy':'jwt', 'accessToken': accessToken }
        self.sio.emit('authenticate', connectionObject, callback=onAuthenticated)

    
    def service(self, serviceName, method, data):

        def onAck(msg, response=None):
            print(response)
            if(response):
                print "Acknowledgement was successful for " + str(serviceName)
            else:
                print "Acknowledgement was unsuccessful for " + str(serviceName)
                self.sio.emit(serviceName+'::'+method, data, callback=onAck)
                print "============== re-emiting " + serviceName + " =============="
        #return message

        print "============== before emit of " + serviceName + " =============="  
        print str(self.connected) + " " + str(self.authenticated)
        while not (self.connected and self.authenticated):
            print "not connected...not sending event"
            time.sleep(0.3)

        self.sio.emit(serviceName+'::'+method, data, callback=onAck)
        print "============== emiting " + serviceName + " =============="