import sqlite3
import sys

from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer, QSoundEffect
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QLabel, QPushButton, QRadioButton, QButtonGroup, QGraphicsDropShadowEffect, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QColor
from calculator import Calculator
import random


class Math(QWidget):
    def __init__(self, login):
        super().__init__()
        self.login = login
        one_question = random.sample(["x = 3", "x = -3", "x = 0", "x = 9"], k=4)
        two_question = random.sample(["√10", "3", "Они равны", "Невозможно сравнить"], k=4)
        three_question = random.sample(["7", "-7", "12", "-12"], k=4)
        four_question = random.sample(["10", "14", "20", "8"], k=4)
        five_question = random.sample(["(-4; 2)", "(9; 3)", "(1; -1)", "(25; 6)"], k=4)
        six_question = random.sample(["90", "180", "200", "2"], k=4)
        seven_question = random.sample(["-1", "0", "1", "2025"], k=4)
        eight_question = random.sample(["2025", "4050", "8100", "2024"], k=4)

        self.questions = [
            {
                "question": "При каких значениях x дробь (x² - 9) / (x - 3) равна нулю?",
                "options": one_question,
                "correct": one_question.index("x = -3")
            },
            {
                "question": "Какое из чисел больше: √10 или 3?",
                "options": two_question,
                "correct": two_question.index("√10")
            },
            {
                "question": "Чему равна сумма корней уравнения x² - 7x + 12 = 0?",
                "options": three_question,
                "correct": three_question.index("7")
            },
            {
                "question": "Известно, что x + y = 7, а x² + y² = 29. Чему равно произведение xy?",
                "options": four_question,
                "correct": four_question.index("10")
            },
            {
                "question": "Какая из точек принадлежит графику функции y = √x?",
                "options": five_question,
                "correct": five_question.index("(9; 3)")
            },
            {
                "question": "Вычислите значение выражения: √(2026² - 2024²)",
                "options": six_question,
                "correct": six_question.index("90")
            },
            {
                "question": "Вычислите: 2026 · 2024 - 2025²",
                "options": seven_question,
                "correct": seven_question.index("-1")
            },
            {
                "question": "Вычислите значение выражения: (2026² - 2024²) / 4",
                "options": eight_question,
                "correct": eight_question.index("2025")
            }
        ]
        self.current_index = 0
        self.score = 0

        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile("math.mp3"))
        self.player.setLoops(QMediaPlayer.Loops.Infinite)
        self.audio_output.setVolume(0.5)

        self.sound_click = QSoundEffect()
        self.sound_click.setSource(QUrl.fromLocalFile("click.wav"))
        self.sound_click.setVolume(0.2)

        self.suc_click = QSoundEffect()
        self.suc_click.setSource(QUrl.fromLocalFile("buy.wav"))
        self.suc_click.setVolume(0.2)

        self.eror_click = QSoundEffect()
        self.eror_click.setSource(QUrl.fromLocalFile("eror.wav"))
        self.eror_click.setVolume(0.2)

        self.initUI()
        self.show_question()

    def initUI(self):
        self.player.play()
        self.setWindowTitle("Математика тест")
        self.setFixedSize(1540, 900)

        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                                  stop:0 #0f172a, stop:1 #1e1b4b);
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #e2e8f0;
            }
            QLabel {
                background: transparent;
            }
            QPushButton {
                background-color: #38bdf8;
                color: #0f172a;
                border: none;
                border-radius: 12px;
                padding: 15px 30px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7dd3fc;
            }
            QPushButton:pressed {
                background-color: #0ea5e9;
            }
            QRadioButton {
                background-color: rgba(30, 41, 59, 0.8);
                border: 2px solid #334155;
                border-radius: 12px;
                padding: 20px 30px;
                font-size: 22px;
                font-weight: 600;
                spacing: 15px;
                color: #e2e8f0;
            }
            QRadioButton:hover {
                background-color: rgba(51, 65, 85, 0.9);
                border: 2px solid #38bdf8;
            }
            QRadioButton:checked {
                background-color: rgba(56, 189, 248, 0.2);
                border: 2px solid #38bdf8;
                color: #38bdf8;
            }
            QRadioButton::indicator {
                width: 25px;
                height: 25px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        self.question_page = QWidget()
        q_layout = QVBoxLayout(self.question_page)
        q_layout.setSpacing(30)

        self.progress_label = QLabel("Вопрос 1 из 8")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setStyleSheet("color: #38bdf8; font-size: 24px; font-weight: bold; letter-spacing: 2px;")
        q_layout.addWidget(self.progress_label)

        question_card = QWidget()
        question_card.setStyleSheet("background-color: #1e293b; border-radius: 20px; border: 1px solid #334155;")
        q_card_layout = QVBoxLayout(question_card)
        q_card_layout.setContentsMargins(40, 40, 40, 40)

        self.question_label = QLabel("")
        self.question_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setStyleSheet("color: #ffffff;")
        q_card_layout.addWidget(self.question_label)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(56, 189, 248, 80))
        shadow.setOffset(0, 10)
        question_card.setGraphicsEffect(shadow)

        q_layout.addWidget(question_card)

        self.button_group = QButtonGroup(self)
        self.option_buttons = []
        for i in range(4):
            rb = QRadioButton("")
            self.button_group.addButton(rb, i)
            self.option_buttons.append(rb)
            q_layout.addWidget(rb)

        q_layout.addStretch()

        bottom_layout = QHBoxLayout()

        self.check_button = QPushButton("Ответить 🚀")
        self.check_button.setFixedHeight(70)
        self.check_button.clicked.connect(self.check_answer)
        bottom_layout.addWidget(self.check_button, stretch=3)

        self.calc_button = QPushButton("🧮 Калькулятор")
        self.calc_button.setFixedHeight(70)
        self.calc_button.setStyleSheet("""
            QPushButton {
                background-color: #8b5cf6;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px 30px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #a78bfa; }
            QPushButton:pressed { background-color: #7c3aed; }
        """)
        self.calc_button.clicked.connect(self.open_calculator)
        bottom_layout.addWidget(self.calc_button, stretch=1)

        q_layout.addLayout(bottom_layout)

        self.stacked_widget.addWidget(self.question_page)

        self.answer_page = QWidget()
        a_layout = QVBoxLayout(self.answer_page)
        a_layout.setSpacing(30)
        a_layout.addStretch()

        self.answer_status_label = QLabel("")
        self.answer_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.answer_status_label.setStyleSheet("font-size: 120px;")
        a_layout.addWidget(self.answer_status_label)

        self.answer_title_label = QLabel("")
        self.answer_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        a_layout.addWidget(self.answer_title_label)

        self.correct_answer_label = QLabel("")
        self.correct_answer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.correct_answer_label.setWordWrap(True)
        self.correct_answer_label.setStyleSheet(
            "font-size: 24px; color: #ffffff; background: rgba(30, 41, 59, 0.9); border-radius: 15px; padding: 25px; border: 1px solid #334155;")
        a_layout.addWidget(self.correct_answer_label)

        a_layout.addStretch()

        self.next_button = QPushButton("Далее ➡️")
        self.next_button.setFixedHeight(70)
        self.next_button.clicked.connect(self.next_question)
        a_layout.addWidget(self.next_button)

        self.stacked_widget.addWidget(self.answer_page)

        self.finish_page = QWidget()
        f_layout = QVBoxLayout(self.finish_page)
        f_layout.setSpacing(30)
        f_layout.addStretch()

        self.finish_icon_label = QLabel("🏆")
        self.finish_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.finish_icon_label.setStyleSheet("font-size: 150px;")
        f_layout.addWidget(self.finish_icon_label)

        self.finish_title_label = QLabel("Тест завершен!")
        self.finish_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.finish_title_label.setStyleSheet("font-size: 40px; font-weight: bold; color: #38bdf8;")
        f_layout.addWidget(self.finish_title_label)

        self.finish_score_label = QLabel("")
        self.finish_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.finish_score_label.setStyleSheet(
            "font-size: 30px; color: #ffffff; font-weight: bold; background: #1e293b; border-radius: 20px; padding: 20px; border: 1px solid #38bdf8;")
        f_layout.addWidget(self.finish_score_label)

        self.finish_message_label = QLabel("")
        self.finish_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.finish_message_label.setWordWrap(True)
        self.finish_message_label.setStyleSheet("font-size: 26px; color: #e2e8f0; font-weight: 500;")
        f_layout.addWidget(self.finish_message_label)

        f_layout.addStretch()

        self.restart_button = QPushButton("Выйти")
        self.restart_button.setFixedHeight(70)
        self.restart_button.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px 30px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #f87171; }
            QPushButton:pressed { background-color: #b91c1c; }
        """)
        self.restart_button.clicked.connect(self.restart_quiz)
        f_layout.addWidget(self.restart_button)

        self.stacked_widget.addWidget(self.finish_page)

    def open_calculator(self):
        self.calc_window = Calculator()
        self.calc_window.show()

    def show_question(self):
        q = self.questions[self.current_index]
        self.progress_label.setText(f"Вопрос {self.current_index + 1} из {len(self.questions)}")
        self.question_label.setText(q["question"])

        self.button_group.setExclusive(False)
        for i, btn in enumerate(self.option_buttons):
            btn.setText(q["options"][i])
            btn.setChecked(False)
        self.button_group.setExclusive(True)

        self.stacked_widget.setCurrentWidget(self.question_page)

    def check_answer(self):
        self.sound_click.play()
        checked_id = self.button_group.checkedId()
        if checked_id == -1:
            return

        q = self.questions[self.current_index]
        is_correct = (checked_id == q["correct"])

        if is_correct:
            self.suc_click.play()
            self.score += 1
            self.answer_status_label.setText("✅")
            self.answer_title_label.setText("Верно!")
            self.answer_title_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #38ef7d;")
            self.correct_answer_label.setText("Отличная работа! Так держать! 🌟")
            self.next_button.setStyleSheet("background-color: #16a34a; color: white;")
        else:
            self.eror_click.play()
            self.answer_status_label.setText("❌")
            self.answer_title_label.setText("Неверно")
            self.answer_title_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #ef4444;")
            correct_text = q["options"][q["correct"]]
            self.correct_answer_label.setText(f"Правильный ответ: <b>{correct_text}</b>")
            self.next_button.setStyleSheet("background-color: #dc2626; color: white;")

        if self.current_index == len(self.questions) - 1:
            self.next_button.setText("Показать результат 🏁")
        else:
            self.next_button.setText("Далее ➡️")

        self.stacked_widget.setCurrentWidget(self.answer_page)

    def next_question(self):
        self.current_index += 1
        if self.current_index < len(self.questions):
            self.show_question()
        else:
            self.finish_quiz()

    def finish_quiz(self):
        total = len(self.questions)
        percent = round(self.score / total * 100)

        self.finish_score_label.setText(f"Ваш результат: {self.score} из {total} ({percent}%)")

        if self.score == 8:
            self.finish_icon_label.setText("🏆")
            self.finish_message_label.setText("Блестяще! Вы настоящий знаток математики!")
        elif self.score >= 6:
            self.finish_icon_label.setText("🌟")
            self.finish_message_label.setText("Отличный результат! Вы хорошо знаете математику.")
        elif self.score >= 4:
            self.finish_icon_label.setText("👍")
            self.finish_message_label.setText("Хороший результат, но есть куда стремиться.")
        elif self.score >= 2:
            self.finish_icon_label.setText("📖")
            self.finish_message_label.setText("Неплохо, но стоит освежить знания.")
        else:
            self.finish_icon_label.setText("📚")
            self.finish_message_label.setText("Стоит уделить математике больше внимания. Удачи в изучении!")

        self.stacked_widget.setCurrentWidget(self.finish_page)

    def restart_quiz(self):
        self.player.stop()
        if self.score == 8:
            con = sqlite3.connect("proect.db")
            cur = con.cursor()
            s = cur.execute("SELECT money, ex, level FROM profile WHERE login=?", (self.login,)).fetchone()

            if s:
                current_level = s[2]
                if current_level == 8:
                    cur.execute("UPDATE profile SET money=?, ex=?, level=? WHERE login=?",
                                (s[0] + 30, s[1] + 15, 9, self.login))
                    con.commit()
                    QMessageBox.information(self, 'Победа!', 'Поздравляю, вы прошли уровень!\n'
                                                             'Вам начислено 30 ฿.\n'
                                                             'Ex + 15\n'
                                                             'Открыт следующий уровень!')
                else:
                    QMessageBox.information(self, 'Победа!', 'Вы уже проходили этот уровень ранее.\n'
                                                             'Награда не начислена.')
            con.close()
        else:
            QMessageBox.warning(self, 'Поражение', 'Вы ответили не на все вопросы правильно.\n'
                                                   'Попробуйте еще раз, чтобы получить награду.')

        self.close()
        if hasattr(self, 'calc_window') and self.calc_window:
            self.calc_window.close()
        from proect import Lobby
        self.lobby = Lobby(None, self.login)
        self.lobby.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Math("ads")
    game.show()
    sys.exit(app.exec())
