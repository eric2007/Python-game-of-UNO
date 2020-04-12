from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
class Card(QPushButton):
    cardState = 0 # 0 default 1 out 2 played

    def __init__(self, parentWindow, cardID, x, y, mine = False):
        super().__init__(parentWindow)
        self.x = x
        self.y = y
        self.cardID = cardID
        self.mine = mine
        if mine:
            self.setStyleSheet("QPushButton{{background-image: url(cards/{}.jpg)}}".format(cardID) + "QPushButton{border: none}")
        else:
            self.setStyleSheet("QPushButton{background-image: url(cards/back.jpg)} QPushButton{border: none}")
        self.setGeometry(x,y,62,97)
        self.setFlat(True)
        self.pressed.connect(self.cardClicked)
        self.show()
    def cardClicked(self):
        if not self.mine or self.cardState == 2:
            return
        self.cardState = 1-self.cardState
        self.y -= self.cardState*30-15
        self.setGeometry(self.x,self.y,62,97)
        # print(self.cardState, self.cardState*15)
    def move(self, x, y):
        super().move(x, y)
        self.x = x
        self.y = y
    def pas(self):
        pass
    def play(self, x, y):
        if self.cardState == 1:
            self.cardState = 2
            self.setGeometry(x,y,62,97)
            self.pressed.connect(self.pas)
            self.cardState = 2
            # print(self.cardID)
            if self.cardID == 'wild':
                return 2
                # print('wild')
            return 1
        return 0
    def kill(self):
        if self.cardState != 2:
            return
        self.setStyleSheet("QPushButton{background-image: url(empty.png)} QPushButton{border: none}")
