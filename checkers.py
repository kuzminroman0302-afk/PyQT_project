import sqlite3
import sys
import random

from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer, QSoundEffect
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QColor


class checkers(QWidget):
    def __init__(self, login):
        super().__init__()
        self.login = login

        self.board_lst = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Шашки")
        self.setGeometry(300, 30, 800, 800)
        self.setFixedSize(800, 800)

        self.board = []
        self.chek = []
        count = -1
        y = 0
        for i in range(8):
            x = 0
            n = []
            for j in range(8):
                self.btn = QPushButton(self)
                self.btn.move(x, y)
                self.btn.resize(100, 100)
                if count % 2 == 0:
                    self.btn.setStyleSheet("background-color: black;")
                    if count <= 24:
                        self.btn_black = QPushButton(self)
                        self.btn_black.move(x + 25, y + 25)
                        self.btn_black.resize(50, 50)
                        self.btn_black.setStyleSheet("background-color: red;")
                        self.btn_black.clicked.connect(lambda chek=True, x=i, y=j, color="red": self.clic(x, y, color))

                    elif count >= 43:
                        self.btn_white = QPushButton(self)
                        self.btn_white.move(x + 25, y + 25)
                        self.btn_white.resize(50, 50)
                        self.btn_white.setStyleSheet("background-color: white;")
                        self.btn_white.clicked.connect(lambda chek=True, x=i, y=j, color="white": self.clic(x, y, color))

                    n.append((1, self.btn))
                else:
                    self.btn.setStyleSheet("background-color: white;")
                    n.append((0, self.btn))
                x += 100
                count += 1
            self.board_lst.append(n)
            count += 1
            y += 100

    def clic(self, x, y, color):
        count = -1
        for i in self.board_lst:
            for j in i:
                if count % 2 == 0:
                    j[1].setStyleSheet("background-color: black;")
                else:
                    j[1].setStyleSheet("background-color: white;")
                count += 1
            count += 1

        x1 = None
        y1 = None
        x2 = None
        y2 = None
        if color == "red":
            if self.board_lst[y + 1][x + 1][0] == 1:
                x2 = x + 1
                y2 = y + 1
            if self.board_lst[y + 1][x - 1][0] == 1:
                x1 = x - 1
                y1 = y + 1
        elif color == "white":
            if self.board_lst[y - 1][x - 1][0] == 1:
                x2 = x - 1
                y2 = y - 1
            if self.board_lst[y - 1][x + 1][0] == 1:
                x1 = x + 1
                y1 = y - 1

        for i, y in enumerate(self.board_lst):
            for j, x in enumerate(self.board_lst[i]):
                if (i, j) == (x1, y1) or (i, j) == (x2, y2):
                    print(i, j, x1, y1, x2, y2)
                    self.board_lst[i][j][1].setStyleSheet("background-color: green;")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = checkers("ads")
    game.show()
    sys.exit(app.exec())