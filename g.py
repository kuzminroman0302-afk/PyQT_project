import sqlite3
import sys
import random
from PyQt6.QtMultimedia import QSoundEffect, QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt, QTimer, QUrl
import datetime as dt

class Horror(QWidget):
    def __init__(self, login):
        super().__init__()
        self.login = login

        self.initUI()

    def initUI(self):
        self.setWindowTitle("☠ ХОРРОР ☠")
        self.setFixedSize(1000, 900)
        a = dt.datetime.now()
        print(dt.datetime.strftime(a, "%Y-%m-%d %H:%M:%S"))


        self.time = QLabel(dt.datetime.strftime(a, "%Y-%m-%d %H:%M:%S"), self)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Horror("ads")
    game.show()
    sys.exit(app.exec())