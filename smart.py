import random
import sqlite3
import sys
import traceback

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QColor
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer, QSoundEffect
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QLabel
)


class Game(QWidget):
    def __init__(self, login):
        super().__init__()
        self.login = login

        self.con = sqlite3.connect("proect.db")
        self.cur = self.con.cursor()

        self.money, self.ex, self.level, self.record, self.music = self.cur.execute(
            "SELECT money, ex, level, record_memory, music FROM profile WHERE login=?", (self.login,)).fetchone()

        self.score = 0
        self.high_score = self.record

        self.buttons = []
        self.count_time = 0
        self.count_time_limit = 0

        self.count_player = 0
        self.next = False
        self.lst_bot = []

        self.is_bot = False
        self.game_over = False
        self.flag = False

        self.audio_output = QAudioOutput()
        self.player2 = QMediaPlayer()
        self.player2.setAudioOutput(self.audio_output)
        self.player2.setSource(QUrl.fromLocalFile("memory.wav"))
        self.player2.setLoops(QMediaPlayer.Loops.Infinite)
        self.audio_output.setVolume(0.05)

        self.buy_click = QSoundEffect()
        self.buy_click.setSource(QUrl.fromLocalFile("buy.wav"))
        self.buy_click.setVolume(0.05)

        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(500)

        self.prom_time = QTimer(self)
        self.prom_time.timeout.connect(self.player)

    def initUI(self):
        if self.music == 1:
            self.player2.play()
        self.setWindowTitle("MEMORY")
        self.setGeometry(100, 50, 1540, 900)
        self.setFixedSize(1540, 900)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setStyleSheet("background-color: #0d0d1a;")

        btn_size = 140
        gap = 20
        start_x = 380
        start_y = 80

        y = start_y
        for i in range(5):
            x = start_x
            prom = []
            for j in range(5):
                self.btn = QPushButton(self)
                self.btn.move(x, y)
                self.btn.resize(btn_size, btn_size)
                self.btn.clicked.connect(lambda checked=False, y=i, x=j: self.click(x, y))
                self.set_btn_style(self.btn, "rgb(20, 20, 40)", "rgb(50, 50, 80)")
                prom.append(self.btn)
                x += btn_size + gap
            y += btn_size + gap
            self.buttons.append(prom)

        self.lbl_score_title = QLabel("СЧЕТ", self)
        self.lbl_score_title.setStyleSheet(
            "font-size: 30px; color: #00ffcc; font-weight: bold; background: transparent;")
        self.lbl_score_title.setGeometry(100, 250, 200, 50)
        self.lbl_score_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_score_val = QLabel("0", self)
        self.lbl_score_val.setStyleSheet("""
            font-size: 80px; 
            color: #00ffcc; 
            font-weight: bold;
            background-color: #1a1a33;
            border: 3px solid #00ffcc;
            border-radius: 20px;
            padding: 10px;
        """)
        self.lbl_score_val.setGeometry(50, 300, 300, 150)
        self.lbl_score_val.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_record_title = QLabel("РЕКОРД", self)
        self.lbl_record_title.setStyleSheet(
            "font-size: 30px; color: #ff00ff; font-weight: bold; background: transparent;")
        self.lbl_record_title.setGeometry(1190, 250, 200, 50)
        self.lbl_record_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_record_val = QLabel(str(self.high_score), self)
        self.lbl_record_val.setStyleSheet("""
            font-size: 80px; 
            color: #ff00ff; 
            font-weight: bold;
            background-color: #1a1a33;
            border: 3px solid #ff00ff;
            border-radius: 20px;
            padding: 10px;
        """)
        self.lbl_record_val.setGeometry(1190, 300, 300, 150)
        self.lbl_record_val.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_over = QLabel("GAME OVER", self)
        self.lbl_over.setStyleSheet("""
            font-size: 70px; 
            color: #ff0055; 
            font-weight: bold;
            background-color: rgba(0, 0, 0, 200);
            padding: 20px;
            border-radius: 20px;
            border: 3px solid #ff0055;
        """)
        self.lbl_over.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_over.setGeometry(470, 380, 600, 160)
        self.lbl_over.hide()

        self.btn_restart = QPushButton("RESTART", self)
        self.btn_restart.resize(250, 70)
        self.btn_restart.move(100, 800)
        self.btn_restart.setStyleSheet("""
            QPushButton {
                font-size: 24px; 
                color: #00ffcc; 
                font-weight: bold;
                background-color: #1a1a33;
                border: 2px solid #00ffcc;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #00ffcc;
                color: #000000;
            }
        """)
        self.btn_restart.clicked.connect(self.restart)

        self.btn_exit = QPushButton("EXIT", self)
        self.btn_exit.resize(250, 70)
        self.btn_exit.move(1190, 800)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                font-size: 24px; 
                color: #ff00ff; 
                font-weight: bold;
                background-color: #1a1a33;
                border: 2px solid #ff00ff;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #ff00ff;
                color: #000000;
            }
        """)
        self.btn_exit.clicked.connect(self.lobby)

    def set_btn_style(self, btn, bg_color, border_color):
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                border: 3px solid {border_color};
                border-radius: 25px;
            }}
        """)

    def update_score(self):
        self.lbl_score_val.setText(str(self.score))
        if self.score == 10:
            if self.level == 10:
                self.level += 1
            self.next = True
            self.cur.execute("UPDATE profile SET money=?, ex=?, level=? WHERE login=?",
                             (self.money + 30, self.ex + 20, self.level, self.login))
            self.con.commit()
        if self.score > self.high_score:
            self.high_score = self.score
            self.lbl_record_val.setText(str(self.high_score))
            self.save_record()

    def save_record(self):
        self.cur.execute("UPDATE profile SET record_memory=? WHERE login=?", (self.high_score, self.login))
        self.con.commit()

    def lobby(self):
        self.con.close()
        if self.music == 1:
            if self.next:
                self.buy_click.play()
        self.player2.stop()
        from proect import Lobby
        self.lobby = Lobby(None, self.login)
        self.lobby.show()
        self.close()

    def restart(self):
        self.lbl_over.hide()
        self.game_over = False
        self.next = False

        self.score = 0
        self.lbl_score_val.setText("0")

        for i in self.buttons:
            for j in i:
                j.setEnabled(True)
                self.set_btn_style(j, "rgb(20, 20, 40)", "rgb(50, 50, 80)")

        self.count_time = 0
        self.count_time_limit = 0
        self.count_player = 0
        self.lst_bot = []
        self.is_bot = True

        self.prom_time.stop()
        self.timer.start(500)

    def bot(self):
        if self.lst_bot:
            if self.count_time != 0:
                n = self.count_time - 1
            else:
                n = 0
            i = self.lst_bot[n]
            self.set_btn_style(self.buttons[i[1]][i[0]], i[-1], "#ffffff")

    def tick(self):
        self.is_bot = True

        if self.count_time <= self.count_time_limit:
            self.bot()
            self.count_time += 1
        else:
            hue = random.randint(0, 360)
            color = QColor.fromHsl(hue, 255, 150)
            color_str = f"rgb({color.red()}, {color.green()}, {color.blue()})"

            x, y = random.randint(0, 4), random.randint(0, 4)

            self.set_btn_style(self.buttons[y][x], color_str, "#ffffff")
            self.lst_bot.append((x, y, color_str))

            self.timer.stop()
            self.prom_time.start(1000)

    def player(self):
        for row in self.buttons:
            for btn in row:
                self.set_btn_style(btn, "rgb(20, 20, 40)", "rgb(50, 50, 80)")

        self.prom_time.stop()
        self.is_bot = False

    def click(self, x, y):
        if self.is_bot or self.game_over:
            return

        if (x, y) == (self.lst_bot[self.count_player][0], self.lst_bot[self.count_player][1]):
            self.set_btn_style(self.buttons[y][x], self.lst_bot[self.count_player][-1], "#ffffff")
            self.count_player += 1

            if self.count_player > self.count_time_limit:
                self.is_bot = True
                QTimer.singleShot(500, self.next_level)
        else:
            self.lbl_over.show()
            self.dead()

    def next_level(self):
        for row in self.buttons:
            for btn in row:
                self.set_btn_style(btn, "rgb(20, 20, 40)", "rgb(50, 50, 80)")

        self.count_time = 0
        self.count_time_limit += 1
        self.count_player = 0
        self.is_bot = True
        self.score += 1
        self.update_score()

        self.timer.start(500)

    def dead(self):
        self.game_over = True
        self.is_bot = True
        self.timer.stop()
        self.prom_time.stop()
        for i in self.buttons:
            for j in i:
                j.setEnabled(False)
                self.set_btn_style(j, "rgb(40, 10, 10)", "rgb(100, 20, 20)")


def my_excepthook(type, value, tback):
    traceback.print_exception(type, value, tback)


sys.excepthook = my_excepthook

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game("a")
    game.show()
    sys.exit(app.exec())
