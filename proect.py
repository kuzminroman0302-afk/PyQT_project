import json
import sys
import sqlite3

from PyQt6.QtCore import Qt, QTimer

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QApplication, QWidget, QRadioButton,
                             QPushButton, QLabel, QLineEdit,
                             QCheckBox, QMainWindow,
                             QInputDialog, QHBoxLayout, QVBoxLayout, QMessageBox)
from krestic_nolik_solo import TicTacToe_friend
from krestic_nolik_bot import TicTacToe_bot
from viktorina import History
from Clicker import ClickerUI
from words import HangmanGame
from reaction import Reaction
from snake import SnakeGame
from casino import Casino
import random

STYLE = """
QMainWindow, QDialog, QWidget {
    background-color: #0f172a;
    color: #e2e8f0;
    font-family: "Segoe UI", "Arial", sans-serif;
    font-size: 15px;
}
QLineEdit {
    background-color: #1e293b;
    border: 2px solid #334155;
    border-radius: 10px;
    padding: 6px 10px;
    color: #e2e8f0;
    font-size: 15px;
}
QLineEdit:focus { border: 2px solid #38bdf8; }
QPushButton {
    background-color: #38bdf8;
    color: #0f172a;
    border: none;
    border-radius: 10px;
    padding: 8px 16px;
    font-size: 15px;
    font-weight: bold;
}
QPushButton:hover   { background-color: #7dd3fc; }
QPushButton:pressed { background-color: #0ea5e9; }
QPushButton:disabled { background-color: #334155; color: #64748b; }
QLabel { background: transparent; color: #e2e8f0; }
QRadioButton { background: transparent; color: #e2e8f0; spacing: 6px; }
QRadioButton::indicator {
    width: 20px; height: 20px; border-radius: 10px;
    border: 2px solid #64748b; background: #1e293b;
}
QRadioButton::indicator:checked { background: #38bdf8; border: 2px solid #38bdf8; }
QCheckBox { background: transparent; }
QCheckBox::indicator {
    width: 22px; height: 22px; border-radius: 4px;
    border: 2px solid #64748b; background: #1e293b;
}
QCheckBox::indicator:checked { background: #38bdf8; border: 2px solid #38bdf8; }

QMessageBox {
    background-color: #1e293b;
}
QMessageBox QLabel {
    color: #e2e8f0;
    font-size: 15px;
}
QMessageBox QPushButton {
    background-color: #38bdf8;
    color: #0f172a;
    border: none;
    border-radius: 8px;
    padding: 6px 18px;
    font-weight: bold;
    min-width: 80px;
}
QMessageBox QPushButton:hover   { background-color: #7dd3fc; }
QMessageBox QPushButton:pressed { background-color: #0ea5e9; }
"""


class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.one = False
        self.avatar_choice = ''
        self.con = sqlite3.connect("proect.db")
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('Регистрация')
        self.setFixedSize(900, 400)
        self.main = MainWindow()
        self.login, ok_pressed_login = QInputDialog.getText(
            self, 'Знакомство', 'Введите логин.'
        )
        cur = self.con.cursor()
        s = cur.execute("select login from profile").fetchall()
        self.users = []
        for i in s:
            self.users.append(i[0])
        if self.login.strip() in self.users:
            self.hide()
            QMessageBox.warning(self, 'Предупреждение!', 'Такой логин уже существует!')
            self.main.show()
            return
        self.password, ok_pressed_password = QInputDialog.getText(
            self, 'Знакомство', 'Введите пароль.'
        )
        if not ok_pressed_login or not self.login.strip():
            self.hide()
            self.main.show()
            return
        if not ok_pressed_password or not self.password.strip():
            self.hide()
            self.main.show()
            return
        self.name, ok_pressed_name = QInputDialog.getText(
            self, 'Знакомство', 'Как тебя зовут?'
        )
        self.surname, ok_pressed_surname = QInputDialog.getText(
            self, 'Знакомство', 'Какая у тебя фамилия?'
        )
        self.age, ok_pressed_age = QInputDialog.getInt(
            self, 'Возраст', 'Сколько тебе лет?', 18, 0, 100, 1
        )
        countries = ('Россия', 'Германия', 'США', 'Япония')
        self.country, ok_pressed_country = QInputDialog.getItem(
            self, 'Откуда ты?', 'Выбери страну:', countries, 0, False
        )

        if not ok_pressed_country or not ok_pressed_age or not ok_pressed_surname or not ok_pressed_name or not ok_pressed_password or not ok_pressed_login:
            self.hide()
            self.main = MainWindow()
            self.main.show()
        else:
            self.show()

            self.choice_im = QLabel("Выбери аватарку:", self)
            self.choice_im.resize(200, 40)
            self.choice_im.move(400, 20)
            self.choice_im.setStyleSheet(
                "font-size: 20px; font-weight: bold; color: #f1f5f9;"
            )
            self.choice_im.show()

            self.avatar = ["math.jpg", "rust.jpg", "bmw.jpg", "Lion.jpg"]
            self.avatar_ch = []
            self.box_ch = []
            x = 50
            y = 100
            x1 = 130
            y1 = 320

            for j, i in enumerate(self.avatar):
                self.image1 = QPixmap(i)
                self.image2 = QLabel(self)
                self.image2.move(x, y)
                self.image2.resize(200, 200)
                scaled = self.image1.scaled(
                    200, 200,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image2.setPixmap(scaled)
                self.image2.setStyleSheet("""
                    border: 2px solid #334155;
                    border-radius: 12px;
                    background-color: #1e293b;
                    padding: 4px;
                """)
                self.image2.show()
                self.avatar_ch.append(self.image2)

                self.rad = QRadioButton(self)
                self.rad.move(x1, y1)
                self.rad.setCursor(Qt.CursorShape.PointingHandCursor)
                self.rad.show()
                self.box_ch.append(self.rad)

                x += 220
                x1 += 220

            self.choice_btn = QPushButton("Выбрать", self)
            self.choice_btn.move(350, 350)
            self.choice_btn.resize(200, 40)
            self.choice_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.choice_btn.show()
            self.choice_btn.clicked.connect(self.ava)

    def ava(self):
        if self.ischeck() is not False:
            if self.name.strip() == '':
                self.name = "User" + str(len(self.users) + 1)
            if self.surname.strip() == '':
                self.surname = ""
            self.avatar_choice = self.avatar[self.ischeck()]
            self.hide()
            self.flag = True
            cur = self.con.cursor()
            lst = json.dumps([])
            cur.execute("""INSERT INTO profile(login, password, name, surname, age, country, avatar, level, ex, money, pic)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (self.login, self.password, self.name, self.surname, int(self.age), self.country, self.avatar_choice, 1, 0, 0,
                         lst))
            self.con.commit()


            self.lob = Lobby(self.flag, self.login)
            self.lob.show()

    def ischeck(self):
        for i, j in enumerate(self.box_ch):
            if j.isChecked():
                return i
        return False


class Lobby(QWidget):
    def __init__(self, flag, login=''):
        self.login = login
        self.flag = flag
        self.prof = []
        self.pic_lst = []
        super().__init__()
        self.con = sqlite3.connect("proect.db")
        self.cur = self.con.cursor()
        res = self.cur.execute("""select * from profile where login = ?""", (self.login,)).fetchone()
        self.login, self.password, self.name, self.surname, self.age, self.country, self.avatar, self.level0, self.ex, self.money, self.pic = res
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Lobby')
        self.setFixedSize(1540, 900)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0f172a,
                    stop:0.5 #1e3c72,
                    stop:1 #2a5298
                );
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(30)

        self.title = QLabel("Поздравляем!")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            color: #ffffff;
            font-size: 96px;
            font-weight: bold;
            background: transparent;
            letter-spacing: 2px;
        """)
        main_layout.addWidget(self.title)
        if self.flag:
            self.subtitle = QLabel("Аккаунт успешно создан!")
            self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.subtitle.setStyleSheet("""
                color: #d0e4ff;
                font-size: 42px;
                background: transparent;
            """)
            main_layout.addWidget(self.subtitle)

            main_layout.addSpacing(50)
        else:
            self.subtitle = QLabel("Вы успешно вошли в аккаунт!")
            self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.subtitle.setStyleSheet("""
                color: #d0e4ff;
                font-size: 42px;
                background: transparent;
            """)
            main_layout.addWidget(self.subtitle)

            main_layout.addSpacing(50)

        self.continue_btn = QPushButton("Продолжить")
        self.continue_btn.setFixedSize(360, 80)
        self.continue_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.continue_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffd166;
                color: #1e3c72;
                font-size: 26px;
                font-weight: bold;
                border: none;
                border-radius: 40px;
            }
            QPushButton:hover   { background-color: #ffe08a; }
            QPushButton:pressed { background-color: #e6b94a; }
        """)
        self.continue_btn.clicked.connect(self.on_continue)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout.addWidget(self.continue_btn)
        main_layout.addLayout(btn_layout)
        if self.flag is None:
            self.on_continue()

    def on_continue(self):
        self.continue_btn.hide()
        self.title.hide()
        self.subtitle.hide()

        try:
            self.btn_profile = QPushButton("Профиль", self)
            self.btn_profile.setFixedSize(292, 80)
            self.btn_profile.move(1248, 820)
            self.btn_profile.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_profile.show()
            self.btn_profile.setStyleSheet("""
                QPushButton {
                    background-color: #ffd166;
                    color: #1e3c72;
                    font-size: 26px;
                    font-weight: bold;
                    border: none;
                    border-radius: 40px;
                }
                QPushButton:hover   { background-color: #ffe08a; }
                QPushButton:pressed { background-color: #e6b94a; }
            """)
            self.btn_profile.clicked.connect(self.profile_fon)

            self.image1 = QPixmap(str(self.avatar))
            self.image2 = QLabel(self)
            self.image2.move(1168, 820)
            self.image2.resize(80, 80)
            scaled = self.image1.scaled(
                80, 80,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image2.setPixmap(scaled)
            self.image2.setStyleSheet("""
                border: 2px solid #334155;
                border-radius: 12px;
                background-color: #1e293b;
                padding: 4px;
            """)
            self.image2.show()

            self.btn_shop = QPushButton("Магазин", self)
            self.btn_shop.setFixedSize(282, 80)
            self.btn_shop.move(876, 820)
            self.btn_shop.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_shop.show()
            self.btn_shop.setStyleSheet("""
                QPushButton {
                    background-color: #ffd166;
                    color: #1e3c72;
                    font-size: 26px;
                    font-weight: bold;
                    border: none;
                    border-radius: 40px;
                }
                QPushButton:hover   { background-color: #ffe08a; }
                QPushButton:pressed { background-color: #e6b94a; }
            """)
            self.btn_shop.clicked.connect(self.shop_fon)

            self.exit_btn = QPushButton("ВЫЙТИ", self)
            self.exit_btn.setFixedSize(282, 80)
            self.exit_btn.move(584, 820)
            self.exit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.exit_btn.show()
            self.exit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffd166;
                    color: #1e3c72;
                    font-size: 26px;
                    font-weight: bold;
                    border: none;
                    border-radius: 40px;
                }
                QPushButton:hover   { background-color: #ffe08a; }
                QPushButton:pressed { background-color: #e6b94a; }
            """)
            self.exit_btn.clicked.connect(self.exit)

            self.cheat_btn = QPushButton("Чит-код", self)
            self.cheat_btn.setFixedSize(282, 80)
            self.cheat_btn.move(292, 820)
            self.cheat_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.cheat_btn.show()
            self.cheat_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffd166;
                    color: #1e3c72;
                    font-size: 26px;
                    font-weight: bold;
                    border: none;
                    border-radius: 40px;
                }
                QPushButton:hover   { background-color: #ffe08a; }
                QPushButton:pressed { background-color: #e6b94a; }
            """)
            self.cheat_btn.clicked.connect(self.cheat)

            self.bonus_btn = QPushButton("Казино", self)
            self.bonus_btn.setFixedSize(282, 80)
            self.bonus_btn.move(0, 820)
            self.bonus_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.bonus_btn.show()
            self.bonus_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffd166;
                    color: #1e3c72;
                    font-size: 26px;
                    font-weight: bold;
                    border: none;
                    border-radius: 40px;
                }
                QPushButton:hover   { background-color: #ffe08a; }
                QPushButton:pressed { background-color: #e6b94a; }
            """)
            self.bonus_btn.clicked.connect(self.casino)

            x = 0
            y = 220
            y1 = 10
            self.btn_levels = []
            self.kek_pic = []
            self.pic1 = ["icon.png", "quiz.jpg", "reaction.jpg", "human.jpg", "clicker.jpg", "snake.jpg"]

            for i in range(10):
                if i < 6:
                    self.icon = QPixmap(self.pic1[i])
                    self.icon6 = QLabel(self)
                    self.icon6.move(x, y1)
                    self.icon6.resize(270, 200)
                    scaled = self.icon.scaled(
                        282, 200,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    self.icon6.setPixmap(scaled)
                    self.icon6.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.icon6.setStyleSheet("""
                        border: 2px solid #334155;
                        border-radius: 8px;
                        background-color: #1e293b;
                        padding: 4px;
                    """)
                    self.icon6.show()
                    self.kek_pic.append(self.icon6)

                self.btn_level = QPushButton(f"Уровень: {i + 1}", self)
                self.btn_level.setFixedSize(282, 80)
                self.btn_level.move(x, y)
                self.btn_level.setCursor(Qt.CursorShape.PointingHandCursor)
                self.btn_level.show()

                if self.level0 >= i + 1:
                    self.btn_level.setStyleSheet("""
                        QPushButton {
                            background-color: #16a34a;
                            color: #1e3c72;
                            font-size: 26px;
                            font-weight: bold;
                            border: none;
                            border-radius: 40px;
                        }
                        QPushButton:hover   { background-color: #16a34a; }
                        QPushButton:pressed { background-color: #16a34a; }
                    """)
                else:
                    self.btn_level.setStyleSheet("""
                        QPushButton {
                            background-color: #dc2626;
                            color: #1e3c72;
                            font-size: 26px;
                            font-weight: bold;
                            border: none;
                            border-radius: 40px;
                        }
                        QPushButton:hover   { background-color: #dc2626; }
                        QPushButton:pressed { background-color: #dc2626; }
                    """)
                self.btn_level.clicked.connect(self.level)

                x += 292
                if i == 4:
                    y = 520
                    x = 0
                    y1 = 310

                self.btn_levels.append(self.btn_level)
        except Exception as e:
            print(e)

    def casino(self):
        self.btn_profile.hide()
        self.btn_shop.hide()
        for i in self.kek_pic:
            i.hide()
        self.image2.hide()
        self.cheat_btn.hide()
        self.exit_btn.hide()
        self.bonus_btn.hide()
        casino = Casino(self.login)
        self.close()
        casino.show()

    def level(self):
        n = int(self.sender().text().split()[1])
        if self.level0 >= n and n == 1:
            self.btn_profile.hide()
            self.btn_shop.hide()
            for i in self.kek_pic:
                i.hide()
            self.image2.hide()
            self.cheat_btn.hide()
            self.exit_btn.hide()
            self.bonus_btn.hide()

            def friend():
                level1 = TicTacToe_friend(self.login)
                self.close()
                level1.show()

            def bot():
                level1 = TicTacToe_bot(self.login)
                self.close()
                level1.show()

            def info():
                QMessageBox.information(self, "Информация",
                                        "1 - Выиграв игру с ботом вы можете перейти на следующий уровень.\n"
                                        "2 - Выиграв игру с ботом вы получаете 25 ฿.\n"
                                        "3 - За игру с другом вы ничего не получаете.\n"
                                        "Удачной игры!")

            def back():
                self.friend_btn.hide()
                self.info_btn.hide()
                self.back_btn.hide()
                self.bot_btn.hide()
                self.icon1.hide()
                self.zero.hide()
                self.on_continue()

            self.friend_btn = QPushButton("Игра против друга!", self)
            self.friend_btn.setFixedSize(600, 200)
            self.friend_btn.move(100, 200)
            self.friend_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.friend_btn.show()
            self.friend_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffd166;
                    color: #1e3c72;
                    font-size: 26px;
                    font-weight: bold;
                    border: none;
                    border-radius: 40px;
                }
                QPushButton:hover   { background-color: #ffe08a; }
                QPushButton:pressed { background-color: #e6b94a; }
            """)
            self.friend_btn.clicked.connect(friend)

            self.zero = QLabel(f"Выбери игру:", self)
            self.zero.resize(250, 50)
            self.zero.move(600, 60)
            self.zero.setStyleSheet("color: #fbbf24; font-size: 40px;")
            self.zero.show()

            self.info_btn = QPushButton("Информация!", self)
            self.info_btn.setFixedSize(250, 80)
            self.info_btn.move(0, 820)
            self.info_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.info_btn.show()
            self.info_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffd166;
                    color: #1e3c72;
                    font-size: 26px;
                    font-weight: bold;
                    border: none;
                    border-radius: 40px;
                }
                QPushButton:hover   { background-color: #ffe08a; }
                QPushButton:pressed { background-color: #e6b94a; }
            """)
            self.info_btn.clicked.connect(info)

            self.back_btn = QPushButton("Назад", self)
            self.back_btn.setFixedSize(200, 80)
            self.back_btn.move(1340, 820)
            self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.back_btn.show()
            self.back_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc2626;
                    color: #1e3c72;
                    font-size: 26px;
                    font-weight: bold;
                    border: none;
                    border-radius: 40px;
                }
                QPushButton:hover   { background-color: #dc2626; }
                QPushButton:pressed { background-color: #dc2626; }
            """)
            self.back_btn.clicked.connect(back)

            self.icon = QPixmap("icon.png")
            self.icon1 = QLabel(self)
            self.icon1.move(550, 450)
            self.icon1.resize(400, 400)
            scaled = self.icon.scaled(
                400, 400,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.icon1.setPixmap(scaled)
            self.icon1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.icon1.setStyleSheet("""
                border: 2px solid #334155;
                border-radius: 8px;
                background-color: #1e293b;
                padding: 4px;
            """)
            self.icon1.show()

            self.bot_btn = QPushButton("Игра против бота!", self)
            self.bot_btn.setFixedSize(600, 200)
            self.bot_btn.move(750, 200)
            self.bot_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.bot_btn.show()
            self.bot_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffd166;
                    color: #1e3c72;
                    font-size: 26px;
                    font-weight: bold;
                    border: none;
                    border-radius: 40px;
                }
                QPushButton:hover   { background-color: #ffe08a; }
                QPushButton:pressed { background-color: #e6b94a; }
            """)
            self.bot_btn.clicked.connect(bot)
            for i in self.btn_levels:
                i.hide()

        elif self.level0 >= n and (n == 2 or n == 3 or n == 4 or n == 5 or n == 6):
            self.btn_profile.hide()
            self.btn_shop.hide()
            for i in self.kek_pic:
                i.hide()
            self.image2.hide()
            self.cheat_btn.hide()
            self.exit_btn.hide()
            self.bonus_btn.hide()

            def start():
                if n == 2:
                    self.level2 = History(self.login)
                    self.hide()
                    self.level2.show()
                if n == 3:
                    self.level3 = Reaction(self.login)
                    self.hide()
                    self.level3.show()
                if n == 4:
                    self.level4 = HangmanGame(self.login)
                    self.hide()
                    self.level4.show()
                if n == 5:
                    self.level5 = ClickerUI(self.login)
                    self.hide()
                    self.level5.show()
                if n == 6:
                    self.level6 = SnakeGame(self.login)
                    self.hide()
                    self.level6.show()

            def info():
                QMessageBox.information(self, "Информация",
                                        "1 - Ответив на все вопросы правильно вы можете перейти на следующий уровень.\n"
                                        "2 - Ответив на все вопросы правильно вы получаете 30 ฿.\n"
                                        "3 - Ответив не правильно вы ничего не получите.\n"
                                        "Хорошо провести время!")

            def back():
                self.info_btn2.hide()
                self.back_btn2.hide()
                self.start_btn2.hide()
                self.icon12.hide()
                self.on_continue()

            self.info_btn2 = QPushButton("Информация!", self)
            self.info_btn2.setFixedSize(250, 80)
            self.info_btn2.move(0, 820)
            self.info_btn2.setCursor(Qt.CursorShape.PointingHandCursor)
            self.info_btn2.show()
            self.info_btn2.setStyleSheet("""
                QPushButton {
                    background-color: #ffd166;
                    color: #1e3c72;
                    font-size: 26px;
                    font-weight: bold;
                    border: none;
                    border-radius: 40px;
                }
                QPushButton:hover   { background-color: #ffe08a; }
                QPushButton:pressed { background-color: #e6b94a; }
            """)
            self.info_btn2.clicked.connect(info)

            self.back_btn2 = QPushButton("Назад", self)
            self.back_btn2.setFixedSize(200, 80)
            self.back_btn2.move(1340, 820)
            self.back_btn2.setCursor(Qt.CursorShape.PointingHandCursor)
            self.back_btn2.show()
            self.back_btn2.setStyleSheet("""
                QPushButton {
                    background-color: #dc2626;
                    color: #1e3c72;
                    font-size: 26px;
                    font-weight: bold;
                    border: none;
                    border-radius: 40px;
                }
                QPushButton:hover   { background-color: #dc2626; }
                QPushButton:pressed { background-color: #dc2626; }
            """)
            self.back_btn2.clicked.connect(back)
            if n == 2:
                self.icon2 = QPixmap("quiz.jpg")
                self.icon12 = QLabel(self)
                self.icon12.move(550, 450)
                self.icon12.resize(400, 400)
                scaled = self.icon2.scaled(
                    400, 400,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.icon12.setPixmap(scaled)
                self.icon12.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.icon12.setStyleSheet("""
                    border: 2px solid #334155;
                    border-radius: 8px;
                    background-color: #1e293b;
                    padding: 4px;
                """)
                self.icon12.show()
            elif n == 3:
                self.icon2 = QPixmap("reaction.jpg")
                self.icon12 = QLabel(self)
                self.icon12.move(550, 450)
                self.icon12.resize(400, 400)
                scaled = self.icon2.scaled(
                    400, 400,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.icon12.setPixmap(scaled)
                self.icon12.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.icon12.setStyleSheet("""
                                border: 2px solid #334155;
                                border-radius: 8px;
                                background-color: #1e293b;
                                padding: 4px;
                            """)
                self.icon12.show()
            elif n == 4:
                self.icon2 = QPixmap("human.jpg")
                self.icon12 = QLabel(self)
                self.icon12.move(550, 450)
                self.icon12.resize(400, 400)
                scaled = self.icon2.scaled(
                    400, 400,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.icon12.setPixmap(scaled)
                self.icon12.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.icon12.setStyleSheet("""
                                border: 2px solid #334155;
                                border-radius: 8px;
                                background-color: #1e293b;
                                padding: 4px;
                            """)
                self.icon12.show()
            elif n == 5:
                self.icon2 = QPixmap("clicker.jpg")
                self.icon12 = QLabel(self)
                self.icon12.move(550, 450)
                self.icon12.resize(400, 400)
                scaled = self.icon2.scaled(
                    400, 400,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.icon12.setPixmap(scaled)
                self.icon12.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.icon12.setStyleSheet("""
                                border: 2px solid #334155;
                                border-radius: 8px;
                                background-color: #1e293b;
                                padding: 4px;
                            """)
                self.icon12.show()
            elif n == 6:
                self.icon2 = QPixmap("snake.jpg")
                self.icon12 = QLabel(self)
                self.icon12.move(550, 450)
                self.icon12.resize(400, 400)
                scaled = self.icon2.scaled(
                    400, 400,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.icon12.setPixmap(scaled)
                self.icon12.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.icon12.setStyleSheet("""
                                border: 2px solid #334155;
                                border-radius: 8px;
                                background-color: #1e293b;
                                padding: 4px;
                            """)
                self.icon12.show()


            self.start_btn2 = QPushButton("НАЧАТЬ", self)
            self.start_btn2.setFixedSize(600, 200)
            self.start_btn2.move(450, 200)
            self.start_btn2.setCursor(Qt.CursorShape.PointingHandCursor)
            self.start_btn2.show()
            self.start_btn2.setStyleSheet("""
                QPushButton {
                    background-color: #ffd166;
                    color: #1e3c72;
                    font-size: 26px;
                    font-weight: bold;
                    border: none;
                    border-radius: 40px;
                }
                QPushButton:hover   { background-color: #ffe08a; }
                QPushButton:pressed { background-color: #e6b94a; }
            """)
            self.start_btn2.clicked.connect(start)
            for i in self.btn_levels:
                i.hide()
        else:
            self.bonus()

    def bonus(self):
        self.image5 = QPixmap("gorila.jpg")
        self.image4 = QLabel(self)
        self.image4.move(400, 100)
        self.image4.resize(900, 900)
        scaled = self.image5.scaled(
            900, 900,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image4.setPixmap(scaled)
        self.image4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image4.setStyleSheet("""
            border: 2px solid #334155;
            border-radius: 8px;
            background-color: #1e293b;
            padding: 4px;
        """)
        self.image4.show()
        QTimer.singleShot(2000, self.image4.hide)

    def cheat(self):
        answer = QMessageBox.question(
            self,
            'Подтверждение',
            'Вы уверены, что хотите использовать чит-код?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.money += 9999999999
            self.cur.execute('''Update profile set money = ? where login = ?''', (self.money, self.login))
            self.con.commit()

    def exit(self):
        self.close()

    def shop_fon(self):
        self.btn_profile.hide()
        self.btn_shop.hide()
        self.image2.hide()
        for i in self.kek_pic:
            i.hide()
        self.cheat_btn.hide()
        self.exit_btn.hide()
        self.bonus_btn.hide()
        for i in self.btn_levels:
            i.hide()
        self.setStyleSheet("""
            QWidget {
                background-color: #14532d;
            }
        """)

        self.shop_label = QLabel("Магазин наклеек на профиль", self)
        self.shop_label.move(600, 0)
        self.shop_label.resize(1000, 300)
        self.shop_label.setStyleSheet("""
            color: #ffffff;
            font-size: 42px;
            background: transparent;
        """)
        self.shop_label.show()
        self.prof.append(self.shop_label)

        self.balance_label = QLabel(f"Ваш баланс: {self.money} ฿", self)
        self.balance_label.move(10, 10)
        self.balance_label.resize(1000, 300)
        self.balance_label.setStyleSheet("""
            color: #ffffff;
            font-size: 42px;
            background: transparent;
        """)
        self.balance_label.show()
        self.prof.append(self.balance_label)

        self.btn_lobby = QPushButton("Lobby", self)
        self.btn_lobby.setFixedSize(292, 80)
        self.btn_lobby.move(1248, 820)
        self.btn_lobby.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_lobby.show()
        self.btn_lobby.setStyleSheet("""
                    QPushButton {
                        background-color: #ffd166;
                        color: #1e3c72;
                        font-size: 26px;
                        font-weight: bold;
                        border: none;
                        border-radius: 40px;
                    }
                    QPushButton:hover   { background-color: #ffe08a; }
                    QPushButton:pressed { background-color: #e6b94a; }
                """)
        self.btn_lobby.clicked.connect(self.loddy_fon)
        self.prof.append(self.btn_lobby)
        self.pic_lst = []
        for i in range(1, 11):
            self.pic_lst.append("pic" + str(i))

        x = 30
        y = 250

        y1 = 460
        self.price_pic = [45, 65, 90, 10, 80, 20, 100, 15, 50, 40]
        for i, j in enumerate(self.pic_lst):
            self.image1 = QPixmap(j)
            self.image3 = QLabel(self)
            self.image3.move(x, y)
            self.image3.resize(200, 200)
            scaled = self.image1.scaled(
                200, 200,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image3.setPixmap(scaled)
            self.image3.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.image3.setStyleSheet("""
                border: 2px solid #334155;
                border-radius: 8px;
                background-color: #1e293b;
                padding: 4px;
            """)
            self.image3.show()
            self.prof.append(self.image3)

            self.btn_price = QPushButton(f"{self.price_pic[i]} ฿", self)
            self.btn_price.move(x, y1)
            self.btn_price.setFixedSize(200, 80)
            self.btn_price.setStyleSheet("""
                QPushButton {
                    background-color: #64748b;
                    color: #ffffff;
                    font-size: 26px;
                    font-weight: bold;
                    border: none;
                    border-radius: 40px;
                }
                QPushButton:hover   { background-color: #94a3b8; }
                QPushButton:pressed { background-color: #475569; }
            """)
            self.btn_price.show()
            self.btn_price.clicked.connect(self.buy)
            self.prof.append(self.btn_price)

            x += 250
            if i == 4:
                x = 30
                y = 550
                y1 = 760

    def buy(self):
        n = int(self.sender().text().split()[0])
        if self.money >= n:
            if self.pic_lst[self.price_pic.index(n)] not in self.pic:
                QMessageBox.information(self, 'Покупка', 'Успешная покупка!')
                self.money -= n
                self.balance_label.setText(f"Ваш баланс: {self.money} ฿")
                n1 = json.loads(self.pic)
                n1.append(self.pic_lst[self.price_pic.index(n)])
                self.pic = json.dumps(n1)
                self.cur.execute('UPDATE profile SET pic=?, money=? WHERE login=?', (self.pic, self.money, self.login))
                self.con.commit()
            else:
                QMessageBox.warning(self, 'Предупреждение', 'У вас уже есть эта наклейка')
        else:
            QMessageBox.warning(self, 'Предупреждение', 'Недостаточно средств!')

    def profile_fon(self):
        self.btn_shop.hide()
        self.cheat_btn.hide()
        self.exit_btn.hide()
        self.bonus_btn.hide()
        for i in self.kek_pic:
            i.hide()
        for i in self.btn_levels:
            i.hide()
        self.image2.move(660, 50)
        self.image2.resize(200, 200)
        scaled = self.image1.scaled(
            200, 200,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image2.setPixmap(scaled)
        self.image2.setStyleSheet("""
            border: 2px solid #334155;
            border-radius: 12px;
            background-color: #1e293b;
            padding: 4px;
        """)
        self.prof.append(self.image2)
        self.name_label = QLabel(self)
        self.name_label.move(650, 250)
        self.name_label.setText(f"Имя: {self.surname + ' ' + self.name}")
        self.name_label.resize(1000, 60)
        self.name_label.setStyleSheet("""
            color: #d0e4ff;
            font-size: 42px;
            background: transparent;
        """)
        self.name_label.show()
        self.prof.append(self.name_label)

        self.age_label = QLabel(self)
        self.age_label.move(650, 320)
        self.age_label.setText(f"Лет: {self.age}")
        self.age_label.resize(1000, 60)
        self.age_label.setStyleSheet("""
            color: #d0e4ff;
            font-size: 42px;
            background: transparent;
        """)
        self.age_label.show()
        self.prof.append(self.age_label)

        self.life_label = QLabel(self)
        self.life_label.move(650, 390)
        self.life_label.setText(f"Страна: {self.country}")
        self.life_label.resize(1000, 60)
        self.life_label.setStyleSheet("""
            color: #d0e4ff;
            font-size: 42px;
            background: transparent;
        """)
        self.life_label.show()
        self.prof.append(self.life_label)

        self.level_label = QLabel(self)
        self.level_label.move(650, 460)
        self.level_label.setText(f"Уровень: {self.level0}")
        self.level_label.resize(1000, 60)
        self.level_label.setStyleSheet("""
            color: #d0e4ff;
            font-size: 42px;
            background: transparent;
        """)
        self.level_label.show()
        self.prof.append(self.level_label)

        self.ex_label = QLabel(self)
        self.ex_label.move(650, 530)
        self.ex_label.setText(f"Опыт: {self.ex}")
        self.ex_label.resize(1000, 60)
        self.ex_label.setStyleSheet("""
            color: #d0e4ff;
            font-size: 42px;
            background: transparent;
        """)
        self.ex_label.show()
        self.prof.append(self.ex_label)

        self.login_label = QLabel(self)
        self.login_label.move(650, 600)
        self.login_label.setText(f"Логин: {self.login}")
        self.login_label.resize(1000, 60)
        self.login_label.setStyleSheet("""
            color: #d0e4ff;
            font-size: 42px;
            background: transparent;
        """)
        self.login_label.show()
        self.prof.append(self.login_label)

        self.password_label = QLabel(self)
        self.password_label.move(650, 670)
        self.password_label.setText(f"Пароль: {self.password}")
        self.password_label.resize(1000, 60)
        self.password_label.setStyleSheet("""
            color: #d0e4ff;
            font-size: 42px;
            background: transparent;
        """)
        self.password_label.show()
        self.prof.append(self.password_label)

        self.money_label = QLabel(self)
        self.money_label.move(650, 740)
        self.money_label.setText(f"Монет: {self.money} ฿")
        self.money_label.resize(1000, 60)
        self.money_label.setStyleSheet("""
            color: #d0e4ff;
            font-size: 42px;
            background: transparent;
        """)
        self.money_label.show()
        self.prof.append(self.money_label)
        x = 50
        y = 50
        n = json.loads(self.pic)
        for i, j in enumerate(n):
            self.im = QPixmap(j)
            self.im2 = QLabel(self)
            self.im2.move(x, y)
            self.im2.resize(150, 150)
            scaled = self.im.scaled(
                150, 150,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.im2.setPixmap(scaled)
            self.im2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.im2.setStyleSheet("""
                border: 2px solid #334155;
                border-radius: 8px;
                background-color: #1e293b;
                padding: 4px;
            """)
            self.im2.show()
            self.prof.append(self.im2)
            x += 200
            if (i + 1) % 3 == 0:
                x = 50
                y += 200

        self.btn_change = QPushButton("Поменять пароль", self)
        self.btn_change.move(650, 820)
        self.btn_change.setFixedSize(400, 80)
        self.btn_change.setStyleSheet("""
            QPushButton {
                background-color: #ffd166;
                color: #1e3c72;
                font-size: 26px;
                font-weight: bold;
                border: none;
                border-radius: 40px;
            }
            QPushButton:hover   { background-color: #ffe08a; }
            QPushButton:pressed { background-color: #e6b94a; }
        """)
        self.btn_change.show()
        self.btn_change.clicked.connect(self.changeevent)
        self.prof.append(self.btn_change)

        self.btn_profile.hide()

        self.btn_lobby = QPushButton("Lobby", self)
        self.btn_lobby.setFixedSize(292, 80)
        self.btn_lobby.move(1248, 820)
        self.btn_lobby.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_lobby.show()
        self.btn_lobby.setStyleSheet("""
            QPushButton {
                background-color: #ffd166;
                color: #1e3c72;
                font-size: 26px;
                font-weight: bold;
                border: none;
                border-radius: 40px;
            }
            QPushButton:hover   { background-color: #ffe08a; }
            QPushButton:pressed { background-color: #e6b94a; }
        """)
        self.btn_lobby.clicked.connect(self.loddy_fon)
        self.prof.append(self.btn_lobby)

    def loddy_fon(self):
        for i in self.prof:
            i.hide()
        self.prof = []
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0f172a,
                    stop:0.5 #1e3c72,
                    stop:1 #2a5298
                );
            }
        """)
        self.on_continue()

    def changeevent(self):
        password_new, ok_pressed_password = QInputDialog.getText(
            self, 'Знакомство', 'Введите новый пароль.')
        if not ok_pressed_password or password_new == "":
            return
        self.password = password_new
        self.password_label.setText(f"Пароль: {self.password}")
        self.cur.execute("UPDATE profile SET password=? WHERE login=?", (self.password, self.login))
        self.con.commit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.flag = False
        self.box = []
        self.img = random.sample(
            ["bike1.png", "bike2.png", "bike3.jpg",
             "car1.png", "car2.jpg", "car3.png",
             "kat1.jpg", "kat2.png", "kat3.png"], k=9)
        self.count = 3
        self.one = False
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Вход')
        self.setFixedSize(400, 400)

        self.entry_bt = QPushButton("Войти", self)
        self.entry_bt.move(100, 280)
        self.entry_bt.resize(200, 40)
        self.entry_bt.setCursor(Qt.CursorShape.PointingHandCursor)
        self.entry_bt.clicked.connect(self.entry)
        self.box.append(self.entry_bt)

        self.register_bt = QPushButton("Зарегистрироваться", self)
        self.register_bt.move(100, 330)
        self.register_bt.resize(200, 40)
        self.register_bt.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_bt.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #38bdf8;
                border: 2px solid #38bdf8;
                border-radius: 10px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover   { background-color: #1e3c72; }
            QPushButton:pressed { background-color: #0f172a; }
        """)
        self.register_bt.clicked.connect(self.sec)
        self.box.append(self.register_bt)

        self.password_label = QLabel("Пароль", self)
        self.password_label.resize(200, 40)
        self.password_label.move(100, 200)
        self.password_label.setStyleSheet("color: #cbd5e1; font-size: 14px;")
        self.box.append(self.password_label)

        self.password1 = QLineEdit(self)
        self.password1.move(100, 230)
        self.password1.resize(200, 40)
        self.password1.setPlaceholderText("Введите пароль")
        self.password1.setEchoMode(QLineEdit.EchoMode.Password)
        self.box.append(self.password1)

        self.login_label = QLabel("Логин", self)
        self.login_label.resize(200, 40)
        self.login_label.move(100, 140)
        self.login_label.setStyleSheet("color: #cbd5e1; font-size: 14px;")
        self.box.append(self.login_label)

        self.login1 = QLineEdit(self)
        self.login1.move(100, 170)
        self.login1.resize(200, 40)
        self.login1.setPlaceholderText("Введите логин")
        self.box.append(self.login1)

        self.pixmap_lock = QPixmap('lock.jpg')
        self.image_lock = QLabel(self)
        self.image_lock.move(150, 30)
        self.image_lock.resize(100, 100)
        scaled = self.pixmap_lock.scaled(
            100, 100,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_lock.setPixmap(scaled)
        self.box.append(self.image_lock)

        self.error_label = QLabel("Не верный логин или пароль!", self)
        self.error_label.resize(300, 40)
        self.error_label.move(150, 140)
        self.error_label.setStyleSheet(
            "color: #f87171; font-size: 13px; font-weight: bold;"
        )
        self.error_label.hide()

    def entry(self):
        self.con = sqlite3.connect("proect.db")
        self.cur = self.con.cursor()
        res = self.cur.execute("""select * from profile where login = ?""", (self.login1.text(),)).fetchone()
        if res:
            self.login, self.password, self.name, self.surname, self.age, self.country, self.avatar, self.level0, self.ex, self.money, self.pic = res
            if self.password1.text() == self.password:
                for i in self.box:
                    i.hide()
                self.error_label.hide()
                self.check_on_robot()
                return
        self.error_label.show()

    def sec(self):
        self.hide()
        self.second_window = SecondWindow()

    def check_on_robot(self):
        self.check = QLabel("ПРОЙДИТЕ КАПЧУ!!!", self)
        self.check.resize(300, 40)
        self.check.move(150, 0)
        self.check.setStyleSheet(
            "color: #f87171; font-weight: bold; font-size: 16px;"
        )
        self.check.show()

        self.bike = QLabel("Найдите все велосипеды!!!", self)
        self.bike.resize(200, 40)
        self.bike.move(50, 20)
        self.bike.setStyleSheet("color: #cbd5e1; font-size: 13px;")
        self.bike.show()

        self.check_count = QLabel(f"Попыток осталось - {self.count}", self)
        self.check_count.resize(200, 40)
        self.check_count.move(250, 20)
        self.check_count.setStyleSheet("color: #fbbf24; font-size: 13px;")
        self.check_count.show()

        self.check_btn = QPushButton(f"Проверить", self)
        self.check_btn.resize(200, 40)
        self.check_btn.move(80, 350)
        self.check_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.check_btn.show()
        self.check_btn.clicked.connect(self.true_false)

        x = 50
        y = 50
        x1 = 80
        y1 = 120
        self.checkbox = []
        self.img_error = []

        for j, i in enumerate(self.img):
            self.image1 = QPixmap(i)
            self.image2 = QLabel(self)
            self.image2.move(x, y)
            self.image2.resize(80, 80)
            scaled = self.image1.scaled(
                80, 80,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image2.setPixmap(scaled)
            self.image2.setStyleSheet("""
                border: 2px solid #334155;
                border-radius: 8px;
                background-color: #1e293b;
                padding: 2px;
            """)
            self.image2.show()
            self.img_error.append(self.image2)

            self.check_box = QCheckBox(self)
            self.check_box.move(x1, y1)
            self.check_box.setCursor(Qt.CursorShape.PointingHandCursor)
            self.checkbox.append(self.check_box)
            self.check_box.show()

            x += 100
            x1 += 100
            if (j + 1) % 3 == 0:
                y += 100
                x = 50
                y1 += 100
                x1 = 80

    def true_false(self):
        true_pic = []
        for i, j in enumerate(self.img):
            if "bike1.png" == j or "bike2.png" == j or "bike3.jpg" == j:
                true_pic.append(i)
        checked = 0
        for i, j in enumerate(self.checkbox):
            if j.isChecked() and i in true_pic:
                checked += 1
            elif j.isChecked() and i not in true_pic:
                self.error()
                return
        if checked != 3:
            self.error()
        if checked == 3:
            self.hide()
            self.flag = False
            self.lobby = Lobby(self.flag, self.login)
            self.lobby.show()

    def error(self):
        self.count -= 1
        if self.count != 0:
            for i in self.img_error:
                i.hide()
            for i in self.checkbox:
                i.hide()
            self.check.hide()
            self.bike.hide()
            self.check_count.hide()
            self.check_btn.hide()
            self.img = random.sample(
                ["bike1.png", "bike2.png", "bike3.jpg",
                 "car1.png", "car2.jpg", "car3.png",
                 "kat1.jpg", "kat2.png", "kat3.png"], k=9)
            for i in self.checkbox:
                if i.isChecked():
                    i.setChecked(False)
            self.check_on_robot()
        else:
            for i in self.img_error:
                i.hide()
            for i in self.checkbox:
                i.hide()
            self.check.hide()
            self.bike.hide()
            self.check_count.hide()
            self.check_btn.hide()

            error_all = []
            for i in range(9):
                if i < 4:
                    name = "error1.jpg"
                elif 4 <= i < 8:
                    name = "error2.png"
                else:
                    name = "robot.png"

                self.pixmap_lock = QPixmap(name)
                self.image_lock = QLabel(self)
                self.image_lock.resize(100, 100)
                scaled = self.pixmap_lock.scaled(
                    100, 100,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_lock.setPixmap(scaled)
                error_all.append(self.image_lock)

            self.robot_true = QLabel("ТЫ РОБОТ!!!", self)
            self.robot_true.resize(200, 40)
            self.robot_true.move(170, 150)
            self.robot_true.setStyleSheet(
                "color: #f87171; font-weight: bold; font-size: 22px;"
            )
            self.robot_true.show()

            error_all[0].move(10, 10)
            error_all[1].move(300, 10)
            error_all[2].move(10, 300)
            error_all[3].move(300, 300)
            error_all[4].move(150, 10)
            error_all[5].move(10, 150)
            error_all[6].move(300, 150)
            error_all[7].move(150, 300)
            error_all[8].move(150, 200)

            for i in error_all:
                i.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
