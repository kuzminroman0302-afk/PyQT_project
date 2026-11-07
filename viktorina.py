import random
import sqlite3
import sys

from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer, QSoundEffect
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QStackedWidget,
    QLabel, QPushButton, QRadioButton, QButtonGroup, QGraphicsDropShadowEffect, QMessageBox
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QColor


class History(QWidget):
    def __init__(self, login):
        super().__init__()
        self.login = login

        one_question = random.sample(["862 год", "988 год", "1147 год", "1237 год"], k=4)
        two_question = random.sample(["Иван III", "Иван IV Грозный", "Пётр I", "Борис Годунов"], k=4)
        three_question = random.sample(["1240 год", "1380 год", "1480 год", "1552 год"], k=4)
        four_question = random.sample(["А.В. Суворов", "М.И. Кутузов", "П.И. Багратион", "М.Б. Барклай-де-Толли"], k=4)
        five_question = random.sample(["1700 год", "1703 год", "1712 год", "1721 год"], k=4)
        six_question = random.sample(["Запуск первого спутника", "Первый полёт человека в космос", "Создание ООН",
                            "Начало перестройки"], k=4)

        self.questions = [
            {
                "question": "В каком году произошло Крещение Руси?",
                "options": one_question,
                "correct": one_question.index("988 год")
            },
            {
                "question": "Кто был первым русским царём?",
                "options": two_question,
                "correct": two_question.index("Иван IV Грозный")
            },
            {
                "question": "В каком году состоялась Куликовская битва?",
                "options": three_question,
                "correct": three_question.index("1380 год")
            },
            {
                "question": "Кто командовал русской армией в Бородинском сражении?",
                "options": four_question,
                "correct": four_question.index("М.И. Кутузов")
            },
            {
                "question": "В каком году был основан Санкт-Петербург?",
                "options": five_question,
                "correct": five_question.index("1703 год")
            },
            {
                "question": "Какое событие произошло 12 апреля 1961 года?",
                "options": six_question,
                "correct": six_question.index("Первый полёт человека в космос")
            }
        ]
        self.current_index = 0
        self.score = 0

        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile("history.mp3"))
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
        self.setWindowTitle("История России: Викторина")
        self.setFixedSize(1540, 900)

        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                                  stop:0 #ff9a9e, stop:1 #fecfef);
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #2c3e50;
            }
            QLabel {
                background: transparent;
            }
            QPushButton {
                background-color: #8e44ad;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px 30px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #732d91;
            }
            QPushButton:pressed {
                background-color: #5e1f7a;
            }
            QRadioButton {
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid #ffffff;
                border-radius: 12px;
                padding: 20px 30px;
                font-size: 22px;
                font-weight: 600;
                spacing: 15px;
            }
            QRadioButton:hover {
                background-color: #ffffff;
                border: 2px solid #8e44ad;
            }
            QRadioButton:checked {
                background-color: #f3e5f5;
                border: 2px solid #8e44ad;
                color: #5e1f7a;
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

        self.progress_label = QLabel("Вопрос 1 из 6")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold; letter-spacing: 1px;")
        q_layout.addWidget(self.progress_label)

        question_card = QWidget()
        question_card.setStyleSheet("background-color: #ffffff; border-radius: 20px;")
        q_card_layout = QVBoxLayout(question_card)
        q_card_layout.setContentsMargins(40, 40, 40, 40)

        self.question_label = QLabel("")
        self.question_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_card_layout.addWidget(self.question_label)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 60))
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

        self.check_button = QPushButton("Ответить 🚀")
        self.check_button.setFixedHeight(70)
        self.check_button.clicked.connect(self.check_answer)
        q_layout.addWidget(self.check_button)

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
            "font-size: 24px; color: #2c3e50; background: rgba(255,255,255,0.9); border-radius: 15px; padding: 25px;")
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

        self.finish_title_label = QLabel("Викторина завершена!")
        self.finish_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.finish_title_label.setStyleSheet("font-size: 40px; font-weight: bold; color: #ffffff;")
        f_layout.addWidget(self.finish_title_label)

        self.finish_score_label = QLabel("")
        self.finish_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.finish_score_label.setStyleSheet(
            "font-size: 30px; color: #ffffff; font-weight: bold; background: #8e44ad; border-radius: 20px; padding: 20px;")
        f_layout.addWidget(self.finish_score_label)

        self.finish_message_label = QLabel("")
        self.finish_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.finish_message_label.setWordWrap(True)
        self.finish_message_label.setStyleSheet("font-size: 26px; color: #ffffff; font-weight: 500;")
        f_layout.addWidget(self.finish_message_label)

        f_layout.addStretch()

        self.restart_button = QPushButton("Выйти")
        self.restart_button.setFixedHeight(70)
        self.restart_button.setStyleSheet("background-color: #e74c3c;")
        self.restart_button.clicked.connect(self.restart_quiz)
        f_layout.addWidget(self.restart_button)

        self.stacked_widget.addWidget(self.finish_page)

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
            self.answer_title_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #ffffff;")
            self.correct_answer_label.setText("Отличная работа! Так держать! 🌟")
            self.next_button.setStyleSheet("background-color: #2ecc71;")
        else:
            self.eror_click.play()
            self.answer_status_label.setText("❌")
            self.answer_title_label.setText("Неверно")
            self.answer_title_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #ffffff;")
            correct_text = q["options"][q["correct"]]
            self.correct_answer_label.setText(f"Правильный ответ: <b>{correct_text}</b>")
            self.next_button.setStyleSheet("background-color: #e74c3c;")

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

        if percent == 100:
            self.finish_icon_label.setText("🏆")
            self.finish_message_label.setText("Блестяще! Вы настоящий знаток истории России!")
        elif percent >= 80:
            self.finish_icon_label.setText("🌟")
            self.finish_message_label.setText("Отличный результат! Вы хорошо знаете историю.")
        elif percent >= 60:
            self.finish_icon_label.setText("👍")
            self.finish_message_label.setText("Хороший результат, но есть куда стремиться.")
        elif percent >= 40:
            self.finish_icon_label.setText("📖")
            self.finish_message_label.setText("Неплохо, но стоит освежить знания.")
        else:
            self.finish_icon_label.setText("📚")
            self.finish_message_label.setText("Стоит уделить истории больше внимания. Удачи в изучении!")

        self.stacked_widget.setCurrentWidget(self.finish_page)

    def restart_quiz(self):
        total = len(self.questions)
        percent = round(self.score / total * 100)
        self.player.stop()
        if percent >= 100:
            QMessageBox.information(self, 'Победа!', 'Поздравляю вы прошли второй уровень!\n'
                                                     'Вам начислено 30 ฿.\n'
                                                     'Ex + 15')
            try:
                con = sqlite3.connect("proect.db")
                cur = con.cursor()
                s = cur.execute("SELECT money, ex, level FROM profile WHERE login=?", (self.login,)).fetchall()
                cur.execute("UPDATE profile SET money=?, ex=? WHERE login=?", (s[0][0] + 30, s[0][1] + 15, self.login))
                con.commit()
                if s[0][2] == 2:
                    cur.execute("UPDATE profile SET level=? WHERE login=?", (s[0][2] + 1, self.login))
                    con.commit()
                con.close()
            except Exception as e:
                print(e)
        else:
            QMessageBox.warning(self, 'Поражение', 'Вы ответили не на все вопросы правильно.\n'
                                                   'Попробуйте еще раз, чтобы получить награду.')

        self.close()
        from proect import Lobby
        self.lobby = Lobby(None, self.login)
        self.lobby.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = History("ads")
    game.show()
    sys.exit(app.exec())