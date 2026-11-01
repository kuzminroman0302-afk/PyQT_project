import sqlite3
import sys
import random

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor


class SnakeGame(QWidget):
    def __init__(self, login):
        super().__init__()
        self.snake = [[10, 10], [9, 10], [8, 10]]
        self.login = login
        self.buttons = []
        self.apple = [random.randint(0, 19), random.randint(0, 19)]
        self.move_x = 1
        self.move_y = 0
        self.score = 0
        self.game_over = False

        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(250)

    def initUI(self):
        self.setWindowTitle("🐍 Змейка")
        self.setFixedSize(1000, 900)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.setStyleSheet("""
            QWidget {
                background-color: #0b0f19;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel { background: transparent; }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(8)

        top_frame = QFrame()
        top_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(30, 41, 59, 0.9), stop:1 rgba(15, 23, 42, 0.9));
                border-radius: 15px;
                border: 2px solid #00e5ff;
            }
        """)
        top_layout = QHBoxLayout(top_frame)
        top_layout.setContentsMargins(20, 8, 20, 8)

        self.score_label = QLabel("Очки: 0")
        self.score_label.setStyleSheet("color: #38ef7d; font-size: 22px; font-weight: bold;")
        top_layout.addWidget(self.score_label)

        top_layout.addStretch()

        self.status_label = QLabel("🟢 Игра идёт")
        self.status_label.setStyleSheet("color: #00e5ff; font-size: 18px; font-weight: bold;")
        top_layout.addWidget(self.status_label)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 229, 255, 120))
        shadow.setOffset(0, 0)
        top_frame.setGraphicsEffect(shadow)

        main_layout.addWidget(top_frame)

        self.field_frame = QFrame()
        self.field_frame.setStyleSheet("""
            QFrame#fieldFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #131c31, stop:1 #0a1122);
                border-radius: 20px;
                border: 2px solid #1e293b;
            }
        """)
        self.field_frame.setObjectName("fieldFrame")

        field_shadow = QGraphicsDropShadowEffect(self)
        field_shadow.setBlurRadius(30)
        field_shadow.setColor(QColor(0, 229, 255, 80))
        field_shadow.setOffset(0, 5)
        self.field_frame.setGraphicsEffect(field_shadow)

        self.grid_layout = QGridLayout(self.field_frame)
        self.grid_layout.setHorizontalSpacing(4)
        self.grid_layout.setVerticalSpacing(4)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)

        for y in range(20):
            row = []
            for x in range(20):
                btn = QPushButton()
                btn.setFixedSize(28, 28)
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                btn.setEnabled(False)
                btn.setStyleSheet(self.empty_cell_style())
                row.append(btn)
                self.grid_layout.addWidget(btn, y, x)
            self.buttons.append(row)

        main_layout.addWidget(self.field_frame)

        controls_frame = QFrame()
        controls_layout = QGridLayout(controls_frame)
        controls_layout.setSpacing(8)
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e293b, stop:1 #334155);
                color: #00e5ff;
                border: 2px solid #00e5ff;
                border-radius: 15px;
                font-size: 28px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #334155, stop:1 #475569);
                border: 2px solid #33ebff;
                color: #33ebff;
            }
            QPushButton:pressed {
                background: #0ea5e9;
                color: white;
                border: 2px solid white;
            }
        """

        self.btn_up = QPushButton("▲")
        self.btn_up.setFixedSize(65, 65)
        self.btn_up.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_up.setStyleSheet(btn_style)
        self.btn_up.clicked.connect(lambda: self.click(0, -1))

        self.btn_down = QPushButton("▼")
        self.btn_down.setFixedSize(65, 65)
        self.btn_down.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_down.setStyleSheet(btn_style)
        self.btn_down.clicked.connect(lambda: self.click(0, 1))

        self.btn_left = QPushButton("◀")
        self.btn_left.setFixedSize(65, 65)
        self.btn_left.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_left.setStyleSheet(btn_style)
        self.btn_left.clicked.connect(lambda: self.click(-1, 0))

        self.btn_right = QPushButton("▶")
        self.btn_right.setFixedSize(65, 65)
        self.btn_right.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_right.setStyleSheet(btn_style)
        self.btn_right.clicked.connect(lambda: self.click(1, 0))

        controls_layout.addWidget(self.btn_up, 0, 1)
        controls_layout.addWidget(self.btn_left, 1, 0)
        controls_layout.addWidget(self.btn_right, 1, 2)
        controls_layout.addWidget(self.btn_down, 2, 1)

        main_layout.addWidget(controls_frame)

        bottom_layout = QHBoxLayout()

        self.restart_btn = QPushButton("🔄 Начать заново")
        self.restart_btn.setFixedHeight(50)
        self.restart_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.restart_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.restart_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f59e0b, stop:1 #fbbf24);
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #fbbf24, stop:1 #fcd34d);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #d97706, stop:1 #f59e0b);
            }
        """)
        self.restart_btn.clicked.connect(self.restart_game)
        bottom_layout.addWidget(self.restart_btn)

        self.btn_exit = QPushButton("🚪 Выйти в лобби")
        self.btn_exit.setFixedHeight(50)
        self.btn_exit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_exit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #dc2626, stop:1 #ef4444);
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ef4444, stop:1 #f87171);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #b91c1c, stop:1 #dc2626);
            }
        """)
        self.btn_exit.clicked.connect(self.exit_to_lobby)
        bottom_layout.addWidget(self.btn_exit)

        main_layout.addLayout(bottom_layout)

        self.setFocus()

    def exit_to_lobby(self):
        if self.score >= 20:
            con = sqlite3.connect('proect.db')
            cur = con.cursor()
            s = cur.execute("select level from profile where login=?", (self.login,)).fetchone()
            if s[0] == 6:
                cur.execute("update profile set level=? where login=?", (7, self.login))
                con.commit()
            con.close()
        self.timer.stop()
        self.close()
        from proect import Lobby
        self.lobby = Lobby(None, self.login)
        self.lobby.show()

    def empty_cell_style(self):
        return """
            QPushButton {
                background-color: #0a1122;
                border-radius: 5px;
                border: none;
            }
        """

    def apple_style(self):
        return """
            QPushButton {
                background: qradialgradient(cx:0.4, cy:0.4, radius:0.7,
                    stop:0 #ff8080, stop:0.4 #ef4444, stop:1 #991b1b);
                border-radius: 50%;
                border: 2px solid #fecaca;
            }
        """

    def head_style(self):
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #a7f3d0, stop:0.5 #38ef7d, stop:1 #11998e);
                border-radius: 6px;
                border: 2px solid #ecfdf5;
            }
        """

    def body_style(self, idx, total):
        alpha = max(0.45, 1.0 - idx / max(total, 1))
        r = int(56 + (34 - 56) * (1 - alpha))
        g = int(239 - (239 - 197) * (1 - alpha))
        b = int(125 - (125 - 94) * (1 - alpha))
        return f"""
            QPushButton {{
                background-color: rgba({r}, {g}, {b}, {alpha});
                border-radius: 6px;
                border: 1px solid rgba(167, 243, 208, {alpha * 0.6});
            }}
        """

    def update_game(self):
        new_x = self.snake[0][0] + self.move_x
        new_y = self.snake[0][1] + self.move_y

        if not (0 <= new_x < 20 and 0 <= new_y < 20):
            self.end_game()
            return

        if [new_x, new_y] in self.snake:
            self.end_game()
            return

        old_snake = [list(seg) for seg in self.snake]

        self.snake[0][0] = new_x
        self.snake[0][1] = new_y

        if self.snake[0] == self.apple:
            self.snake.append(list(old_snake[-1]))
            self.apple = [random.randint(0, 19), random.randint(0, 19)]
            self.score += 1
            self.score_label.setText(f"Очки: {self.score}")

        for i in range(1, len(self.snake)):
            self.snake[i] = old_snake[i - 1]

        for y in range(20):
            for x in range(20):
                self.buttons[y][x].setStyleSheet(self.empty_cell_style())

        ax, ay = self.apple
        self.buttons[ay][ax].setStyleSheet(self.apple_style())

        total = len(self.snake)
        for idx, (x, y) in enumerate(self.snake):
            if idx == 0:
                self.buttons[y][x].setStyleSheet(self.head_style())
            else:
                self.buttons[y][x].setStyleSheet(self.body_style(idx, total))

    def end_game(self):
        self.timer.stop()
        self.status_label.setText("💀 Игра окончена")
        self.status_label.setStyleSheet("color: #ef4444; font-size: 18px; font-weight: bold;")

    def click(self, x, y):
        self.move_x = x
        self.move_y = y

    def restart_game(self):
        self.timer.stop()
        self.snake = [[10, 10], [9, 10], [8, 10]]
        self.apple = [random.randint(0, 19), random.randint(0, 19)]
        self.move_x = 1
        self.move_y = 0
        self.score = 0
        self.score_label.setText("Очки: 0")
        self.status_label.setText("🟢 Игра идёт")
        self.status_label.setStyleSheet("color: #00e5ff; font-size: 18px; font-weight: bold;")
        self.timer.start(250)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key.Key_Up:
            if self.move_y != 1:
                self.click(0, -1)
        elif key == Qt.Key.Key_Down:
            if self.move_y != -1:
                self.click(0, 1)
        elif key == Qt.Key.Key_Left:
            if self.move_x != 1:
                self.click(-1, 0)
        elif key == Qt.Key.Key_Right:
            if self.move_x != -1:
                self.click(1, 0)
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SnakeGame("ads")
    game.show()
    sys.exit(app.exec())