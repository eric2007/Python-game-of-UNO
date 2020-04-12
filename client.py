import socket
import json
import queue


class Client:
    sock = None
    runConnection = None
    # (IP,HOST)
    connectionAccept = False
    runFlag = True
    errorBuf = None
    table = 0
    recvBuf = queue.Queue(10)
    sendBuf =queue.Queue(10)
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.settimeout(1)
        self.main()

    def main(self):
        while self.runFlag:
            if not self.connectionAccept:
                if self.runConnection:
                    try:
                        self.sock.connect(self.runConnection)
                        self.sock.send(json.dumps({"cmd": "a", "table": self.table}).encode('utf-8'))
                    except Exception as ex:
                        self.errorBuf = ex
                continue

            data = self.sock.recv(1024).decode('utf-8')
            if data:
                self.recvBuf.put(data)