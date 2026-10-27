import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGraphicsDropShadowEffect, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
import random


class InfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Информация")
        self.setFixedSize(500, 400)
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
                border-radius: 15px;
                padding: 12px 30px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #33ebff, stop:1 #338cff);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("📖 Как играть")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #00e5ff; font-size: 28px; font-weight: bold;")
        layout.addWidget(title)

        text = QLabel(
            "Нажимайте на большой кристалл 💎, чтобы зарабатывать кристаллы.\n\n"
            "В магазине можно покупать улучшения:\n"
            "• 🤖 Автокликер — даёт пассивный доход каждую секунду.\n"
            "• ⚡ Множитель — увеличивает доход за клик в 2 раза.\n"
            "• 🎯 Крит — шанс получить x5 кристаллов за клик.\n"
            "• 🎁 Бонусный клик — рискни 100 💎 ради крупной награды.\n\n"
            "Удачи в добыче космических кристаллов!"
        )
        text.setWordWrap(True)
        text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        text.setStyleSheet("font-size: 16px; line-height: 1.5;")
        layout.addWidget(text)

        layout.addStretch()

        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)


class Achievements(QWidget):
    def __init__(self, one, two, three, four, five):
        super().__init__()
        self.five = five
        self.four = four
        self.three = three
        self.two = two
        self.one = one
        self.setWindowTitle("Достижения")
        self.setFixedSize(500, 400)
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
                border-radius: 15px;
                padding: 12px 30px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #33ebff, stop:1 #338cff);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Достижения!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #00e5ff; font-size: 28px; font-weight: bold;")
        layout.addWidget(title)

        one = "❌"
        two = "❌"
        three = "❌"
        four = "❌"
        five = "❌"

        if self.one:
            one = "✅"
        if self.two:
            two = "✅"
        if self.three:
            three = "✅"
        if self.four:
            four = "✅"
        if self.five:
            five = "✅"

        text = QLabel(
            "Это все достижения которые надо выполнить чтобы перейти на следующий уровень\n\n"
            f"1 - Прокачать автокликер до максимального уровня. {one}\n"
            f"2 - Прокачать множитель до максимального уровня. {two}\n"
            f"3 - Прокачать крит до максимального уровня. {three}\n"
            f"4 - Выиграть в бонусном клике. {four}\n"
            f"5 - Добыть 100000 кристалов. {five}\n\n"
            "Удачи в добыче космических кристаллов!"
        )
        text.setWordWrap(True)
        text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        text.setStyleSheet("font-size: 16px; line-height: 1.5;")
        layout.addWidget(text)

        layout.addStretch()

        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)


class ClickerUI(QWidget):
    def __init__(self, login):
        super().__init__()
        self.one_click = 1
        self.login = login
        self.price_auto = 50
        self.level_auto = 0
        self.auto_income = 0
        self.crit_n = 0
        self.price_crit = 200
        self.level_mult = 0
        self.price_mult = 100
        self.mult_lev = 1
        self.one = False
        self.two = False
        self.three = False
        self.four = False
        self.five = False
        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)

    def initUI(self):
        self.setWindowTitle("Кликер: Космические кристаллы")
        self.setFixedSize(1000, 800)

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
                border-radius: 15px;
                padding: 15px 30px;
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
            QScrollArea { border: none; background: transparent; }
            QScrollArea > QWidget > QWidget { background: transparent; }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        self.score_frame = QFrame()
        self.score_frame.setStyleSheet(
            "background: rgba(30, 41, 59, 0.8); border-radius: 20px; border: 2px solid #00e5ff;")
        self.score_layout = QVBoxLayout(self.score_frame)

        self.score_label = QLabel("0")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setStyleSheet("color: #00e5ff; font-size: 64px; font-weight: 900;")
        self.score_layout.addWidget(self.score_label)

        self.income_label = QLabel("Доход в секунду: 0")
        self.income_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.income_label.setStyleSheet("color: #94a3b8; font-size: 18px;")
        self.score_layout.addWidget(self.income_label)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 229, 255, 100))
        self.shadow.setOffset(0, 0)
        self.score_frame.setGraphicsEffect(self.shadow)
        main_layout.addWidget(self.score_frame)

        self.center_layout = QHBoxLayout()
        self.center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.left_btn_layout = QVBoxLayout()
        self.left_btn_layout.setSpacing(10)
        self.left_btn_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.btn_info = QPushButton("Информация", self)
        self.btn_info.setFixedSize(200, 60)
        self.btn_info.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00e5ff, stop:1 #0072ff);
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #33ebff, stop:1 #338cff);
            }
        """)
        self.left_btn_layout.addWidget(self.btn_info)
        self.btn_info.clicked.connect(self.open_info)

        self.btn_achievements = QPushButton("Достижения", self)
        self.btn_achievements.setFixedSize(200, 60)
        self.btn_achievements.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f59e0b, stop:1 #fbbf24);
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #fbbf24, stop:1 #fcd34d);
            }
        """)
        self.left_btn_layout.addWidget(self.btn_achievements)
        self.btn_achievements.clicked.connect(self.open_achievements)

        self.center_layout.addLayout(self.left_btn_layout)

        self.click_button = QPushButton("💎")
        self.click_button.setFixedSize(250, 250)
        self.click_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.click_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ff416c, stop:1 #ff4b2b);
                color: white;
                border-radius: 125px;
                font-size: 80px;
                font-weight: bold;
                border: 6px solid rgba(255, 255, 255, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ff5e7d, stop:1 #ff6b4f);
            }
        """)
        self.click_button.clicked.connect(self.clic)
        self.btn_shadow = QGraphicsDropShadowEffect(self)
        self.btn_shadow.setBlurRadius(50)
        self.btn_shadow.setColor(QColor(255, 65, 108, 150))
        self.btn_shadow.setOffset(0, 10)
        self.click_button.setGraphicsEffect(self.btn_shadow)
        self.center_layout.addWidget(self.click_button)

        self.prestige_frame = QFrame()
        self.prestige_frame.setFixedSize(250, 250)
        self.prestige_frame.setStyleSheet(
            "background: rgba(30, 41, 59, 0.8); border-radius: 20px; border: 2px solid #fbbf24;")
        self.prestige_layout = QVBoxLayout(self.prestige_frame)

        self.prestige_title = QLabel("🌟 Доход за клик:\n1")
        self.prestige_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prestige_title.setStyleSheet("color: #fbbf24; font-size: 24px; font-weight: bold;")
        self.prestige_layout.addWidget(self.prestige_title)

        self.center_layout.addWidget(self.prestige_frame)
        main_layout.addLayout(self.center_layout)

        self.shop_scroll = QScrollArea()
        self.shop_scroll.setWidgetResizable(True)
        self.shop_widget = QWidget()
        self.shop_layout = QGridLayout(self.shop_widget)
        self.shop_layout.setSpacing(15)
        self.shop_scroll.setWidget(self.shop_widget)
        main_layout.addWidget(self.shop_scroll)

        self.auto_btn = QPushButton("🤖 Автокликер ур.0\nЦена: 50 💎")
        self.auto_btn.setFixedHeight(80)
        self.auto_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #11998e, stop:1 #38ef7d);
                border-radius: 15px; font-size: 16px; text-align: left; padding-left: 20px;
            }
        """)
        self.shop_layout.addWidget(self.auto_btn, 0, 0)
        self.auto_btn.clicked.connect(self.auto_click)

        self.mult_btn = QPushButton("⚡ Множитель x1 (ур.0)\nЦена: 100 💎")
        self.mult_btn.setFixedHeight(80)
        self.mult_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f59e0b, stop:1 #fbbf24);
                border-radius: 15px; font-size: 16px; text-align: left; padding-left: 20px;
            }
        """)
        self.shop_layout.addWidget(self.mult_btn, 0, 1)
        self.mult_btn.clicked.connect(self.mult)

        self.crit_btn = QPushButton("🎯 Крит шанс: 0%\nЦена: 200 💎")
        self.crit_btn.setFixedHeight(80)
        self.crit_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e11d48, stop:1 #fb7185);
                border-radius: 15px; font-size: 16px; text-align: left; padding-left: 20px;
            }
        """)
        self.shop_layout.addWidget(self.crit_btn, 1, 0)
        self.crit_btn.clicked.connect(self.crit)

        self.bonus_btn = QPushButton("🎁 Бонусный клик (Случайный x5)\nЦена: 100 💎")
        self.bonus_btn.setFixedHeight(80)
        self.bonus_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8e44ad, stop:1 #a55eea);
                border-radius: 15px; font-size: 16px;
            }
        """)
        self.shop_layout.addWidget(self.bonus_btn, 1, 1)
        self.bonus_btn.clicked.connect(self.bonus)

    def open_info(self):
        self.info_window = InfoWindow()
        self.info_window.show()

    def open_achievements(self):
        self.achievements_window = Achievements(self.one, self.two, self.three, self.four, self.five)
        self.achievements_window.show()

    def bonus(self):
        if int(self.score_label.text()) >= 100:
            crit_num = random.randint(1, 3)
            if crit_num == 3:
                self.score_label.setText(str(int(self.score_label.text()) + self.one_click * 10))
                self.four = True
            else:
                self.score_label.setText(str(int(self.score_label.text()) - 100))
            self.bonus_btn.setText(f'🎁 Бонусный клик (Случайный x5)\nЦена: 100 💎')

    def mult(self):
        if int(self.score_label.text()) >= self.price_mult and self.level_mult != 10:
            self.score_label.setText(str(int(self.score_label.text()) - self.price_mult))
            self.price_mult *= 2
            self.level_mult += 1
            self.one_click *= 2
            if self.level_mult == 10:
                self.mult_btn.setText(f'⚡ Множитель x2 max')
                self.two = True
            else:
                self.mult_btn.setText(f'⚡ Множитель x2 (ур.{self.level_mult})\nЦена: {self.price_mult} 💎')
            self.prestige_title.setText(f"🌟 Доход за клик:\n {self.one_click}")

    def clic(self):
        if self.crit_n != 0:
            crit_num = random.randint(1, 20)
            if crit_num in [i for i in range(1, self.crit_n // 5 + 1)]:
                self.score_label.setText(str(int(self.score_label.text()) + self.one_click * 5))
                return
        self.score_label.setText(str(int(self.score_label.text()) + self.one_click))

    def auto_click(self):
        if int(self.score_label.text()) >= self.price_auto and self.level_auto != 10:
            if self.level_auto == 0:
                self.auto_income = 1
            self.score_label.setText(str(int(self.score_label.text()) - self.price_auto))
            self.price_auto += 100
            self.level_auto += 1
            self.auto_income *= 2
            if self.level_auto == 10:
                self.auto_btn.setText(f'🤖 Автокликер max')
                self.one = True
            else:
                self.auto_btn.setText(f'🤖 Автокликер ур.{self.level_auto}\nЦена: {self.price_auto} 💎')
            self.income_label.setText(f"Доход в секунду: {self.auto_income}")

    def tick(self):
        if self.auto_income > 0:
            current_score = int(self.score_label.text())
            self.score_label.setText(str(current_score + self.auto_income))
        if int(self.score_label.text()) >= 100000:
            self.five = True

    def crit(self):
        if int(self.score_label.text()) >= self.price_crit and self.crit_n != 100:
            self.score_label.setText(str(int(self.score_label.text()) - self.price_crit))
            self.crit_n += 5
            self.price_crit += 200
            if self.crit_n == 100:
                self.crit_btn.setText(f'🎯 Крит шанс: {self.crit_n} max ')
                self.three = True
                return
            self.crit_btn.setText(f'🎯 Крит шанс: {self.crit_n}%\nЦена: {self.price_crit} 💎')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClickerUI()
    window.show()
    sys.exit(app.exec())