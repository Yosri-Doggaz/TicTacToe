import os
import sys
from functools import partial
from PyQt5 import QtWidgets, uic ,QtCore ,QtGui
from PyQt5.QtGui import QPixmap
import collections
import numpy as np


class Widget(QtWidgets.QMainWindow):
    def __init__(self):
        super(Widget, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(resource_path('tictac.ui'), self) # Load the .ui file
        self.cases = np.zeros((3,3),dtype=object)
        self.score = [0,0,0]
        self.userFirstPlay = []
        self.pcScore = self.findChild(QtWidgets.QLabel, 'pc')
        self.tieScore = self.findChild(QtWidgets.QLabel, 'tie')
        self.playerScore = self.findChild(QtWidgets.QLabel, 'player')
        self.restartImg = self.findChild(QtWidgets.QLabel, 'label')
        self.restartImg.mouseReleaseEvent = self.restart
        self.centerPlay= False
        self.mainWidget = self.findChild(QtWidgets.QWidget, 'mainView')
        self.set = {}
        self.moves = 9
        for i in range(3):
            for j in range(3):
                setattr(self,"label_{0}{1}".format(i,j),self.findChild(QtWidgets.QLabel, 'label_'+str(i)+str(j)))
                getattr(self,"label_{0}{1}".format(i,j)).mouseReleaseEvent = partial(self.userPlay,i,j)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.setFixedSize(752,621)
        self.show()

    def userPlay(self,l,c,QMouseEvent):
        self.userFirstPlay.append((l,c))
        self.ownMapPlace(l,c,1)
        if self.winnerCheck():
            self.setFinishScene("Player Win")
            self.score[0] += 1
            self.playerScore.setText(str(self.score[0]))
        elif self.moves != 0:
            self.pcPlay()
        if( not self.winnerCheck() and self.moves == 0):
            self.setFinishScene("Tie")
            self.score[1] += 1
            self.tieScore.setText(str(self.score[1]))


    def ownMapPlace(self,l,c,value):
        self.mainWidget.setEnabled(False)
        pixmap = QPixmap(resource_path("X.png") if value == 1 else resource_path("O.png"))
        pixmap = pixmap.scaled(125, 125)
        self.cases[l][c] = value
        getattr(self,"label_{0}{1}".format(l,c)).setPixmap(pixmap)
        getattr(self,"label_{0}{1}".format(l,c)).mouseReleaseEvent = None
        self.moves -= 1
        self.mainWidget.setEnabled(True)

    def diagonalMoveDetermer(self):
        sumUser = sumPc = last = 0
        for i in range(3) :
            if(self.cases[i][i]==1):
                sumUser+=1
            elif(self.cases[i][i]==0):
                last = (i,i)
            else:
                sumPc +=1
        if(sumUser == 2 and sumPc == 0):
            self.set[3] = last
        if(sumPc == 2 and sumUser == 0):
            self.set[4] = last
        if ( sumPc == 1 and sumUser ==0) or (sumPc == 0 and sumUser == 1):
            self.set[2] = last
        if ( sumPc == 1 and sumUser ==1) :
            self.set[1] = last
        
    def revDiagonalMoveDetermer(self):
        sumUser = sumPc = last = 0
        for i in range(3) :
            if(self.cases[i][2-i]==1):
                sumUser+=1
            elif(self.cases[i][2-i]==0):
                last = (i,2-i)
            else:
                sumPc +=1
        if(sumUser == 2 and sumPc == 0):
            self.set[3] = last
        if(sumPc == 2 and sumUser == 0):
            self.set[4] = last
        if ( sumPc == 1 and sumUser ==0) or (sumPc == 0 and sumUser == 1) :
            self.set[2] = last
        if ( sumPc == 1 and sumUser ==1) :
            self.set[1] = last

    def lineMoveDetermer(self):
        for i in range(3):
            sumUser = sumPc = last = 0
            for j in range(3):
                if(self.cases[i][j] == 1):
                    sumUser+=1
                elif(self.cases[i][j] == 0):
                    last = (i,j)
                else:
                    sumPc +=1
            if(sumUser == 2 and sumPc == 0):
                self.set[3] = last
            if(sumPc == 2 and sumUser == 0):
                self.set[4] = last
            if ( sumPc == 1 and sumUser ==0) or (sumPc == 0 and sumUser == 1):
                self.set[2] = last
            if ( sumPc == 1 and sumUser ==1) :
                self.set[1] = last

    def HorizontalMoveDetermer(self):
        for i in range(3):
            sumUser = sumPc = last = 0
            for j in range(3):
                if(self.cases[j][i]==1):
                    sumUser+=1
                elif(self.cases[j][i]==0):
                    last = (j,i)
                else:
                    sumPc +=1
            if(sumUser == 2 and sumPc == 0):
                self.set[3] = last
            if(sumPc == 2 and sumUser == 0):
                self.set[4] = last
            if ( sumPc == 1 and sumUser ==0) or (sumPc == 0 and sumUser == 1):
                self.set[2] = last
            if ( sumPc == 1 and sumUser ==1) :
                self.set[1] = last
 


    def pcPlay(self):
        self.set = {}
        self.determineNextMove()
        self.set = {k:v for k,v in self.set.items() if v != 0}
        l,c = self.set[next(iter(collections.OrderedDict(sorted(self.set.items(),reverse=True))))]
        self.ownMapPlace(l,c,2)
        if self.winnerCheck() :
            self.setFinishScene("PC Win")
            self.score[2] += 1
            self.pcScore.setText(str(self.score[2]))
    
    def firstMovePick(self):
        if(self.cases[1][1] == 1):
            self.set[2] = (0,0)
        elif(self.cases[0][0] == 1 or self.cases[0][2] == 1 or self.cases[2][0] == 1 or self.cases[2][2] == 1):
            self.set[2] = (1,1)
            self.centerPlay= True
        else:
            self.set[2] = (1,1)

    def secondMovePick(self):
        if( self.userFirstPlay[0][0] == 2 and self.userFirstPlay[0][1] == 2 ) or ( self.userFirstPlay[0][0] != 2 and self.userFirstPlay[0][1] == 2):
            self.set[2] = (self.userFirstPlay[0][0] , self.userFirstPlay[0][1] -1)
        elif( self.userFirstPlay[0][0] == 2 and self.userFirstPlay[0][1] != 2):
            self.set[2] = (self.userFirstPlay[0][0]-1 , self.userFirstPlay[0][1] )
        elif( self.userFirstPlay[0][0] == 0 and self.userFirstPlay[0][1] == 0):
            self.set[2] = (self.userFirstPlay[0][0] , self.userFirstPlay[0][1] + 1 )



    def determineNextMove(self):
        if( self.moves == 8 ):
            self.firstMovePick()
        elif( self.moves == 6 and self.centerPlay ):
            self.secondMovePick()
        else:
            self.lineMoveDetermer()
            self.revDiagonalMoveDetermer()
            self.HorizontalMoveDetermer()
            self.diagonalMoveDetermer()



    def setFinishScene(self,gameStatus):
        self.mainWidget.setEnabled(False)
        self.win_lbl = QtWidgets.QLabel(gameStatus, self)
        self.btn_Restart = QtWidgets.QPushButton("Restart", self)
        self.btn_Restart.clicked.connect(self.restart)
        self.win_lbl.setFont(QtGui.QFont('Segoe UI', 14))
        self.win_lbl.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.win_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.layout().addChildWidget(self.win_lbl)
        self.btn_Restart.setGeometry(200, 150, 100, 40)
        self.layout().addChildWidget(self.btn_Restart)
        self.win_lbl.move(int(( self.width() - self.win_lbl.width()-40 ) / 2), int(( self.height() - self.win_lbl.height() - self.btn_Restart.height()-70) / 2))
        self.btn_Restart.move(int(( self.width() - self.win_lbl.width()-40 ) / 2), int(( self.height()-70 ) / 2))

    def lineWinCheck(self):
        for i in range(3):
            sumUser = sumPc = 0
            for j in range(3):
                if(self.cases[i][j] == 1):
                    sumUser+=1
                elif(self.cases[i][j] == 2):
                    sumPc +=1
            if(sumPc > 2 or sumUser > 2):
                return True
        return False
                
    def HorizontalWinCheck(self):
        for i in range(3):
            sumUser = sumPc = 0
            for j in range(3):
                if(self.cases[j][i] == 1):
                    sumUser+=1
                elif(self.cases[j][i] == 2):
                    sumPc +=1
            if(sumPc > 2 or sumUser > 2):
                return True
        return False

    def revDiagonalWinCheck(self):
        sumUser = sumPc = 0
        for i in range(3) :
            if(self.cases[i][2-i] == 1):
                sumUser+=1
            elif(self.cases[i][2-i] == 2):
                sumPc +=1
        if(sumPc > 2 or sumUser > 2):
            return True
        return False

    def diagonalWinCheck(self):
        sumUser = sumPc = 0
        for i in range(3) :
            if(self.cases[i][i] == 1):
                sumUser+=1
            elif(self.cases[i][i] == 2):
                sumPc +=1
        if(sumPc > 2 or sumUser > 2):
            return True
        return False

    def winnerCheck(self):
        result = self.lineWinCheck()
        result = result or self.HorizontalWinCheck()
        result = result or self.revDiagonalWinCheck()
        result = result or self.diagonalWinCheck()
        return result


    def restart(self,QMouseEvent=""):
        self.cases = np.zeros((3,3))
        self.set = {}
        self.userFirstPlay = []
        self.centerPlay = False
        self.moves = 9
        for i in range(3):
            for j in range(3):
                getattr(self,"label_{0}{1}".format(i,j)).clear()
                getattr(self,"label_{0}{1}".format(i,j)).mouseReleaseEvent = partial(self.userPlay,i,j)
        try:
            self.win_lbl.deleteLater()
            self.btn_Restart.deleteLater()
        except :
            print("")
        self.mainWidget.setEnabled(True)






def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Widget()
    sys.exit(app.exec())
