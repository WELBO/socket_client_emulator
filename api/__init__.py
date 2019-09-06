from .feathers import Feathers

class API:
    def __init__(self, deps, url, onAuthenticated, onAuthenticationFailed, onReAuthenticated):
        self.feathers = Feathers(deps, url, onAuthenticated, onAuthenticationFailed, onReAuthenticated)
        print "initialized feathers object in API"

    def onPosition(self, position):
        print "API position created"
        self.feathers.service('positions', 'create', position)
