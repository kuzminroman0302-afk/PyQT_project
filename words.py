import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QMessageBox, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPen


class GallowsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 400)
        self.errors = 0

    def set_errors(self, errors):
        self.errors = errors
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(QColor("#00e5ff"))
        pen.setWidth(6)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(pen)

        p.drawLine(50, 380, 250, 380)
        p.drawLine(150, 380, 150, 50)
        p.drawLine(150, 50, 250, 50)
        p.drawLine(250, 50, 250, 100)

        pen.setColor(QColor("#ef4444"))
        pen.setWidth(5)
        p.setPen(pen)

        if self.errors >= 1:
            p.drawEllipse(230, 100, 40, 40)
        if self.errors >= 2:
            p.drawLine(250, 140, 250, 240)
        if self.errors >= 3:
            p.drawLine(250, 160, 210, 200)
        if self.errors >= 4:
            p.drawLine(250, 160, 290, 200)
        if self.errors >= 5:
            p.drawLine(250, 240, 210, 300)
        if self.errors >= 6:
            p.drawLine(250, 240, 290, 300)


class HangmanGame(QWidget):
    def __init__(self, login):
        super().__init__()
        self.login = login
        self.words = [
            ("ПРОГРАММА", "Код, который выполняется на компьютере"),
            ("КОМПЬЮТЕР", "Электронная вычислительная машина"),
            ("КЛАВИАТУРА", "Устройство ввода текста"),
            ("МОНИТОР", "Устройство вывода изображения"),
            ("АЛГОРИТМ", "Последовательность действий для решения задачи"),
            ("ПИТОН", "Язык программирования"),
            ("ИНТЕРНЕТ", "Всемирная сеть"),
            ("КРИСТАЛЛ", "То, что мы добываем в кликере"),
        ]
        self.current_word = ""
        self.hint = ""
        self.guessed_letters = set()
        self.errors = 0
        self.max_errors = 6
        self.letter_inputs = []
        self.initUI()
        self.start_new_game()

    def initUI(self):
        self.setWindowTitle("Виселица")
        self.setFixedSize(1000, 850)

        self.setStyleSheet("""
            QWidget {
                background-color: #0b0f19;
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #e2e8f0;
            }
            QLabel { background: transparent; }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00e5ff, stop:1 #0072ff);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #33ebff, stop:1 #338cff);
            }
            QPushButton:disabled {
                background: #1e293b;
                color: #475569;
                border: 2px solid #334155;
            }
            QLineEdit {
                background: rgba(30, 41, 59, 0.7);
                color: #00e5ff;
                border: 2px solid #00e5ff;
                border-radius: 10px;
                font-size: 28px;
                font-weight: bold;
                text-align: center;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title = QLabel("ВИСЕЛИЦА")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #00e5ff; font-size: 36px; font-weight: 900; letter-spacing: 3px;")
        main_layout.addWidget(title)

        center_layout = QHBoxLayout()
        center_layout.setSpacing(20)

        self.gallows = GallowsWidget()
        center_layout.addWidget(self.gallows)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(20)

        self.slots_layout = QHBoxLayout()
        self.slots_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.slots_layout.setSpacing(8)
        right_layout.addLayout(self.slots_layout)

        self.hint_label = QLabel("")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hint_label.setWordWrap(True)
        self.hint_label.setStyleSheet("color: #94a3b8; font-size: 18px; font-style: italic;")
        right_layout.addWidget(self.hint_label)

        self.errors_label = QLabel("Ошибок: 0 / 6")
        self.errors_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.errors_label.setStyleSheet("color: #ef4444; font-size: 20px; font-weight: bold;")
        right_layout.addWidget(self.errors_label)

        self.new_game_btn = QPushButton("🔄 Новая игра")
        self.new_game_btn.setFixedHeight(60)
        self.new_game_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.new_game_btn.clicked.connect(self.start_new_game)
        right_layout.addWidget(self.new_game_btn)

        right_layout.addStretch()
        center_layout.addLayout(right_layout)
        main_layout.addLayout(center_layout)

        keyboard_layout = QGridLayout()
        keyboard_layout.setSpacing(8)
        keyboard_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        row = 0
        col = 0
        self.buttons = {}

        for letter in letters:
            btn = QPushButton(letter)
            btn.setFixedSize(60, 60)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e293b, stop:1 #334155);
                    color: white;
                    border: 2px solid #475569;
                    border-radius: 12px;
                    font-size: 22px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #334155, stop:1 #475569);
                    border: 2px solid #00e5ff;
                }
                QPushButton:disabled {
                    background: #0f172a;
                    color: #334155;
                    border: 2px solid #1e293b;
                }
            """)
            btn.clicked.connect(lambda checked, l=letter: self.guess_letter(l))
            keyboard_layout.addWidget(btn, row, col)
            self.buttons[letter] = btn

            col += 1
            if col > 10:
                col = 0
                row += 1

        main_layout.addLayout(keyboard_layout)

    def start_new_game(self):
        self.current_word, self.hint = random.choice(self.words)
        self.guessed_letters = set()
        self.errors = 0
        self.gallows.set_errors(0)
        self.hint_label.setText(f"💡 {self.hint}")
        self.errors_label.setText("Ошибок: 0 / 6")

        for inp in self.letter_inputs:
            inp.deleteLater()
        self.letter_inputs.clear()

        while self.slots_layout.count():
            item = self.slots_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for _ in self.current_word:
            edit = QLineEdit()
            edit.setFixedSize(50, 60)
            edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
            edit.setMaxLength(1)
            edit.setReadOnly(True)
            edit.setStyleSheet("""
                QLineEdit {
                    background: rgba(30, 41, 59, 0.7);
                    color: #00e5ff;
                    border: 2px solid #00e5ff;
                    border-radius: 10px;
                    font-size: 28px;
                    font-weight: bold;
                }
            """)
            self.slots_layout.addWidget(edit)
            self.letter_inputs.append(edit)

        for btn in self.buttons.values():
            btn.setEnabled(True)
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e293b, stop:1 #334155);
                    color: white;
                    border: 2px solid #475569;
                    border-radius: 12px;
                    font-size: 22px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #334155, stop:1 #475569);
                    border: 2px solid #00e5ff;
                }
            """)

    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return
        self.guessed_letters.add(letter)

        btn = self.buttons[letter]
        btn.setEnabled(False)

        if letter in self.current_word:
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #11998e, stop:1 #38ef7d);
                    color: white;
                    border: 2px solid #38ef7d;
                    border-radius: 12px;
                    font-size: 22px;
                    font-weight: bold;
                }
            """)
            for i, letter in enumerate(self.current_word):
                if letter in self.guessed_letters:
                    edit = self.letter_inputs[i]
                    edit.setText(letter)
                    edit.setStyleSheet("""
                        QLineEdit {
                            background: rgba(56, 239, 125, 0.1);
                            color: #38ef7d;
                            border: 2px solid #38ef7d;
                            border-radius: 10px;
                            font-size: 28px;
                            font-weight: bold;
                        }
                    """)
            self.check_win()
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #991b1b, stop:1 #ef4444);
                    color: white;
                    border: 2px solid #ef4444;
                    border-radius: 12px;
                    font-size: 22px;
                    font-weight: bold;
                }
            """)
            self.errors += 1
            self.gallows.set_errors(self.errors)
            self.errors_label.setText(f"Ошибок: {self.errors} / {self.max_errors}")
            self.check_lose()


    def check_win(self):
        if all(letter in self.guessed_letters for letter in self.current_word):
            for btn in self.buttons.values():
                btn.setEnabled(False)
            QMessageBox.information(self, "🎉 Победа!", f"Вы угадали слово: {self.current_word}")

    def check_lose(self):
        if self.errors >= self.max_errors:
            for btn in self.buttons.values():
                btn.setEnabled(False)
            for i, letter in enumerate(self.current_word):
                edit = self.letter_inputs[i]
                edit.setText(letter)
                edit.setStyleSheet("""
                    QLineEdit {
                        background: rgba(239, 68, 68, 0.1);
                        color: #ef4444;
                        border: 2px solid #ef4444;
                        border-radius: 10px;
                        font-size: 28px;
                        font-weight: bold;
                    }
                """)
            QMessageBox.critical(self, "💀 Поражение", f"Вы не угадали слово: {self.current_word}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = HangmanGame()
    game.show()
    sys.exit(app.exec())