import random
import sqlite3
import sys

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QColor
from PyQt6.QtMultimedia import QSoundEffect, QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QGraphicsDropShadowEffect
)


class TetrisGame(QWidget):
    def __init__(self, login):
        super().__init__()
        self.login = login

        self.game_over = False

        self.SHAPES = [
            [[1]],
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[0, 1, 0], [1, 1, 1]],
            [[1, 0, 0], [1, 1, 1]],
            [[0, 0, 1], [1, 1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 0], [0, 1, 1]]
        ]

        self.colors = [
            "#00e5ff", "#fbbf24", "#a855f7", "#38bdf8",
            "#f97316", "#38ef7d", "#ef4444"
        ]

        self.cord = []
        self.all_cord = []
        self.score = 0

        self.over = QSoundEffect()
        self.over.setSource(QUrl.fromLocalFile("over.wav"))
        self.over.setVolume(0.3)

        self.audio_output = QAudioOutput()
        self.tetris = QMediaPlayer()
        self.tetris.setAudioOutput(self.audio_output)
        self.tetris.setSource(QUrl.fromLocalFile("tetris.mp3"))
        self.tetris.setLoops(QMediaPlayer.Loops.Infinite)
        self.audio_output.setVolume(0.3)

        self.con = sqlite3.connect("proect.db")
        self.cur = self.con.cursor()
        self.money, self.ex, self.level, self.record, self.music = self.cur.execute(
            "SELECT money, ex, level, record_tetris, music FROM profile WHERE login=?", (self.login,)).fetchone()

        self.initUI()
        self.spawn()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(500)

    def initUI(self):
        if self.music == 1:
            self.tetris.play()
        self.setWindowTitle("🧱 Тетрис")
        self.setGeometry(300, 30, 900, 900)
        self.setFixedSize(1000, 900)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.setStyleSheet("""
            QWidget {
                background-color: #0b0f19;
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #e2e8f0;
            }
            QLabel { background: transparent; }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        self.field_frame = QFrame()
        self.field_frame.setFixedSize(620, 820)
        self.field_frame.setStyleSheet("""
            QFrame {
                background-color: #131c31;
                border: 2px solid #00e5ff;
                border-radius: 15px;
            }
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 229, 255, 100))
        shadow.setOffset(0, 0)
        self.field_frame.setGraphicsEffect(shadow)

        y = 10
        self.buttons = []
        for i in range(13):
            x = 10
            m = []
            for j in range(10):
                self.btn = QPushButton(self.field_frame)
                self.btn.setFixedSize(55, 55)
                self.btn.move(x, y)
                self.btn.setStyleSheet("background: black; border: 1px solid #1e293b; border-radius: 5px;")
                self.btn.setEnabled(False)
                m.append(self.btn)
                x += 60
            y += 60
            self.buttons.append(m)

        main_layout.addWidget(self.field_frame)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_layout.setSpacing(20)

        title = QLabel("ТЕТРИС")
        title.setStyleSheet("font-size: 42px; font-weight: bold; color: #00e5ff; letter-spacing: 2px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(title)

        self.record_label = QLabel(f"Рекорд: {self.record}")
        self.record_label.setStyleSheet("""
            font-size: 24px; font-weight: bold; color: black;
            background: yellow; padding: 15px; border-radius: 10px;
            border: 2px solid red;
        """)
        self.record_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.record_label)

        self.score_label = QLabel("Очки: 0")
        self.score_label.setStyleSheet("""
            font-size: 24px; font-weight: bold; color: #38ef7d;
            background: #1e293b; padding: 15px; border-radius: 10px;
            border: 2px solid #38ef7d;
        """)
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.score_label)

        info_frame = QFrame()
        info_frame.setStyleSheet("background: #1e293b; border-radius: 10px; padding: 10px;")
        info_layout = QVBoxLayout(info_frame)

        info_text = QLabel(
            "Управление:\n\n"
            "⬅️ Влево\n"
            "➡️ Вправо\n"
            "⬇️ Вниз\n"
            "⬆️ Поворот\n\n"
            "Собирайте линии!"
        )
        info_text.setStyleSheet("font-size: 18px; color: #94a3b8; line-height: 1.5;")
        info_layout.addWidget(info_text)
        right_layout.addWidget(info_frame)

        right_layout.addStretch()

        self.btn_restart = QPushButton("Restart")
        self.btn_restart.setFixedSize(220, 60)
        self.btn_restart.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_restart.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 purple, stop:1 purple);
                        color: white; border: none; border-radius: 15px;
                        font-size: 18px; font-weight: bold;
                    }
                    QPushButton:hover { background: purple; }
                    QPushButton:pressed { background: purple; }
                """)
        self.btn_restart.clicked.connect(self.restart)
        right_layout.addWidget(self.btn_restart)

        self.btn_exit = QPushButton("🚪 Выйти в лобби")
        self.btn_exit.setFixedSize(220, 60)
        self.btn_exit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #dc2626, stop:1 #ef4444);
                color: white; border: none; border-radius: 15px;
                font-size: 18px; font-weight: bold;
            }
            QPushButton:hover { background: #ef4444; }
            QPushButton:pressed { background: #b91c1c; }
        """)
        self.btn_exit.clicked.connect(self.exit_to_lobby)
        right_layout.addWidget(self.btn_exit)

        main_layout.addLayout(right_layout)

        self.game_over_label = QLabel("GAME\nOVER", self)
        self.game_over_label.setStyleSheet("""
            font-size: 60px; font-weight: bold; color: #ef4444;
            background: rgba(15, 23, 42, 0.9); border: 3px solid #ef4444;
            border-radius: 20px; padding: 20px;
        """)
        self.game_over_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.game_over_label.setFixedSize(300, 200)
        self.game_over_label.move(350, 300)
        self.game_over_label.hide()

    def restart(self):
        self.timer.stop()
        self.tetris.stop()
        self.restart_res = TetrisGame(self.login)
        self.close()
        self.restart_res.show()

    def spawn(self):
        self.shape = random.choice(self.SHAPES)
        self.color = random.choice(self.colors)

        self.cord = []
        for i, j in enumerate(self.shape):
            for m, k in enumerate(j):
                if k == 1:
                    if i == 0:
                        self.cord.append((4 + m, 0))
                    else:
                        self.cord.append((4 + m, 1))

        self.cord.append(self.color)
        self.all_cord.append(self.cord)

        for x, y in self.cord[:-1]:
            c = []
            for s in self.all_cord[:-1]:
                for pos in s[:-1]:
                    c.append(pos)
            if (x, y) in c:
                self.timer.stop()
                self.game_over = True
                if self.music == 1:
                    self.over.play()
                self.game_over_label.show()
                return

    def tick(self):
        if self.check_collision(0, 1):
            self.check_lines()
            self.spawn()
            return

        new_all_cord = []
        for i in self.all_cord:
            if i == self.all_cord[-1]:
                new = [(x, y + 1) for x, y in i[:-1]] + [i[-1]]
                new_all_cord.append(new)
                self.cord = new
            else:
                new_all_cord.append(i)
        self.all_cord = new_all_cord
        self.redraw()

    def check_collision(self, dx, dy):
        c = []
        for i in self.all_cord[:-1]:
            for j in i[:-1]:
                c.append(j)

        for x, y in self.all_cord[-1][:-1]:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx > 9 or ny > 12:
                return True
            if (nx, ny) in c:
                return True
        return False

    def new(self, n):
        if not self.check_collision(n, 0):
            new_all_cord = []
            for i in self.all_cord:
                if i == self.all_cord[-1]:
                    new = [(x + n, y) for x, y in i[:-1]] + [i[-1]]
                    new_all_cord.append(new)
                    self.cord = new
                else:
                    new_all_cord.append(i)
            self.all_cord = new_all_cord
            self.redraw()

    def rotate(self):
        new_coords = []
        min_x = min(x for x, y in self.all_cord[-1][:-1])
        min_y = min(y for x, y in self.all_cord[-1][:-1])

        for x, y in self.all_cord[-1][:-1]:
            new_coords.append((y - min_y, -(x - min_x)))

        c_final = []
        for x, y in new_coords:
            new_x = x - min(x for x, y in new_coords) + min_x
            new_y = y - min(y for x, y in new_coords) + min_y
            c_final.append((new_x, new_y))

        fall = []
        for shape in self.all_cord[:-1]:
            for pos in shape[:-1]:
                fall.append(pos)
        for nx, ny in c_final:
            if nx < 0 or nx > 9 or ny > 12 or ny < 0:
                return
            if (nx, ny) in fall:
                return

        self.all_cord[-1] = c_final + [self.all_cord[-1][-1]]
        self.redraw()

    def check_lines(self):
        clear = []
        for y in range(13):
            count = 0
            for i in self.all_cord:
                for x, sy in i[:-1]:
                    if sy == y:
                        count += 1
            if count == 10:
                clear.append(y)

        if not clear:
            return

        for y in clear:
            for i in self.all_cord:
                i[:] = [(x, sy) for x, sy in i[:-1] if sy != y] + [i[-1]]
            self.all_cord = [i for i in self.all_cord if len(i) > 1]

        for i in self.all_cord:
            new_coords = []
            for x, y in i[:-1]:
                s = sum(1 for row in clear if row > y)
                new_coords.append((x, y + s))
            i[:-1] = new_coords

        self.score += len(clear) * 10
        if self.score > self.record:
            self.record = self.score
        self.score_label.setText(f"Очки: {self.score}")
        self.record_label.setText(f"Рекорд: {self.record}")
        self.redraw()

    def redraw(self):
        for i in self.buttons:
            for j in i:
                j.setStyleSheet("background: black; border: 1px solid #1e293b; border-radius: 5px;")
        for i in self.all_cord:
            for x, y in i[:-1]:
                self.buttons[y][x].setStyleSheet(f"background: {i[-1]}; border: 1px solid #1e293b; border-radius: 5px;")

    def keyPressEvent(self, event):
        if self.game_over:
            return
        if event.key() == Qt.Key.Key_Left:
            self.new(-1)
        elif event.key() == Qt.Key.Key_Right:
            self.new(1)
        elif event.key() == Qt.Key.Key_Up:
            self.rotate()
        elif event.key() == Qt.Key.Key_Down:
            self.tick()

    def exit_to_lobby(self):
        self.tetris.stop()
        self.timer.stop()
        self.close()
        if self.score > self.record:
            self.record = self.score
        if self.score >= 100:
            if self.level == 7:
                self.level += 1
            self.cur.execute("Update profile set money=?, ex=?, level=?, record_tetris=? WHERE login=?",
                             (self.money + 50, self.ex + 30, self.level, self.record, self.login)).fetchone()
            self.con.commit()
            self.con.close()
        from proect import Lobby
        self.lobby = Lobby(None, self.login)
        self.lobby.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = TetrisGame("s")
    game.show()
    sys.exit(app.exec())
