import json
import sys
import random

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox,
    QDialog, QVBoxLayout
)
from PyQt6.QtCore import Qt, QTimer


class WinDialog(QDialog):
    def __init__(self, parent, choice, win_value, win, balance):
        super().__init__(parent)
        self.setWindowTitle("🎉 Победа!")
        self.setFixedSize(500, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a2e;
                border: 4px solid #FFD700;
                border-radius: 20px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("🎉 ПОБЕДА! 🎉")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 36px;
            color: #FFD700;
            font-weight: bold;
            font-family: Georgia;
        """)
        layout.addWidget(title)

        crown = QLabel("👑")
        crown.setAlignment(Qt.AlignmentFlag.AlignCenter)
        crown.setStyleSheet("font-size: 80px;")
        layout.addWidget(crown)

        info = QLabel(
            f"Вы поставили на:  x{choice}\n"
            f"Выпало:           x{win_value}\n"
            f"Выигрыш:          +{win} 💰\n"
            f"Баланс:           {balance} 💰"
        )
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("""
            font-size: 20px;
            color: white;
            font-family: Consolas;
            background-color: rgba(255, 215, 0, 0.15);
            border-radius: 10px;
            padding: 15px;
        """)
        layout.addWidget(info)

        btn = QPushButton("ЗАБРАТЬ ВЫИГРЫШ")
        btn.setFixedHeight(55)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #FFD700;
                color: #8B0000;
                border: 3px solid white;
                border-radius: 25px;
                font-size: 22px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #FFE44D; }
            QPushButton:pressed { background-color: #DAA520; }
        """)
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)


class LoseDialog(QDialog):
    def __init__(self, parent, choice, win_value, bet, balance):
        super().__init__(parent)
        self.setWindowTitle("😢 Поражение")
        self.setFixedSize(500, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a2e;
                border: 4px solid #8B0000;
                border-radius: 20px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("😢 ПОРАЖЕНИЕ 😢")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 36px;
            color: #FF5555;
            font-weight: bold;
            font-family: Georgia;
        """)
        layout.addWidget(title)

        sad = QLabel("💸")
        sad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sad.setStyleSheet("font-size: 80px;")
        layout.addWidget(sad)

        info = QLabel(
            f"Вы поставили на:  x{choice}\n"
            f"Выпало:           x{win_value}\n"
            f"Потеряно:         -{bet} 💰\n"
            f"Баланс:           {balance} 💰"
        )
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("""
            font-size: 20px;
            color: white;
            font-family: Consolas;
            background-color: rgba(139, 0, 0, 0.3);
            border-radius: 10px;
            padding: 15px;
        """)
        layout.addWidget(info)

        btn = QPushButton("ПОПРОБОВАТЬ СНОВА")
        btn.setFixedHeight(55)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #8B0000;
                color: white;
                border: 3px solid #FFD700;
                border-radius: 25px;
                font-size: 22px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #A52A2A; }
            QPushButton:pressed { background-color: #5C0000; }
        """)
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

class Casino(QWidget):
    def __init__(self, login):
        super().__init__()
        self.login = login
        self.count = 0
        with open("info.json", "r") as f:
            self.prof = json.load(f)
            self.balance = self.prof[login]["money"]
        self.bet = 0
        self.user_choice = None

        self.values = [2, 2, 2, 2, 2, 3, 3, 3, 3, 5, 5, 10, 10, 25]
        self.casino_lst = random.sample(self.values, k=3)

        self.buttons = []
        self.choice_buttons = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle("КАЗИНО")
        self.setFixedSize(1000, 900)
        self.setStyleSheet("background-color: #1a1a2e;")

        self.label_casino = QLabel("🎰 КАЗИНО 🎰", self)
        self.label_casino.setGeometry(0, 20, 1000, 50)
        self.label_casino.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_casino.setStyleSheet("""
            font-size: 36px;
            color: #FFD700;
            font-weight: bold;
            font-family: Georgia;
        """)

        self.label_balance = QLabel(f"💰 Баланс: {self.balance}", self)
        self.label_balance.setGeometry(720, 30, 260, 40)
        self.label_balance.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_balance.setStyleSheet("""
            font-size: 20px;
            color: white;
            background-color: rgba(139, 0, 0, 0.85);
            border-radius: 15px;
            padding: 5px;
        """)

        self.label_choose = QLabel("Выберите множитель:", self)
        self.label_choose.setGeometry(0, 420, 1000, 30)
        self.label_choose.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_choose.setStyleSheet("""
            font-size: 20px;
            color: #FFD700;
            font-weight: bold;
        """)

        self.create_choice_buttons()

        self.dep_edit = QLineEdit(self)
        self.dep_edit.setGeometry(300, 620, 400, 55)
        self.dep_edit.setPlaceholderText("Введите ставку...")
        self.dep_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dep_edit.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 240, 245, 0.95);
                border: 3px solid #FFD700;
                border-radius: 25px;
                font-size: 22px;
                color: #4B0082;
                padding: 8px;
            }
        """)

        self.btn_spin = QPushButton("🎲 КРУТИТЬ 🎲", self)
        self.btn_spin.setGeometry(350, 700, 300, 60)
        self.btn_spin.setStyleSheet("""
            QPushButton {
                background-color: #8B0000;
                color: white;
                border: 3px solid #FFD700;
                border-radius: 30px;
                font-size: 26px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #A52A2A; }
            QPushButton:pressed { background-color: #5C0000; }
        """)
        self.btn_spin.clicked.connect(self.spin)

        self.btn_exit = QPushButton("ВЫХОД", self)
        self.btn_exit.setGeometry(10, 840, 300, 60)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background-color: #8B0000;
                color: white;
                border: 3px solid #FFD700;
                border-radius: 30px;
                font-size: 26px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #A52A2A; }
            QPushButton:pressed { background-color: #5C0000; }
        """)
        self.btn_exit.clicked.connect(self.exit)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.iter)

        self.draw_cards()

    def exit(self):
        from proect import Lobby
        with open("info.json", "w") as f:
            self.prof[self.login]["money"] = self.balance
            json.dump(self.prof, f)
        self.close()
        self.lobby = Lobby(None, self.login)
        self.lobby.show()

    def create_choice_buttons(self):
        multipliers = [2, 3, 5, 10, 25]
        btn_w = 130
        gap = 20
        total_w = len(multipliers) * btn_w + (len(multipliers) - 1) * gap
        start_x = (1000 - total_w) // 2
        y = 470

        for i, m in enumerate(multipliers):
            btn = QPushButton(f"x{m}", self)
            btn.setGeometry(start_x + i * (btn_w + gap), y, btn_w, 70)
            btn.setStyleSheet(self.choice_style(False))
            btn.clicked.connect(lambda _, val=m: self.select_multiplier(val))
            btn.show()
            self.choice_buttons.append((m, btn))

    def choice_style(self, selected):
        if selected:
            return """
                QPushButton {
                    background-color: #FFD700;
                    color: #8B0000;
                    border: 4px solid white;
                    border-radius: 20px;
                    font-size: 24px;
                    font-weight: bold;
                }
            """
        return """
            QPushButton {
                background-color: #6A0DAD;
                color: white;
                border: 3px solid #FFD700;
                border-radius: 20px;
                font-size: 24px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #8A2BE2; }
        """

    def select_multiplier(self, value):
        self.user_choice = value
        for m, btn in self.choice_buttons:
            btn.setStyleSheet(self.choice_style(m == value))

    def draw_cards(self):
        for btn in self.buttons:
            btn.deleteLater()
        self.buttons = []

        x = 50
        for value in self.casino_lst:
            btn = QPushButton(f"x{value}", self)
            btn.setGeometry(x, 100, 300, 300)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #6A0DAD;
                    color: white;
                    border: 4px solid #FFD700;
                    border-radius: 20px;
                    font-size: 60px;
                    font-weight: bold;
                }
            """)
            btn.show()
            self.buttons.append(btn)
            x += 310

    def spin(self):
        if self.timer.isActive():
            return

        if self.user_choice is None:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите множитель!")
            return

        try:
            bet = int(self.dep_edit.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите целое число!")
            return

        if bet <= 0:
            QMessageBox.warning(self, "Ошибка", "Ставка должна быть > 0!")
            return

        if bet > self.balance:
            QMessageBox.warning(self, "Ошибка", "Недостаточно средств!")
            return

        self.bet = bet
        self.balance -= bet
        self.label_balance.setText(f"💰 Баланс: {self.balance}")

        self.count = 0
        self.timer.start(150)

    def iter(self):
        self.count += 1

        if self.count >= 60:
            self.timer.stop()
            self.stop()
            return

        new_val = random.choice(self.values)
        self.casino_lst = [new_val, self.casino_lst[0], self.casino_lst[1]]
        self.draw_cards()

    def stop(self):
        win_value = self.casino_lst[1]

        if win_value == self.user_choice:
            win = self.bet * win_value
            self.balance += win
            self.label_balance.setText(f"💰 Баланс: {self.balance}")

            dlg = WinDialog(self, self.user_choice, win_value, win, self.balance)
            dlg.exec()
        else:
            dlg = LoseDialog(self, self.user_choice, win_value, self.bet, self.balance)
            dlg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Casino("ads")
    game.show()
    sys.exit(app.exec())