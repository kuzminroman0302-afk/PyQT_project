import sqlite3
import sys
import random
from logging import exception

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGridLayout, QFrame)
from PyQt6.QtCore import Qt, QTimer


class Second_window(QWidget):
    def __init__(self, login, score=0, misses=0, parent=None):
        super().__init__()
        self.login = login
        self.score = score
        self.misses = misses
        self.parent_window = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🏆 Победа!")
        self.setFixedSize(700, 520)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #0b0f19, stop:1 #1e293b);
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #e2e8f0;
            }
            QLabel { background: transparent; }
        """)

        main = QVBoxLayout(self)
        main.setContentsMargins(40, 40, 40, 40)
        main.setSpacing(20)

        cup = QLabel("🏆")
        cup.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cup.setStyleSheet("font-size: 90px;")
        main.addWidget(cup)

        title = QLabel("Поздравляем!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: #fbbf24;
            font-size: 42px;
            font-weight: bold;
        """)
        main.addWidget(title)

        subtitle = QLabel("Вы прошли уровень «Реакция»!")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #38ef7d; font-size: 22px;")
        main.addWidget(subtitle)

        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            QFrame {
                background: rgba(30, 41, 59, 0.85);
                border: 2px solid #00e5ff;
                border-radius: 20px;
            }
        """)
        stats_layout = QVBoxLayout(stats_frame)
        stats_layout.setContentsMargins(30, 20, 30, 20)
        stats_layout.setSpacing(10)

        stats_title = QLabel("📊 Ваш результат")
        stats_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_title.setStyleSheet("color: #00e5ff; font-size: 20px; font-weight: bold;")
        stats_layout.addWidget(stats_title)

        score_lbl = QLabel(f"✅ Очки: {self.score}")
        score_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_lbl.setStyleSheet("color: #38ef7d; font-size: 22px; font-weight: bold;")
        stats_layout.addWidget(score_lbl)

        miss_lbl = QLabel(f"❌ Промахи: {self.misses}")
        miss_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        miss_lbl.setStyleSheet("color: #ef4444; font-size: 22px; font-weight: bold;")
        stats_layout.addWidget(miss_lbl)

        reward_lbl = QLabel("💰 Награда: +30 ฿  |  ⭐ Ex +15")
        reward_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        reward_lbl.setStyleSheet("color: #fbbf24; font-size: 20px; font-weight: bold;")
        stats_layout.addWidget(reward_lbl)

        main.addWidget(stats_frame)
        main.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.exit_btn = QPushButton("🚪 Выйти")
        self.exit_btn.setFixedSize(260, 65)
        self.exit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.exit_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #991b1b, stop:1 #ef4444);
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #b91c1c, stop:1 #ff6b6b);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #7f1d1d, stop:1 #dc2626);
            }
        """)
        self.exit_btn.clicked.connect(self.go_lobby)
        btn_layout.addWidget(self.exit_btn)

        main.addLayout(btn_layout)

    def go_lobby(self):
        from proect import Lobby
        self.lobby = Lobby(None, self.login)
        self.lobby.show()
        self.close()

class Reaction(QWidget):
    def __init__(self, login):
        super().__init__()
        self.buttons = []
        self.time = 3
        self.score = 0
        self.misses = 0
        self.initUI()
        self.login = login
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(750)

    def initUI(self):
        self.setWindowTitle("🎯 Реакция: Найди красную кнопку!")
        self.setFixedSize(1000, 900)

        self.setStyleSheet("""
            QWidget {
                background-color: #0b0f19;
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #e2e8f0;
            }
            QLabel { background: transparent; }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        top_frame = QFrame()
        top_frame.setStyleSheet("""
            QFrame {
                background: rgba(30, 41, 59, 0.8);
                border-radius: 20px;
                border: 2px solid #00e5ff;
            }
        """)
        top_layout = QHBoxLayout(top_frame)
        top_layout.setContentsMargins(20, 15, 20, 15)

        self.score_label = QLabel("Очки: 0")
        self.score_label.setStyleSheet("color: #38ef7d; font-size: 26px; font-weight: bold;")
        top_layout.addWidget(self.score_label)

        self.miss_label = QLabel("Промахи: 0")
        self.miss_label.setStyleSheet("color: #ef4444; font-size: 26px; font-weight: bold;")
        top_layout.addWidget(self.miss_label)

        top_layout.addStretch()

        self.stage_label = QLabel("Этап: 1 / 4")
        self.stage_label.setStyleSheet("color: #fbbf24; font-size: 26px; font-weight: bold;")
        top_layout.addWidget(self.stage_label)

        main_layout.addWidget(top_frame)

        grid_frame = QFrame()
        grid_frame.setStyleSheet("background: transparent;")
        grid_layout = QGridLayout(grid_frame)
        grid_layout.setSpacing(12)

        x, y = 0, 0
        for i in range(25):
            btn = QPushButton(self)
            btn.setFixedSize(150, 130)
            btn.setText("")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(self._btn_green_style())
            btn.clicked.connect(lambda checked=False, idx=i: self.click(idx))
            self.buttons.append([btn, "green", False])
            grid_layout.addWidget(btn, y, x)
            x += 1
            if x > 4:
                x = 0
                y += 1

        main_layout.addWidget(grid_frame)

        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.restart_btn = QPushButton("🔄 Начать заново")
        self.restart_btn.setFixedHeight(60)
        self.restart_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.restart_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00e5ff, stop:1 #0072ff);
                color: white;
                border: none;
                border-radius: 15px;
                padding: 15px 40px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #33ebff, stop:1 #338cff);
            }
        """)
        self.restart_btn.clicked.connect(self.restart)
        bottom_layout.addWidget(self.restart_btn)

        main_layout.addLayout(bottom_layout)

    def win(self):
        if self.score == 1 and self.misses == 0:
            try:
                print(self.login)
                con = sqlite3.connect("proect.db")
                cur = con.cursor()
                money, ex, level = cur.execute("SELECT money, ex, level FROM profile WHERE login=?", (self.login,)).fetchone()
                if level == 3:
                    level += 1
                cur.execute("update profile set money=?, ex=?, level=? WHERE login=?", (money + 30, ex + 15, level, self.login))
                con.commit()
                con.close()

                self.a = Second_window(self.login, self.score, self.misses)
                self.a.show()
                self.timer.stop()
            except Exception as e:
                print(e)
    def _btn_green_style(self):
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #11998e, stop:1 #38ef7d);
                border: 3px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
            }
            QPushButton:hover {
                border: 3px solid #38ef7d;
            }
        """

    def _btn_red_style(self):
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #991b1b, stop:1 #ef4444);
                border: 3px solid #ef4444;
                border-radius: 20px;
            }
        """

    def tick(self):
        for i, j in enumerate(self.buttons):
            j[0].setStyleSheet(self._btn_green_style())
            j[1] = "green"
            j[2] = False


        if self.time == 3:
            red_indices = [1, 2, 3, 8, 11, 12, 13, 18, 21, 22, 23]
        elif self.time == 2:
            red_indices = [1, 2, 3, 8, 11, 12, 13, 16, 21, 22, 23]
        elif self.time == 1:
            red_indices = [2, 7, 12, 17, 22]
        else:
            red_indices = [random.randint(0, 24)]

        for i in red_indices:
            self.buttons[i][0].setStyleSheet(self._btn_red_style())

            self.buttons[i][1] = "red"
        if self.time >= 0:
            self.stage_label.setText(f"Этап: {4 - self.time} / 4")
        self.time -= 1
        self.win()


    def click(self, ind):
        if self.buttons[ind][2] is False and self.time < 0:
            if self.buttons[ind][1] == "red":
                self.score += 1
                self.score_label.setText(f"Очки: {self.score}")
                self.buttons[ind][2] = True
            else:
                self.misses += 1
                self.miss_label.setText(f"Промахи: {self.misses}")
                self.buttons[ind][2] = True

    def restart(self):
        self.score = 0
        self.misses = 0
        self.time = 3
        self.score_label.setText("Очки: 0")
        self.miss_label.setText("Промахи: 0")
        self.stage_label.setText("Этап: 1 / 4")
        for i, j in enumerate(self.buttons):
            j[0].setStyleSheet(self._btn_green_style())
            j[1] = "green"
        self.timer.start(750)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Reaction()
    game.show()
    sys.exit(app.exec())