import sys, random, time
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
import card
colorList = ['b','g','r','y']
class Main(QMainWindow):
    cardLeft = list(range(1,109))
    myCard = []
    p1Card = []
    # p2Card = []
    done = False
    nowOut = []
    step = 0
    nowDir = False # 0:cw 1:ccw
    colorPad = []
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.resize(960,640)
        self.setWindowTitle('UNO Cards')
        cards = self.cardFun(7)
        for cardID, num in zip(self.cardFun(20), range(20)):
            self.myCard.append(card.Card(self, cardID, 150+25*num, 510, True))
        for cardID, num in zip(self.cardFun(20), range(20)):
            self.p1Card.append(card.Card(self, cardID, 30, 30+10*num))
        # for cardID, num in zip(self.cardFun(20), range(20)):
        #     self.p2Card.append(card.Card(self, cardID, 868, 30+10*num))

        # self.p1Left = QLabel('abc', self)
        self.playButton = QPushButton(self)
        self.playButton.pressed.connect(self.playMine)
        self.playButton.setStyleSheet("QPushButton{background-image: url(assets/play.png)} QPushButton{border: none}")
        self.playButton.setGeometry(355,470,70,22)
        self.noButton = QPushButton(self)
        self.noButton.pressed.connect(self.noMine)
        self.noButton.setStyleSheet("QPushButton{background-image: url(assets/no.png)} QPushButton{border: none}")
        self.noButton.setGeometry(475,470,70,22)
        tmp = QPushButton(self)
        tmp.setStyleSheet('QPushButton{background-image: url(empty.png)} QPushButton{border: none}')
        tmp.setGeometry(422, 116, 58, 52)
        tmp.setEnabled(False)
        self.colorPad.append(tmp)
        tmp = QPushButton(self)
        tmp.setStyleSheet('QPushButton{background-image: url(empty.png)} QPushButton{border: none}')
        tmp.setGeometry(480, 115, 58, 52)
        tmp.setEnabled(False)
        self.colorPad.append(tmp)
        tmp = QPushButton(self)
        tmp.setStyleSheet('QPushButton{background-image: url(empty.png)} QPushButton{border: none}')
        tmp.setGeometry(422, 170, 58, 52)
        tmp.setEnabled(False)
        self.colorPad.append(tmp)
        tmp = QPushButton(self)
        tmp.setStyleSheet('QPushButton{background-image: url(empty.png)} QPushButton{border: none}')
        tmp.setGeometry(479, 170, 58, 52)
        tmp.setEnabled(False)
        self.colorPad.append(tmp)
        self.timer1 = QBasicTimer()
        self.show()
    def noMine(self):
        self.timer1.start(15, self)
        self.myCard.append(card.Card(self, self.getRandomCard(), 150+25*len(self.myCard), 510, True))
        self.playButton.setDisabled(True)
        self.noButton.setDisabled(True)
        self.playButton.setStyleSheet("QPushButton{background-image: url(empty.png)} QPushButton{border: none}")
        self.noButton.setStyleSheet("QPushButton{background-image: url(empty.png)} QPushButton{border: none}")
        self.step = 0
    def bColorPadEvent(self):
        self.colorPadEvent('b')
    def gColorPadEvent(self):
        self.colorPadEvent('g')
    def rColorPadEvent(self):
        self.colorPadEvent('r')
    def yColorPadEvent(self):
        self.colorPadEvent('y')
    def colorPadEvent(self, color):
        self.colorPad[0].setStyleSheet('QPushButton{background-image: url(assets/rButton.png)} QPushButton{border: none}')
        self.colorPad[0].setEnabled(False)
        self.colorPad[1].setStyleSheet('QPushButton{background-image: url(assets/bButton.png)} QPushButton{border: none}')
        self.colorPad[1].setEnabled(False)
        self.colorPad[2].setStyleSheet('QPushButton{background-image: url(assets/yButton.png)} QPushButton{border: none}')
        self.colorPad[2].setEnabled(False)
        self.colorPad[3].setStyleSheet('QPushButton{background-image: url(assets/gButton.png)} QPushButton{border: none}')
        self.colorPad[3].setEnabled(False)
    def showColorPad(self):
        self.colorPad[0].setStyleSheet('QPushButton{background-image: url(assets/rButton.png)} QPushButton{border: none}')
        self.colorPad[0].setEnabled(True)
        self.colorPad[1].setStyleSheet('QPushButton{background-image: url(assets/bButton.png)} QPushButton{border: none}')
        self.colorPad[1].setEnabled(True)
        self.colorPad[2].setStyleSheet('QPushButton{background-image: url(assets/yButton.png)} QPushButton{border: none}')
        self.colorPad[2].setEnabled(True)
        self.colorPad[3].setStyleSheet('QPushButton{background-image: url(assets/gButton.png)} QPushButton{border: none}')
        self.colorPad[3].setEnabled(True)
    def playMine(self):
        self.done = 0
        for cardd in self.myCard:
            self.carddState = cardd.play(434, 400)
            if self.carddState != 0:
                self.myCard.remove(cardd)
                self.nowOut.append(cardd)
                self.done+=1
                if self.carddState == 2:
                    self.showColorPad()
        if self.done == 0:
            return
        self.timer1.start(15, self)
        for cardd, num in zip(self.myCard, range(len(self.myCard))):
            cardd.move(150+25*num, 510)
        self.noButton.setDisabled(True)
        self.playButton.setDisabled(True)
        self.playButton.setStyleSheet
        self.playButton.setStyleSheet("QPushButton{background-image: url(empty.png)} QPushButton{border: none}")
        self.noButton.setStyleSheet("QPushButton{background-image: url(empty.png)} QPushButton{border: none}")
        self.step = 0
        # self.nextPlayer(0)
    # def nextPlayer(self, lastPlayer): #0:me 1:p1 2:p2
    #     if nowDir:
            
            
    # def p1Turn(self):
    #     pass
    # def p2Turn(self):
    #     pass
    def timerEvent(self, e):
        # if e is self.timer1:
        if self.step >= 15:
            print(self.nowOut)
            self.timer1.stop()
            for i in self.nowOut:
                i.kill()
            self.nowOut.clear()
            self.playButton.setDisabled(False)
            self.noButton.setDisabled(False)
            self.playButton.setStyleSheet("QPushButton{background-image: url(assets/play.png)} QPushButton{border: none}")
            self.noButton.setStyleSheet("QPushButton{background-image: url(assets/no.png)} QPushButton{border: none}")
            return
        self.step += 1
    def getRandomCard(self):
        global colorList
        if len(self.cardLeft) == 0:
            raise SystemExit("Out of cards!")
        cardID = self.cardLeft.pop(random.randint(0,len(self.cardLeft)-1))
        if cardID>104: # 4
            return 'wild'
        elif cardID > 100:
            return 'wild4'
        # cardID 0-100
        cardColor = colorList[cardID % 4] # 0-3
        cardID = cardID%25 # 0-24
        if cardID == 0:
            return cardColor+'0'
        cardID = cardID%12
        if cardID == 9:
            return cardColor+'reverse'
        elif cardID == 10:
            return cardColor+'skip'
        elif cardID == 11:
            return cardColor+'draw2'
        else: # number
            return cardColor+str(cardID+1)
    def cardFun(self, num):
        tmp = []
        for _ in range(num):
            tmp.append(self.getRandomCard())
        return tmp
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())