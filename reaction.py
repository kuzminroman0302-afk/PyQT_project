import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGridLayout, QMessageBox, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor


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