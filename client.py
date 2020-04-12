import socket
class Client:
    sock = None
    runConnection = None
    # (IP,HOST)
    connectionAccept = False
    runFlag = True
    errorBuf
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.init
    def init(self):
        while self.runFlag:
            if not self.connectionAccept:
                if self.runConnection:
                    try:
                        self.sock.connect(self.)