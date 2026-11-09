import json
import sys
import sqlite3

import datetime as dt
from PyQt6.QtCore import Qt, QUrl, QTimer

from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtMultimedia import (QSoundEffect, QAudioOutput, QMediaPlayer)
from PyQt6.QtWidgets import (QApplication, QWidget, QRadioButton,
                             QPushButton, QLabel, QLineEdit,
                             QCheckBox, QMainWindow,
                             QInputDialog, QHBoxLayout, QVBoxLayout, QMessageBox, QTableWidgetItem, QHeaderView,
                             QTableWidget, QFrame, QGridLayout, QSpinBox, QComboBox, QFileDialog, QButtonGroup,
                             QGraphicsDropShadowEffect)
from krestic_nolik_solo import TicTacToe_friend
from krestic_nolik_bot import TicTacToe_bot
from viktorina import History
from Clicker import ClickerUI
from words import HangmanGame
from reaction import Reaction
from snake import SnakeGame
from casino import Casino
from tetris import TetrisGame
from paint import Paint
from math_test import Math
from flappy_bird import FlappyBird
from horror import Horror
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


class Fake(QWidget):
    def __init__(self, login):
        super().__init__()
        self.login = login
        self.con = sqlite3.connect("proect.db")
        self.cur = self.con.cursor()
        s = json.dumps([])

        self.cur.execute("UPDATE profile SET money=0, ex=0, level=1, record_snake=0, record_tetris=0, casino=0, paint=0, horror=0, pic=? WHERE login=?", (s, self.login))
        self.con.commit()
        self.con.close()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Халявы нет')
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #0f172a; color: #e2e8f0;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        self.label = QLabel("НИКАКОЙ ХАЛЯВЫ В МОЕМ ПРОЕКТЕ!!!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: #ef4444; font-size: 24px; font-weight: bold;")
        layout.addWidget(self.label)

        self.label_fake = QLabel("ЗА ЭТО Я ОБНУЛЮ ВЕСЬ ТВОЙ АККАУНТ!!!")
        self.label_fake.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_fake.setStyleSheet("color: #ef4444; font-size: 24px; font-weight: bold;")
        layout.addWidget(self.label_fake)

        self.btn_ok = QPushButton("Понятно")
        self.btn_ok.setFixedSize(200, 50)
        self.btn_ok.setStyleSheet("""
            QPushButton {
                background-color: #dc2626; color: white;
                border-radius: 10px; font-size: 18px; font-weight: bold;
            }
            QPushButton:hover { background-color: #ef4444; }
        """)
        self.btn_ok.clicked.connect(self.close)
        layout.addWidget(self.btn_ok, alignment=Qt.AlignmentFlag.AlignCenter)


class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.one = False
        self.avatar_choice = ''
        self.con = sqlite3.connect("proect.db")

        self.avatar_group = QButtonGroup(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Регистрация')
        self.setFixedSize(1540, 900)

        self.setStyleSheet("""
               QWidget { background-color: #0f172a; color: #e2e8f0; font-family: 'Segoe UI'; }
               QLabel { font-size: 16px; font-weight: 600; color: #cbd5e1; }
               QLineEdit, QComboBox, QSpinBox {
                   background-color: #1e293b; border: 2px solid #334155;
                   border-radius: 8px; padding: 8px; font-size: 16px; color: #e2e8f0;
               }
               QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border: 2px solid #38bdf8; }
               QPushButton {
                   background-color: #38bdf8; color: #0f172a;
                   border: none; border-radius: 10px; font-size: 18px; font-weight: bold; padding: 12px;
               }
               QPushButton:hover { background-color: #7dd3fc; }
               QPushButton:pressed { background-color: #0ea5e9; }
               QRadioButton::indicator {
                   width: 24px; height: 24px; border-radius: 12px;
                   border: 2px solid #64748b; background: #1e293b;
               }
               QRadioButton::indicator:checked { background: #38bdf8; border: 2px solid #38bdf8; }
           """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(50)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        title = QLabel("Регистрация")
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #ffffff; margin-bottom: 20px;")
        form_layout.addWidget(title)

        form_layout.addWidget(QLabel("Логин"))

        self.login = QLabel("Логин не может быть пустым или занят", self)
        self.login.setStyleSheet("font-size: 12px; color: #ef4444; font-weight: bold; margin-bottom: 2px;")
        self.login.hide()
        form_layout.addWidget(self.login)

        self.edit_login = QLineEdit()
        self.edit_login.setPlaceholderText("Введите логин")
        form_layout.addWidget(self.edit_login)

        form_layout.addWidget(QLabel("Пароль"))

        self.password = QLabel("Обязательное поле", self)
        self.password.setStyleSheet("font-size: 12px; color: #ef4444; font-weight: bold; margin-bottom: 2px;")
        self.password.hide()
        form_layout.addWidget(self.password)

        self.edit_password = QLineEdit()
        self.edit_password.setPlaceholderText("Введите пароль")
        self.edit_password.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.edit_password)

        form_layout.addWidget(QLabel("Имя"))

        self.name = QLabel("Обязательное поле", self)
        self.name.setStyleSheet("font-size: 12px; color: #ef4444; font-weight: bold; margin-bottom: 2px;")
        self.name.hide()
        form_layout.addWidget(self.name)

        self.edit_name = QLineEdit()
        self.edit_name.setPlaceholderText("Введите имя")
        form_layout.addWidget(self.edit_name)

        form_layout.addWidget(QLabel("Фамилия"))

        self.surname = QLabel("Обязательное поле", self)
        self.surname.setStyleSheet("font-size: 12px; color: #ef4444; font-weight: bold; margin-bottom: 2px;")
        self.surname.hide()
        form_layout.addWidget(self.surname)

        self.edit_surname = QLineEdit()
        self.edit_surname.setPlaceholderText("Введите фамилию")
        form_layout.addWidget(self.edit_surname)

        form_layout.addWidget(QLabel("Страна"))
        self.combo_country = QComboBox()
        self.combo_country.addItems([
            "Россия", "Беларусь", "Казахстан", "Украина",
            "Армения", "Грузия", "Узбекистан", "Другая"
        ])
        form_layout.addWidget(self.combo_country)

        form_layout.addWidget(QLabel("Возраст"))
        self.spin_age = QSpinBox()
        self.spin_age.setRange(1, 120)
        self.spin_age.setValue(18)
        self.spin_age.setSuffix(" лет")
        form_layout.addWidget(self.spin_age)

        form_layout.addStretch()

        self.btn_register = QPushButton("Зарегистрироваться")
        self.btn_register.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_register.clicked.connect(self.on_register)
        form_layout.addWidget(self.btn_register)
        main_layout.addLayout(form_layout, stretch=1)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title_av = QLabel("Выберите аватарку:")
        title_av.setStyleSheet("font-size: 28px; font-weight: bold; color: #ffffff; margin-bottom: 20px;")
        right_layout.addWidget(title_av)

        avatar_grid = QGridLayout()
        avatar_grid.setSpacing(20)

        self.avatars_list = ["math.jpg", "rust.jpg", "bmw.jpg", "Lion.jpg"]

        for i, j in enumerate(self.avatars_list):
            row = i // 2
            col = i % 2

            cell_widget = QWidget()
            cell_layout = QVBoxLayout(cell_widget)
            cell_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            pix = QPixmap(j)
            lbl = QLabel()
            lbl.setFixedSize(180, 180)
            lbl.setPixmap(pix.scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio,
                                     Qt.TransformationMode.SmoothTransformation))
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(
                "border: 2px solid #334155; border-radius: 15px; background-color: #1e293b; padding: 5px;")
            cell_layout.addWidget(lbl)

            rad = QRadioButton()
            rad.setCursor(Qt.CursorShape.PointingHandCursor)
            self.avatar_group.addButton(rad, i)
            cell_layout.addWidget(rad, alignment=Qt.AlignmentFlag.AlignCenter)

            avatar_grid.addWidget(cell_widget, row, col)

        right_layout.addLayout(avatar_grid)

        self.upload_layout = QHBoxLayout()
        self.btn_choose = QPushButton("Загрузить свою")
        self.btn_choose.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_choose.setStyleSheet("""
               QPushButton { background-color: #8b5cf6; color: white; border-radius: 10px; font-size: 16px; }
               QPushButton:hover { background-color: #a78bfa; }
           """)
        self.btn_choose.clicked.connect(self.ava)
        self.upload_layout.addWidget(self.btn_choose)

        self.lbl_custom = QLabel()
        self.lbl_custom.setFixedSize(100, 100)
        self.upload_layout.addWidget(self.lbl_custom)

        right_layout.addLayout(self.upload_layout)

        self.avatar_group.button(0).setChecked(True)

        main_layout.addLayout(right_layout, stretch=1)

        self.show()

    def on_register(self):
        self.cur = self.con.cursor()
        all1 = self.cur.execute("select login from profile").fetchall()
        all1 = [x[0] for x in all1]
        flag = True
        ava = None
        for j, i in enumerate(self.avatar_group.buttons()):
            if i.isChecked():
                ava = self.avatars_list[j]
        if not self.edit_login.text() or self.edit_login.text() in all1:
            self.login.show()
            flag = False
        else:
            self.login.hide()

        if not self.edit_password.text():
            self.password.show()
            flag = False
        else:
            self.password.hide()

        if not self.edit_name.text():
            self.name.show()
            flag = False
        else:
            self.name.hide()

        if not self.edit_surname.text():
            self.surname.show()
            flag = False
        else:
            self.surname.hide()

        if not flag:
            return

        lst = json.dumps([])
        self.cur.execute("""INSERT INTO profile(login, password, name, surname, age, country, avatar, level, ex, money, pic, horror, paint, casino, record_snake, record_tetris)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (self.edit_login.text(), self.edit_password.text(), self.edit_name.text(), self.edit_surname.text(), int(self.spin_age.value()), self.combo_country.currentText(),
                     ava, 1, 0, 0, lst, 0, 0, 0, 0, 0))
        self.con.commit()
        self.con.close()
        self.close()
        self.lob = Lobby(True, self.edit_login.text())
        self.lob.show()


    def ava(self):
        file, ok = QFileDialog.getOpenFileName(
            self, 'Выбери файл', '',
            'Картинки (*.jpg *.png)')
        if not ok or not file:
            return  

        pix = QPixmap(file)
        self.custom_rad = QRadioButton()
        self.avatar_group.addButton(self.custom_rad, 4)
        self.upload_layout.addWidget(self.custom_rad)

        self.lbl_custom.setPixmap(pix.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                             Qt.TransformationMode.SmoothTransformation))
        self.lbl_custom.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_custom.setStyleSheet(
            "border: 2px solid #8b5cf6; border-radius: 10px; background-color: #1e293b;")
        self.avatars_list.append(file)
        self.custom_rad.setChecked(True)


class Lobby(QWidget):
    def __init__(self, flag, login):
        self.login = login
        self.flag = flag
        self.prof = []
        self.pic_lst = []
        super().__init__()

        self.sound_click = QSoundEffect()
        self.sound_click.setSource(QUrl.fromLocalFile("click.wav"))
        self.sound_click.setVolume(0.05)

        self.buy_click = QSoundEffect()
        self.buy_click.setSource(QUrl.fromLocalFile("buy.wav"))
        self.buy_click.setVolume(0.05)

        self.eror_click = QSoundEffect()
        self.eror_click.setSource(QUrl.fromLocalFile("eror.wav"))
        self.eror_click.setVolume(0.05)

        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile("music.mp3"))
        self.player.setLoops(QMediaPlayer.Loops.Infinite)
        self.audio_output.setVolume(0.05)

        self.flag_lider = False

        self.con = sqlite3.connect("proect.db")
        self.cur = self.con.cursor()
        res = self.cur.execute("""select * from profile where login = ?""", (self.login,)).fetchone()
        self.login, self.password, self.name, self.surname, self.age, self.country, self.avatar, self.level0, self.ex, self.money, self.pic, self.horror, self.paint, self.casino, self.record_snake, self.record_tetris = res
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.time1)
        self.timer1.start(1000)
        self.initUI()

    def initUI(self):
        self.player.play()
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
        self.sound_click.play()

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
        self.exit_btn.clicked.connect(self.close)

        self.paint_btn = QPushButton("Paint", self)
        self.paint_btn.setFixedSize(282, 80)
        self.paint_btn.move(292, 820)
        self.paint_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.paint_btn.setStyleSheet("""
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
        self.paint_btn.clicked.connect(self.paint)

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

        self.leaderboard_btn = QPushButton("Лидерборд", self)
        self.leaderboard_btn.setFixedSize(282, 80)
        self.leaderboard_btn.move(0, 730)
        self.leaderboard_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.leaderboard_btn.show()
        self.leaderboard_btn.setStyleSheet("""
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
        self.leaderboard_btn.clicked.connect(self.open_leaderboard)

        self.horror_btn = QPushButton("Хоррор", self)
        self.horror_btn.setFixedSize(282, 80)
        self.horror_btn.move(292, 730)
        self.horror_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.horror_btn.show()
        self.horror_btn.setStyleSheet("""
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
        self.horror_btn.clicked.connect(self.horror)
        self.time = QLabel(self)
        self.time.move(292 + 292, 730)
        self.time.resize(282, 80)
        self.time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time.show()
        self.time1()

        self.time.setStyleSheet("""
                    QLabel {
                        background-color: #1e293b;
                        color: #38bdf8;
                        border: 3px solid #0ea5e9;
                        border-radius: 40px;
                        font-size: 24px;
                        font-weight: bold;
                        font-family: 'Consolas', 'Courier New', monospace;
                        letter-spacing: 1px;
                    }
                """)

        time_shadow = QGraphicsDropShadowEffect()
        time_shadow.setBlurRadius(30)
        time_shadow.setColor(QColor(56, 189, 248, 200))
        time_shadow.setOffset(0, 0)
        self.time.setGraphicsEffect(time_shadow)

        self.inf_btn = QPushButton("Наклейки", self)
        self.inf_btn.setFixedSize(282, 80)
        self.inf_btn.move(1248, 730)
        self.inf_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.inf_btn.show()
        self.inf_btn.setStyleSheet("""
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
        self.inf_btn.clicked.connect(self.inf)

        self.achivki_btn = QPushButton("Достижения", self)
        self.achivki_btn.setFixedSize(282, 80)
        self.achivki_btn.move(1248 - 292 - 80, 730)
        self.achivki_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.achivki_btn.show()
        self.achivki_btn.setStyleSheet("""
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
        self.achivki_btn.clicked.connect(self.achivki)

        x = 0
        y = 220
        y1 = 10
        self.btn_levels = []
        self.kek_pic = []
        self.pic1 = ["icon.png", "quiz.jpg", "reaction.jpg", "human.jpg", "clicker.jpg", "snake.jpg", "tetris.jpg",
                     "math_level.jpg", "flappy_bird.jpg", "checckers.jpg"]

        for i in range(10):
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

    def achivki(self):
        self.hide_lobby()
        self.sound_click.play()

        self.achivki_title = QLabel("🏆 ВАШИ ДОСТИЖЕНИЯ", self)
        self.achivki_title.setGeometry(0, 30, 1540, 80)
        self.achivki_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.achivki_title.setStyleSheet("""
            color: #ffd166; 
            font-size: 56px; 
            font-weight: bold; 
            font-family: 'Georgia', serif;
            background: transparent;
            letter-spacing: 2px;
        """)
        self.achivki_title.show()
        self.prof.append(self.achivki_title)

        title_shadow = QGraphicsDropShadowEffect()
        title_shadow.setBlurRadius(40)
        title_shadow.setColor(QColor(255, 209, 102, 150))
        title_shadow.setOffset(0, 0)
        self.achivki_title.setGraphicsEffect(title_shadow)

        achievements = [
            ("Крестики-нолики", "Победить бота в крестиках-ноликах", self.level0 > 1),
            ("История России", "Пройти викторину по истории на 100%", self.level0 > 2),
            ("Реакция", "Найти все красные кнопки", self.level0 > 3),
            ("Виселица", "Угадать слово и спасти человечка", self.level0 > 4),
            ("Кликер", "Выполнить все задания в кликере", self.level0 > 5),
            ("Змейка", "Набрать 20 очков в змейке", self.level0 > 6),
            ("Тетрис", "Набрать 100 очков в тетрисе", self.level0 > 7),
            ("Математика", "Пройти математический тест", self.level0 > 8),
            ("Flappy Bird", "Пролететь 20 труб", self.level0 > 9),
            ("Хоррор", "Выбраться из проклятого дома", False)
        ]

        start_x = 140
        start_y = 130
        col_width = 400
        row_height = 140

        x = start_x
        y = start_y

        for idx, (name, desc, is_done) in enumerate(achievements):
            card = QFrame(self)
            card.setGeometry(x, y, 380, 120)
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: #1e293b;
                    border: 2px solid {'#16a34a' if is_done else '#dc2626'};
                    border-radius: 15px;
                }}
            """)
            card.show()
            self.prof.append(card)

            icon = QLabel("✔" if is_done else "✖", card)
            icon.setGeometry(15, 15, 40, 40)
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon.setStyleSheet(f"""
                color: {'#16a34a' if is_done else '#dc2626'};
                font-size: 32px;
                font-weight: bold;
                background: transparent;
            """)
            icon.show()

            name_lbl = QLabel(name, card)
            name_lbl.setGeometry(65, 15, 300, 30)
            name_lbl.setStyleSheet(f"""
                color: {'#16a34a' if is_done else '#e2e8f0'};
                font-size: 22px;
                font-weight: bold;
                background: transparent;
            """)
            name_lbl.show()

            desc_lbl = QLabel(desc, card)
            desc_lbl.setGeometry(65, 45, 300, 60)
            desc_lbl.setWordWrap(True)
            desc_lbl.setStyleSheet("""
                color: #94a3b8;
                font-size: 14px;
                background: transparent;
            """)
            desc_lbl.show()

            x += col_width
            if (idx + 1) % 3 == 0:
                x = start_x
                y += row_height

        self.btn_back_ach = QPushButton("Назад", self)
        self.btn_back_ach.setFixedSize(292, 80)
        self.btn_back_ach.move(1248, 820)
        self.btn_back_ach.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back_ach.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                font-size: 26px;
                font-weight: bold;
                border: none;
                border-radius: 40px;
            }
            QPushButton:hover { background-color: #ef4444; }
        """)
        self.btn_back_ach.clicked.connect(self.loddy_fon)
        self.btn_back_ach.show()
        self.prof.append(self.btn_back_ach)

    def time1(self):
        time = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S").split()
        self.time.setText(time[1] + "\n" + time[0])

    def horror(self):
        self.player.stop()
        self.hor = Horror(self.login)
        self.hor.show()
        self.close()

    def inf(self):
        self.flag_lider = True
        self.hide_lobby()
        self.sound_click.play()

        descriptions = [
            "«Свидетель» — Кот смотрит прямо в душу. Видел то, что ты натворил в прошлой игре, и теперь молча осуждает.",
            "«Паникёр» — Кот с картины «Крик». Его лицо, когда ты понял, что поставил всё состояние на «красное», а выпало «чёрное».",
            "«Скрытый агент» — Панда в солнцезащитных очках. Стиль, харизма, полная невозмутимость. Никто не знает, что у неё на уме.",
            "«Одобряю» — Енот с большим пальцем вверх. Тот самый друг, который говорит: «Всё норм, давай ещё одну ставку».",
            "«Добряк» — Пёс в очках с высунутым языком. Абсолютно беззаботный пёсель, которому всё равно, что он проиграл все монеты.",
            "«Босс качалки» — Пёс в кепке и цветных очках. Кажется, он здесь не играет, а просто пришёл набрать массу и попить протеина.",
            "«Спецназ» — Губка Боб в военной экипировке. Готов к любым испытаниям, даже если это просто кнопка «Крутить».",
            "«Неоновый демон» — Красный контур волка. Символизирует твой внутренний азарт, который просыпается ровно в 3 часа ночи.",
            "«Философ» — Бородатый мужчина. Тысячу раз проигрывал, но всё равно сохраняет спокойствие и рассуждает о смысле жизни.",
            "«Хищник» — Тёмный персонаж в шлеме. Легенда ночных серверов. Заходит в игру только чтобы забрать последний джекпот."
        ]

        start_x = 40
        start_y = 20
        col_width = 370
        row_height = 280

        x = start_x
        y = start_y

        pic_lst = []
        for i in range(1, 11):
            pic_lst.append("pic" + str(i))

        for i, j in enumerate(pic_lst):
            container = QWidget(self)
            container.move(x, y)
            container.resize(col_width - 20, row_height - 10)
            container.setStyleSheet("background: transparent;")

            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(5)

            self.image1 = QPixmap(j)
            self.image3 = QLabel(container)
            self.image3.resize(col_width - 20, 150)
            scaled = self.image1.scaled(
                col_width - 20, 150,
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
            layout.addWidget(self.image3)

            self.text_label = QLabel(descriptions[i], container)
            self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.text_label.setWordWrap(True)
            self.text_label.setStyleSheet("""
                color: #FFD700; 
                font-size: 13px; 
                font-weight: bold;
                background: transparent;
            """)
            layout.addWidget(self.text_label)

            container.show()
            self.prof.append(container)

            x += col_width

            if (i + 1) % 4 == 0:
                x = start_x
                y += row_height

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

    def open_leaderboard(self):
        self.sound_click.play()
        if self.flag_lider:
            self.btn_lobby.hide()
        self.hide_lobby()

        rows = self.cur.execute("SELECT name, surname, money, ex, level, age, country FROM profile").fetchall()
        rows = sorted(rows, key=lambda x: (x[4], x[2], x[1], x[0], x[1], x[-2], x[-1]), reverse=True)

        self.table = QTableWidget(self)
        self.table.setSortingEnabled(True)
        self.table.show()
        self.table.setGeometry(100, 100, 1340, 600)
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(rows[0]))
        self.table.setHorizontalHeaderLabels(["Имя", "Фамилия", "Монеты", "Опыт", "Уровень", "Возраст", "Страна"])

        self.table.setStyleSheet("""
               QTableWidget {
                   background-color: #0f172a;
                   color: #e2e8f0;
                   border: 2px solid #334155;
                   border-radius: 15px;
                   gridline-color: #334155;
                   font-size: 18px;
                   outline: 0;
                   selection-background-color: #1e293b;
                   selection-color: #38bdf8;
               }
               QTableWidget::item {
                   padding: 10px;
                   border-bottom: 1px solid #1e293b;
                   border-right: 1px solid #1e293b;
                   background-color: #0f172a;
               }
               QTableWidget::item:alternate {
                   background-color: #16213e;
               }
               QTableWidget::item:selected {
                   background-color: #1e293b;
                   color: #38bdf8;
               }
               QHeaderView::section {
                   background-color: #1e293b;
                   color: #38bdf8;
                   padding: 12px;
                   border: none;
                   border-bottom: 2px solid #38bdf8;
                   border-right: 1px solid #334155;
                   font-weight: bold;
                   font-size: 16px;
               }
               QScrollBar:vertical {
                   border: none;
                   background: #0f172a;
                   width: 10px;
                   margin: 0px;
               }
               QScrollBar::handle:vertical {
                   background: #334155;
                   min-height: 20px;
                   border-radius: 5px;
               }
               QScrollBar::handle:vertical:hover {
                   background: #38bdf8;
               }
               QTableCornerButton::section {
                   background-color: #1e293b;
                   border: none;
               }
           """)

        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                if isinstance(val, int):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                if r == 0:
                    item.setBackground(QColor(251, 191, 36, 50))
                    item.setForeground(QColor(251, 191, 36))
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)

                self.table.setItem(r, c, item)

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)

        self.back_btn = QPushButton("Назад", self)
        self.back_btn.setGeometry(620, 750, 300, 80)
        self.back_btn.setStyleSheet("""
               QPushButton {
                   background-color: #dc2626;
                   color: white;
                   font-size: 26px;
                   font-weight: bold;
                   border: none;
                   border-radius: 40px;
               }
               QPushButton:hover { background-color: #ef4444; }
           """)
        self.back_btn.clicked.connect(self.close_leaderboard)
        self.back_btn.show()

    def close_leaderboard(self):
        self.table.hide()
        self.back_btn.hide()
        self.on_continue()

    def paint(self):
        self.sound_click.play()
        self.player.stop()
        self.paint_level = Paint(self.login)
        self.paint_level.show()
        self.close()

    def casino(self):
        self.sound_click.play()
        self.player.stop()
        casino = Casino(self.login)
        self.close()
        casino.show()

    def hide_lobby(self):
        self.btn_profile.hide()
        self.btn_shop.hide()
        self.horror_btn.hide()
        self.time.hide()
        self.achivki_btn.hide()
        for i in self.kek_pic:
            i.hide()
        self.image2.hide()
        self.paint_btn.hide()
        self.exit_btn.hide()
        self.bonus_btn.hide()
        self.leaderboard_btn.hide()
        self.inf_btn.hide()
        for i in self.btn_levels:
            i.hide()

    def level(self):
        n = int(self.sender().text().split()[1])
        if self.level0 >= n != 10:
            self.hide_lobby()
            self.sound_click.play()

            def friend():
                self.player.stop()
                self.sound_click.play()
                level1 = TicTacToe_friend(self.login)
                self.close()
                level1.show()

            def bot():
                self.player.stop()
                self.sound_click.play()
                level1 = TicTacToe_bot(self.login)
                self.close()
                level1.show()

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
            self.bot_btn.hide()

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
            self.friend_btn.hide()

            if n == 1:
                text = f'''1 - Чтобы перейти на следущий уровень надо пройти игру с ботом.\n
                                            2 - Выиграв бота вы получаете 25 ฿.\n
                                            3 - Игра против друга за нее ничего не получаете.\n
                                            Хорошо провести время!'''

            elif n == 2 or n == 8:
                text = f'''1 - Ответив на все вопросы правильно вы можете перейти на следующий уровень.\n
                                            2 - Ответив на все вопросы правильно вы получаете 30 ฿.\n
                                            3 - Ответив не правильно вы ничего не получите.\n
                                            Хорошо провести время!'''

            elif n == 3:
                text = f'''1 - Если вы наберете 20 очков в игры вы сможете пройти на следущий уровень.\n
                                            2 - За победу вы получаете 30 ฿.\n
                                            Хорошо провести время!'''

            elif n == 4:
                text = f'''1 - Если вы угадаете слово вы сможете пройти на следущий уровень.\n
                                            2 - Угадав слово вы получаете 30 ฿.\n
                                            Хорошо провести время!'''

            elif n == 5:
                text = f'''1 - Если вы выполните все достижения в кликере вы сможете пройти на следущий уровень.\n
                                            2 - Вы получаете 35 ฿.\n
                                            Хорошо провести время!'''

            elif n == 6:
                text = f'''1 - Если вы наберете 20 очков вы сможете пройти на следущий уровень.\n
                                            2 - Вы получаете 35 ฿.\n
                                            Хорошо провести время!'''

            elif n == 7:
                text = f'''1 - Если вы наберете 100 очков вы сможете пройти на следущий уровень.\n
                                            2 - Вы получаете 35 ฿.\n
                                            Хорошо провести время!'''

            elif n == 9:
                text = f'''1 - Если вы наберете 20 очков вы сможете пройти на следущий уровень.\n
                                            2 - Вы получаете 40 ฿.\n
                                            Хорошо провести время!'''

            def start():
                self.player.stop()
                self.sound_click.play()
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
                if n == 7:
                    self.level7 = TetrisGame(self.login)
                    self.hide()
                    self.level7.show()
                if n == 8:
                    self.level8 = Math(self.login)
                    self.hide()
                    self.level8.show()
                if n == 9:
                    self.level9 = FlappyBird(self.login)
                    self.hide()
                    self.level9.show()

            def info():
                self.sound_click.play()
                QMessageBox.information(self, "Информация",
                                        text)

            def back():
                self.sound_click.play()
                self.info_btn2.hide()
                self.back_btn2.hide()
                self.start_btn2.hide()
                self.icon12.hide()
                if n == 1:
                    self.friend_btn.hide()
                    self.bot_btn.hide()
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

            self.icon2 = QPixmap(self.pic1[n - 1])
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

            self.start_btn2 = QPushButton("Начать", self)
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

            if n == 1:
                self.friend_btn.show()
                self.bot_btn.show()
                self.start_btn2.hide()

    def shop_fon(self):
        self.sound_click.play()
        self.hide_lobby()
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

            self.cor_not = QLabel(self)
            self.cor_not.resize(20, 20)
            self.cor_not.move(x, y1)
            if j in self.pic:
                self.cor_not.setText("✅")
            else:
                self.cor_not.setText("❌")
            self.cor_not.show()
            self.prof.append(self.cor_not)

            x += 250
            if i == 4:
                x = 30
                y = 550
                y1 = 760

    def buy(self):
        n = int(self.sender().text().split()[0])
        if self.money >= n:
            if self.pic_lst[self.price_pic.index(n)] not in self.pic:
                self.buy_click.play()
                self.money -= n
                self.balance_label.setText(f"Ваш баланс: {self.money} ฿")
                n1 = json.loads(self.pic)
                n1.append(self.pic_lst[self.price_pic.index(n)])
                self.pic = json.dumps(n1)
                self.cur.execute('UPDATE profile SET pic=?, money=? WHERE login=?', (self.pic, self.money, self.login))
                self.con.commit()
                self.loddy_fon()
                self.shop_fon()

            else:
                self.eror_click.play()
        else:
            self.eror_click.play()

    def profile_fon(self):
        self.hide_lobby()
        self.sound_click.play()
        self.image67 = QPixmap(self.avatar)
        self.image23 = QLabel(self)
        self.image23.move(660, 50)
        self.image23.resize(200, 200)
        scaled = self.image67.scaled(
            200, 200,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image23.setPixmap(scaled)
        self.image23.setStyleSheet("""
            border: 2px solid #334155;
            border-radius: 12px;
            background-color: #1e293b;
            padding: 4px;
        """)
        self.image23.show()
        self.prof.append(self.image23)

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

        x = 990
        y = 50
        for i in range(self.level0 - 1):
            self.img = QPixmap(self.pic1[i])
            self.img2 = QLabel(self)
            self.img2.move(x, y)
            self.img2.resize(150, 150)
            scaled = self.img.scaled(
                150, 150,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.img2.setPixmap(scaled)
            self.img2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.img2.setStyleSheet("""
                border: 2px solid #334155;
                border-radius: 8px;
                background-color: #1e293b;
                padding: 4px;
            """)
            self.img2.show()
            self.prof.append(self.img2)
            x += 200
            if (i + 1) % 3 == 0:
                x = 990
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

        self.btn_money_fake = QPushButton("Получить монеты (бесплатно)", self)
        self.btn_money_fake.move(0, 840)
        self.btn_money_fake.setFixedSize(500, 60)
        self.btn_money_fake.setStyleSheet("""
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
        self.btn_money_fake.show()
        self.btn_money_fake.clicked.connect(self.money_fake)
        self.prof.append(self.btn_money_fake)

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

    def money_fake(self):
        self.fake = Fake(self.login)
        self.fake.btn_ok.clicked.connect(self.reload_lobby)
        self.close()
        self.fake.show()

    def reload_lobby(self):
        self.lobby = Lobby(None, self.login)
        self.lobby.show()
        self.fake.close()


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
        self.setWindowTitle('Вход')
        self.setFixedSize(1540, 900)

        self.login_page = QWidget(self)
        self.login_page.setGeometry(0, 0, 1540, 900)

        layout = QVBoxLayout(self.login_page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        self.pixmap_lock = QPixmap('lock.jpg')
        self.image_lock = QLabel(self.login_page)
        self.image_lock.setPixmap(self.pixmap_lock.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                                          Qt.TransformationMode.SmoothTransformation))
        self.image_lock.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_lock)

        self.login1 = QLineEdit(self.login_page)
        self.login1.setPlaceholderText("Введите логин")
        self.login1.setFixedSize(400, 50)
        self.login1.setStyleSheet("font-size: 18px; padding: 5px;")
        layout.addWidget(self.login1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.password1 = QLineEdit(self.login_page)
        self.password1.setPlaceholderText("Введите пароль")
        self.password1.setEchoMode(QLineEdit.EchoMode.Password)
        self.password1.setFixedSize(400, 50)
        self.password1.setStyleSheet("font-size: 18px; padding: 5px;")
        layout.addWidget(self.password1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.entry_bt = QPushButton("Войти", self.login_page)
        self.entry_bt.setFixedSize(400, 60)
        self.entry_bt.setCursor(Qt.CursorShape.PointingHandCursor)
        self.entry_bt.clicked.connect(self.entry)
        layout.addWidget(self.entry_bt, alignment=Qt.AlignmentFlag.AlignCenter)

        self.register_bt = QPushButton("Зарегистрироваться", self.login_page)
        self.register_bt.setFixedSize(400, 60)
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
        layout.addWidget(self.register_bt, alignment=Qt.AlignmentFlag.AlignCenter)

        self.error_label = QLabel("Не верный логин или пароль!", self.login_page)
        self.error_label.setStyleSheet("color: #f87171; font-size: 20px; font-weight: bold;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.hide()
        layout.addWidget(self.error_label)

    def entry(self):
        self.con = sqlite3.connect("proect.db")
        self.cur = self.con.cursor()
        res = self.cur.execute("""select * from profile where login = ?""", (self.login1.text(),)).fetchone()
        if res:
            self.login, self.password, self.name, self.surname, self.age, self.country, self.avatar, self.level0, self.ex, self.money, self.pic, self.horror, self.paint, self.casino, self.record_snake, self.record_tetris = res
            if self.password1.text() == self.password:
                self.login_page.hide()
                self.error_label.hide()
                self.check_on_robot()
                return
        self.error_label.show()

    def sec(self):
        self.close()
        self.second_window = SecondWindow()

    def check_on_robot(self):
        self.captcha_page = QWidget(self)
        self.captcha_page.setGeometry(0, 0, 1540, 900)
        self.captcha_page.show()

        main_layout = QVBoxLayout(self.captcha_page)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(20)

        self.check = QLabel("ПРОЙДИТЕ КАПЧУ!!!", self.captcha_page)
        self.check.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.check.setStyleSheet("color: #f87171; font-weight: bold; font-size: 40px;")
        main_layout.addWidget(self.check)

        self.bike = QLabel("Найдите все велосипеды!!!", self.captcha_page)
        self.bike.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bike.setStyleSheet("color: #cbd5e1; font-size: 24px;")
        main_layout.addWidget(self.bike)

        self.check_count = QLabel(f"Попыток осталось - {self.count}", self.captcha_page)
        self.check_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.check_count.setStyleSheet("color: #fbbf24; font-size: 24px;")
        main_layout.addWidget(self.check_count)

        grid_frame = QFrame(self.captcha_page)
        grid_layout = QGridLayout(grid_frame)
        grid_layout.setSpacing(15)

        self.checkbox = []
        self.img_error = []

        for j, i in enumerate(self.img):
            self.image1 = QPixmap(i)
            self.image2 = QLabel(grid_frame)
            self.image2.resize(200, 200)
            scaled = self.image1.scaled(
                200, 200,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image2.setPixmap(scaled)
            self.image2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.image2.setStyleSheet("""
                border: 2px solid #334155;
                border-radius: 8px;
                background-color: #1e293b;
                padding: 4px;
            """)
            self.img_error.append(self.image2)

            self.check_box = QCheckBox(grid_frame)
            self.check_box.setCursor(Qt.CursorShape.PointingHandCursor)
            self.checkbox.append(self.check_box)

            cell_widget = QWidget()
            cell_layout = QVBoxLayout(cell_widget)
            cell_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cell_layout.addWidget(self.image2)
            cell_layout.addWidget(self.check_box, alignment=Qt.AlignmentFlag.AlignCenter)

            row = j // 3
            col = j % 3
            grid_layout.addWidget(cell_widget, row, col)

        main_layout.addWidget(grid_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        self.check_btn = QPushButton("Проверить", self.captcha_page)
        self.check_btn.setFixedSize(400, 60)
        self.check_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.check_btn.clicked.connect(self.true_false)
        main_layout.addWidget(self.check_btn, alignment=Qt.AlignmentFlag.AlignCenter)

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
            self.captcha_page.hide()
            self.close()
            self.flag = False
            self.lobby = Lobby(self.flag, self.login)
            self.lobby.show()

    def error(self):
        self.count -= 1
        if self.count != 0:
            self.check_count.setText(f"Попыток осталось - {self.count}")
            self.img = random.sample(
                ["bike1.png", "bike2.png", "bike3.jpg",
                 "car1.png", "car2.jpg", "car3.png",
                 "kat1.jpg", "kat2.png", "kat3.png"], k=9)
            self.captcha_page.hide()
            self.check_on_robot()
        else:
            self.captcha_page.hide()

            self.robot_true = QLabel("ТЫ РОБОТ!!!", self)
            self.robot_true.setGeometry(0, 0, 1540, 900)
            self.robot_true.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.robot_true.setStyleSheet("""
                color: #f87171; 
                font-weight: bold; 
                font-size: 100px; 
                background-color: #0f172a;
            """)
            self.robot_true.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
