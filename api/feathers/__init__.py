from .feathers import FeathersObj
import os

class Feathers(FeathersObj):
    def __init__(self, *args):
        try:
            import socketio
            import websocket
            print( "succesfully importet socketio library")
        except:
            print( "Installing socketio")
            if not os.path.exists(os.getenv("HOME")+"/get-pip.py"): #check if pip is already installed
                os.system("cd ~ && wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py --user")
            os.system("cd ~/.local/bin && ./pip install python-socketio --user && ./pip install --upgrade python-socketio --user")
            os.system("cd ~/.local/bin && ./pip install websocket_client --user && ./pip install --upgrade websocket_client --user")

        import socketio
        args[0]['socketio'] = socketio

        super(Feathers, self).__init__( *args )
