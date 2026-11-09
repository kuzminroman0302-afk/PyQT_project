import sqlite3
import sys
import random
from PyQt6.QtMultimedia import QSoundEffect, QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt, QTimer, QUrl


class Horror(QWidget):
    def __init__(self, login):
        super().__init__()
        self.login = login

        self.imgs = [
            "one_close_door.jpg", "two_close_door.jpg", "three_close_door.jpg",
            "four_close_door.jpg", "five_close_door.jpg", "six_close_door.jpg",
            "seven_close_door.jpg", "eight_close_door.jpg", "nine_close_door.jpg",
            "ten_close_door.jpg", "eleven_close_door.jpg"
        ]

        self.count1 = 0
        self.count2 = 0
        self.count3 = 0

        self.door_open = QSoundEffect()
        self.door_open.setSource(QUrl.fromLocalFile("door.wav"))
        self.door_open.setVolume(0.5)

        self.scrim = QSoundEffect()
        self.scrim.setSource(QUrl.fromLocalFile("scrim.wav"))
        self.scrim.setVolume(0.5)

        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile("dead.mp3"))
        self.player.setLoops(QMediaPlayer.Loops.Infinite)
        self.audio_output.setVolume(0.3)

        self.r = QAudioOutput()
        self.heartbeat = QMediaPlayer()
        self.heartbeat.setAudioOutput(self.r)
        self.heartbeat.setSource(QUrl.fromLocalFile("heartbeat.mp3"))
        self.heartbeat.setLoops(QMediaPlayer.Loops.Infinite)
        self.r.setVolume(1)

        self.level = 0

        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.next_frame1)

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.next_frame2)

        self.timer3 = QTimer(self)
        self.timer3.timeout.connect(self.next_frame3)

        self.initUI()

    def initUI(self):
        self.player.play()
        self.setWindowTitle("☠ ХОРРОР ☠")
        self.setFixedSize(1000, 900)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #000000, stop:0.7 #1a0000, stop:1 #3a0000);
                font-family: 'Georgia', serif;
                color: #8b0000;
            }
        """)

        self.title_label = QLabel("ВЫБЕРИ ДВЕРЬ", self)
        self.title_label.setGeometry(0, 20, 1000, 100)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            color: #8b0000;
            font-family: 'Georgia', serif;
            font-size: 64px;
            font-weight: bold;
            letter-spacing: 8px;
            background: transparent;
        """)
        title_shadow = QGraphicsDropShadowEffect()
        title_shadow.setBlurRadius(40)
        title_shadow.setColor(QColor(255, 0, 0, 200))
        title_shadow.setOffset(0, 0)
        self.title_label.setGraphicsEffect(title_shadow)

        self.lbl1 = QLabel(self)
        self.lbl1.move(50, 140)
        self.lbl1.resize(300, 450)
        self.lbl1.setStyleSheet("""
            border: 5px solid #4a0000;
            border-radius: 5px;
            background-color: #0a0000;
            padding: 4px;
        """)
        shadow1 = QGraphicsDropShadowEffect()
        shadow1.setBlurRadius(50)
        shadow1.setColor(QColor(255, 0, 0, 150))
        shadow1.setOffset(0, 0)
        self.lbl1.setGraphicsEffect(shadow1)
        self.lbl1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_door_image(self.lbl1, "zero_close_door.jpg")

        self.btn_open_one = QPushButton("ОТКРЫТЬ", self)
        self.btn_open_one.resize(200, 100)
        self.btn_open_one.move(100, 620)
        self.btn_open_one.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_open_one.setStyleSheet("""
            QPushButton {
                background-color: #3a0000;
                color: #ff3333;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Arial Black', sans-serif;
                border: 3px solid #8b0000;
                border-radius: 10px;
                letter-spacing: 2px;
            }
            QPushButton:hover {
                background-color: #8b0000;
                color: white;
                border: 3px solid #ff0000;
            }
            QPushButton:pressed {
                background-color: #ff0000;
            }
            QPushButton:disabled {
                background-color: #1a0000;
                color: #4a0000;
                border: 3px solid #2a0000;
            }
        """)
        self.btn_open_one.clicked.connect(self.open_one)

        self.lbl2 = QLabel(self)
        self.lbl2.move(350, 140)
        self.lbl2.resize(300, 450)
        self.lbl2.setStyleSheet("""
            border: 5px solid #4a0000;
            border-radius: 5px;
            background-color: #0a0000;
            padding: 4px;
        """)
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(50)
        shadow2.setColor(QColor(255, 0, 0, 150))
        shadow2.setOffset(0, 0)
        self.lbl2.setGraphicsEffect(shadow2)
        self.lbl2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_door_image(self.lbl2, "zero_close_door.jpg")

        self.btn_open_two = QPushButton("ОТКРЫТЬ", self)
        self.btn_open_two.resize(200, 100)
        self.btn_open_two.move(400, 620)
        self.btn_open_two.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_open_two.setStyleSheet(self.btn_open_one.styleSheet())
        self.btn_open_two.clicked.connect(self.open_two)

        self.lbl3 = QLabel(self)
        self.lbl3.move(650, 140)
        self.lbl3.resize(300, 450)
        self.lbl3.setStyleSheet("""
            border: 5px solid #4a0000;
            border-radius: 5px;
            background-color: #0a0000;
            padding: 4px;
        """)
        shadow3 = QGraphicsDropShadowEffect()
        shadow3.setBlurRadius(50)
        shadow3.setColor(QColor(255, 0, 0, 150))
        shadow3.setOffset(0, 0)
        self.lbl3.setGraphicsEffect(shadow3)
        self.lbl3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_door_image(self.lbl3, "zero_close_door.jpg")

        self.btn_open_three = QPushButton("ОТКРЫТЬ", self)
        self.btn_open_three.resize(200, 100)
        self.btn_open_three.move(700, 620)
        self.btn_open_three.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_open_three.setStyleSheet(self.btn_open_one.styleSheet())
        self.btn_open_three.clicked.connect(self.open_three)

    def set_door_image(self, label, image_path):
        pix = QPixmap(image_path)
        scaled = pix.scaled(
            300, 450,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        label.setPixmap(scaled)

    def block(self):
        if self.timer1.isActive() or self.timer2.isActive() or self.timer3.isActive():
            self.btn_open_one.setEnabled(False)
            self.btn_open_two.setEnabled(False)
            self.btn_open_three.setEnabled(False)
        else:
            self.btn_open_one.setEnabled(True)
            self.btn_open_two.setEnabled(True)
            self.btn_open_three.setEnabled(True)

    def win(self):
        self.title_label.hide()
        self.btn_open_three.hide()
        self.btn_open_one.hide()
        self.btn_open_two.hide()
        self.lbl1.hide()
        self.lbl2.hide()
        self.lbl3.hide()

        self.heartbeat.play()
        self.player.stop()

        self.win_bg = QLabel(self)
        self.win_bg.setGeometry(0, 0, 1000, 900)
        self.win_bg.setStyleSheet("background-color: rgba(0, 0, 0, 220);")
        self.win_bg.show()

        self.win_frame = QLabel(self)
        self.win_frame.setGeometry(150, 250, 700, 400)
        self.win_frame.setStyleSheet("""
               QLabel {
                   background-color: #1a0000;
                   border: 4px solid #ff0000;
                   border-radius: 20px;
                   color: #ffcccc;
                   font-family: 'Georgia', serif;
                   font-size: 32px;
                   font-weight: bold;
                   padding: 30px;
               }
           """)
        self.win_frame.setText(
            "☠ ВЫ ВЫБРАЛИСЬ ☠\n\n"
            "Вы прошли все 5 испытаний\n"
            "и смогли покинуть этот\n"
            "проклятый дом.\n\n"
            "Но помните...\n"
            "Он всегда будет ждать вас."
        )
        self.win_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.win_frame.setWordWrap(True)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(60)
        shadow.setColor(QColor(255, 0, 0, 200))
        shadow.setOffset(0, 0)
        self.win_frame.setGraphicsEffect(shadow)

        self.win_frame.show()

        self.exit = QPushButton("Exit", self)
        self.exit.resize(300, 80)
        self.exit.move(350, 680)
        self.exit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.exit.setStyleSheet("""
               QPushButton {
                   background-color: #3a0000;
                   color: #ff3333;
                   font-size: 22px;
                   font-weight: bold;
                   font-family: 'Arial Black', sans-serif;
                   border: 3px solid #8b0000;
                   border-radius: 15px;
                   letter-spacing: 2px;
               }
               QPushButton:hover {
                   background-color: #8b0000;
                   color: white;
                   border: 3px solid #ff0000;
               }
               QPushButton:pressed {
                   background-color: #ff0000;
               }
           """)
        self.exit.clicked.connect(self.close_game)
        self.exit.show()

    def close_game(self):
        self.heartbeat.stop()
        self.close()
        if self.level >= 5:
            con = sqlite3.connect("proect.db")
            cur = con.cursor()
            money = cur.execute("SELECT money FROM profile WHERE login = ?", (self.login,)).fetchone()
            cur.execute("UPDATE profile SET money=? WHERE login=?", (money[0] + 30, self.login))
            con.commit()
            con.close()
        from proect import Lobby
        self.lobby = Lobby(None, self.login)
        self.lobby.show()

    def open_one(self):
        self.count1 = 0
        self.timer1.start(220)
        self.block()
        self.door_open.play()
        self.level += 1

    def next_frame1(self):
        if self.count1 >= len(self.imgs):
            self.timer1.stop()
            self.block()
            if self.level != 4:
                self.scare_by("scare_one.jpg")
            else:
                self.set_door_image(self.lbl1, "zero_close_door.jpg")
                if self.level == 5:
                    self.win()
            return
        self.set_door_image(self.lbl1, self.imgs[self.count1])
        self.count1 += 1

    def open_two(self):
        self.count2 = 0
        self.block()
        self.door_open.play()
        self.level += 1
        self.timer2.start(220)

    def next_frame2(self):
        if self.count2 >= len(self.imgs):
            self.timer2.stop()
            self.block()
            if self.level != 2 and self.level != 3:
                self.scare_by("scare_two.jpg")
            else:
                self.set_door_image(self.lbl2, "zero_close_door.jpg")
                if self.level == 5:
                    self.win()
            return
        self.set_door_image(self.lbl2, self.imgs[self.count2])
        self.count2 += 1

    def open_three(self):
        self.count3 = 0
        self.block()
        self.door_open.play()
        self.level += 1
        self.timer3.start(220)

    def scare_by(self, path):
        self.player.stop()
        self.heartbeat.play()
        self.scrim.play()
        self.image8 = QPixmap(path)
        self.lbl8 = QLabel(self)
        self.lbl8.move(0, 0)
        self.lbl8.resize(1000, 900)
        scaled = self.image8.scaled(
            1000, 900,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.lbl8.setPixmap(scaled)
        self.lbl8.setStyleSheet("background-color: black;")
        self.lbl8.show()
        self.lbl8.raise_()

        self.exit = QPushButton("Exit", self)
        self.exit.resize(300, 80)
        self.exit.move(0, 820)
        self.exit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.exit.setStyleSheet("""
                       QPushButton {
                           background-color: #3a0000;
                           color: #ff3333;
                           font-size: 22px;
                           font-weight: bold;
                           font-family: 'Arial Black', sans-serif;
                           border: 3px solid #8b0000;
                           border-radius: 15px;
                           letter-spacing: 2px;
                       }
                       QPushButton:hover {
                           background-color: #8b0000;
                           color: white;
                           border: 3px solid #ff0000;
                       }
                       QPushButton:pressed {
                           background-color: #ff0000;
                       }
                   """)
        self.exit.clicked.connect(self.close_game)
        self.exit.show()

    def next_frame3(self):
        if self.count3 >= len(self.imgs):
            self.timer3.stop()
            self.block()
            if self.level != 1 and self.level != 5:
                self.scare_by("scare_three.jpg")
            else:
                self.set_door_image(self.lbl3, "zero_close_door.jpg")
                if self.level == 5:
                    self.win()
            return
        self.set_door_image(self.lbl3, self.imgs[self.count3])
        self.count3 += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Horror("ads")
    game.show()
    sys.exit(app.exec())