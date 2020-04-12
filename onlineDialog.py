import sys, socket, json, threading
from PyQt5.QtWidgets import QDialog, QLabel, QApplication, QGridLayout, QLineEdit, QSpinBox, QPushButton, QHBoxLayout
from PyQt5.QtCore import QRect, QBasicTimer
from PyQt5.QtGui import QPainter, QColor


class OnlineDialog(QDialog):
    IP = ''
    host = 1024
    table = 1
    pid = None
    # receiverThread = None
    status = 0
    # 0:connecting 1:waiting 2:my turn

    def __init__(self, sock, connectEvent):
        self.connectEvent = connectEvent
        self.socket = sock
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Get online')
        self.resize(400, 300)   # set dialog size to 400*3Q00
        self.grid = QGridLayout(self)
        self.iplb = QLabel("IP:",self)        # add a label to this dialog
        self.grid.addWidget(self.iplb, 1, 1)

        self.ipEdit = QLineEdit(self)
        self.ipEdit.textChanged[str].connect(self.onChange1)
        self.grid.addWidget(self.ipEdit, 1, 2)

        self.hostlb = QLabel("Host:          ",self)        # add a label to this dialog
        self.grid.addWidget(self.hostlb, 2, 1)

        self.hostEdit = QSpinBox(self)
        self.hostEdit.valueChanged.connect(self.onChange2)
        self.hostEdit.setMinimum(1024)
        # self.hostEdit.setValue(8080)
        self.hostEdit.setMaximum(65535)
        self.grid.addWidget(self.hostEdit, 2, 2)

        # TODO connection password
        # self.pwdlb = QLabel("Password:     ",self)        # add a label to this dialog
        # self.grid.addWidget(self.pwdlb, 3, 1)   # set label position and size

        # self.pwdEdit = QLineEdit(self)
        # self.grid.addWidget(self.pwdEdit)
        
        self.tablelb = QLabel("Table:", self)
        self.grid.addWidget(self.tablelb, 4, 1)

        self.tableEdit = QSpinBox(self)
        self.tableEdit.valueChanged.connect(self.onChange3)
        self.tableEdit.setMinimum(1)
        self.tableEdit.setMaximum(5)
        self.grid.addWidget(self.tableEdit, 4, 2)

        self.hbox = QHBoxLayout()
        self.grid.addLayout(self.hbox, 5, 2)
        self.hbox.setContentsMargins(180, 0, 0, 0)

        self.cancelButton = QPushButton('Cancel', self)
        self.hbox.addWidget(self.cancelButton)
        self.cancelButton.pressed.connect(self.cancelButtonEvent)

        self.okButton = QPushButton('OK',self)
        self.hbox.addWidget(self.okButton)
        self.okButton.pressed.connect(self.OK)

        self.statusBar = QLabel(self)
        self.grid.addWidget(self.statusBar, 5, 1)

        self.setLayout(self.grid)
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.show()

    def cancelButtonEvent(self):
        if self.receiverThread and self.status == 1:
            self.receiverThread

    def onChange1(self, text):
        self.IP = text

    def onChange2(self, text):
        self.host = text

    def onChange3(self, text):
        self.table = text

    def OK(self):
        self.statusBar.setText('Connecting...')
        self.receiverThread = threading.Thread(target=self.receiverThreadFunction)
        self.receiverThread.start()

    def receiverThreadFunction(self):
        if self.pid == 0:
            while True:
                try:
                    self.socket.connect((self.IP, self.host))
                    print("debug#1")
                    # self.statusBar.setText('Your id:\n'+self.socket.recv(17).decode('utf-8'))
                    # self.pid = self.socket.recv(17).decode('utf-8')
                    self.socket.send(json.dumps({"cmd":"a", "table":self.table}).encode('utf-8'))
                    print("debug#2")
                    while True:
                        print("debug#3")
                        get = self.socket.recv(32).decode('utf-8')
                        try:
                            print('debug#4:', get)
                            recv = json.loads(get)
                        except json.decoder.JSONDecodeError:
                            print('debug#5:', get)
                            continue
                        if recv['cmd'] == 's':
                            print("done!")
                            self.accept()
                            self.connectEvent()
                            self.status = 1
                            # return
                        elif recv['cmd'] == 'f':
                            self.statusBar.setText(recv['reason'])
                            self.socket.close()
                            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            self.receiverThread = None
                            return
                        # break
                except ConnectionRefusedError:
                    self.statusBar.setText('Connection \nrefused!')
                    self.statusBar.setText(recv['reason'])
                    self.socket.close()
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.receiverThread = None
                    return
                except OSError as ex:
                    print(str(ex))
                    self.statusBar.setText("OS\nError!")
                    self.statusBar.setText(recv['reason'])
                    self.socket.close()
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.receiverThread = None
                    return
                if self.status != 0:
                    break
        if self.status == 1:
            while True:
                while True:
                    try:
                        self.socket.recv(8)
                        # TODO receive EOL
                    except BlockingIOError:
                        break
                # TODO return data


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OnlineDialog(socket.socket(), lambda: 0)
    sys.exit(app.exec_())
    threading.Thread()