import sqlite3
import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QTableWidget,
                             QVBoxLayout, QWidget, QHeaderView, QPushButton,
                             QTableWidgetItem)
from PyQt6.QtGui import QColor


class Table(QMainWindow):
    def __init__(self, login):
        super().__init__()
        self.setWindowTitle("Зал славы")
        self.setFixedSize(1540, 900)
        self.login = login

        self.con = sqlite3.connect("proect.db")
        self.cur = self.con.cursor()

        self.res = self.cur.execute("""
            SELECT name, surname, money, ex, level, age, country, record_snake, record_tetris, record_flappy_bird 
            FROM profile
        """).fetchall()

        res = self.cur.execute("""SELECT music FROM profile where login=?""", (self.login,)).fetchone()
        self.music = res[0]

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #0f172a, stop:0.5 #1e3c72, stop:1 #2a5298);
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #e2e8f0;
            }
            QLabel {
                background: transparent;
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #dc2626; }
            QPushButton:pressed { background-color: #b91c1c; }
            QTabWidget::pane {
                border: 2px solid #38bdf8;
                border-radius: 10px;
                background-color: #0f172a;
                top: -2px;
            }
            QTabBar::tab {
                background-color: #1e293b;
                color: #94a3b8;
                border: 2px solid #38bdf8;
                border-bottom: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #0f172a;
                color: #38bdf8;
            }
            QTabBar::tab:hover:!selected {
                background-color: #334155;
                color: #e2e8f0;
            }
            QTableWidget {
                background-color: #0f172a;
                color: #e2e8f0;
                border: 2px solid #334155;
                border-radius: 10px;
                gridline-color: #475569;
                font-size: 16px;
                outline: 0;
            }
            QTableWidget::item {
                padding: 12px 10px;
                border-right: 1px solid #334155;
                border-bottom: 1px solid #334155;
            }
            QTableWidget::item:alternate {
                background-color: #16213e;
            }
            QTableWidget::item:selected {
                background-color: #0ea5e9;
                color: white;
            }
            QHeaderView::section {
                background-color: #1e293b;
                color: #38bdf8;
                padding: 12px;
                border: none;
                border-right: 2px solid #0f172a;
                border-bottom: 2px solid #38bdf8;
                font-weight: bold;
                font-size: 16px;
            }
            QScrollBar:vertical {
                border: none;
                background: #0f172a;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #334155;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #38bdf8;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.open_button = QPushButton("Выйти")
        self.open_button.clicked.connect(self.exit)
        layout.addWidget(self.open_button)

        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        self.create_empty_tabs()

        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile("music.wav"))
        self.player.setLoops(QMediaPlayer.Loops.Infinite)
        self.audio_output.setVolume(0.05)

        self.update_tables()

    def create_empty_tabs(self):
        data_widget = QWidget()
        data_layout = QVBoxLayout(data_widget)
        self.data_table = QTableWidget()
        self.data_table.setSortingEnabled(True)
        self.data_table.verticalHeader().setVisible(False)
        self.data_table.setAlternatingRowColors(True)
        self.data_table.setShowGrid(True)
        data_layout.addWidget(self.data_table)
        self.tab_widget.addTab(data_widget, "Общее")

        count_widget = QWidget()
        count_layout = QVBoxLayout(count_widget)
        self.count_table = QTableWidget()
        self.count_table.setSortingEnabled(True)
        self.count_table.verticalHeader().setVisible(False)
        self.count_table.setAlternatingRowColors(True)
        self.count_table.setShowGrid(True)
        count_layout.addWidget(self.count_table)
        self.tab_widget.addTab(count_widget, "Змейка")

        match_widget = QWidget()
        match_layout = QVBoxLayout(match_widget)
        self.match_table = QTableWidget()
        self.match_table.setSortingEnabled(True)
        self.match_table.verticalHeader().setVisible(False)
        self.match_table.setAlternatingRowColors(True)
        self.match_table.setShowGrid(True)
        match_layout.addWidget(self.match_table)
        self.tab_widget.addTab(match_widget, "Тетрис")

        no_match_widget = QWidget()
        no_match_layout = QVBoxLayout(no_match_widget)
        self.no_match_table = QTableWidget()
        self.no_match_table.setSortingEnabled(True)
        self.no_match_table.verticalHeader().setVisible(False)
        self.no_match_table.setAlternatingRowColors(True)
        self.no_match_table.setShowGrid(True)
        no_match_layout.addWidget(self.no_match_table)
        self.tab_widget.addTab(no_match_widget, "Flappy bird")

    def exit(self):
        self.player.stop()
        self.con.commit()
        self.con.close()
        from proect import Lobby
        self.lobby = Lobby(None, self.login)
        self.lobby.show()
        self.close()

    def update_tables(self):
        if self.music == 1:
            self.player.play()
        self.update_data_table()
        self.update_count_table()
        self.update_match_table()
        self.update_no_match_table()

    def style_item(self, item, r):
        font = item.font()
        font.setBold(True)
        font.setPointSize(11)
        item.setFont(font)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        if r == 0:
            item.setBackground(QColor(255, 215, 0, 100))
            item.setForeground(QColor(255, 255, 255))
        elif r == 1:
            item.setBackground(QColor(192, 192, 192, 100))
            item.setForeground(QColor(255, 255, 255))
        elif r == 2:
            item.setBackground(QColor(205, 127, 50, 100))
            item.setForeground(QColor(255, 255, 255))

    def update_data_table(self):
        rows = sorted(self.res, key=lambda x: (x[4], x[2], x[3]), reverse=True)

        self.data_table.setRowCount(len(rows))
        self.data_table.setColumnCount(7)
        self.data_table.setHorizontalHeaderLabels(["Имя", "Фамилия", "Монеты", "Опыт", "Уровень", "Возраст", "Страна"])

        for r, row in enumerate(rows):
            for c in range(7):
                val = str(row[c])
                item = QTableWidgetItem(val)
                self.style_item(item, r)
                self.data_table.setItem(r, c, item)

        h = self.data_table.horizontalHeader()
        h.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def update_count_table(self):
        rows = sorted(self.res, key=lambda x: x[7], reverse=True)

        self.count_table.setRowCount(len(rows))
        self.count_table.setColumnCount(3)
        self.count_table.setHorizontalHeaderLabels(["Имя", "Фамилия", "Рекорд в Змейке"])

        for r, row in enumerate(rows):
            item1 = QTableWidgetItem(row[0])
            self.style_item(item1, r)
            self.count_table.setItem(r, 0, item1)

            item2 = QTableWidgetItem(row[1])
            self.style_item(item2, r)
            self.count_table.setItem(r, 1, item2)

            item3 = QTableWidgetItem(str(row[7]))
            self.style_item(item3, r)
            self.count_table.setItem(r, 2, item3)

        h = self.count_table.horizontalHeader()
        h.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def update_match_table(self):
        rows = sorted(self.res, key=lambda x: x[8], reverse=True)

        self.match_table.setRowCount(len(rows))
        self.match_table.setColumnCount(3)
        self.match_table.setHorizontalHeaderLabels(["Имя", "Фамилия", "Рекорд в Тетрисе"])

        for r, row in enumerate(rows):
            item1 = QTableWidgetItem(row[0])
            self.style_item(item1, r)
            self.match_table.setItem(r, 0, item1)

            item2 = QTableWidgetItem(row[1])
            self.style_item(item2, r)
            self.match_table.setItem(r, 1, item2)

            item3 = QTableWidgetItem(str(row[8]))
            self.style_item(item3, r)
            self.match_table.setItem(r, 2, item3)

        h = self.match_table.horizontalHeader()
        h.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def update_no_match_table(self):
        rows = sorted(self.res, key=lambda x: x[-1], reverse=True)

        self.no_match_table.setRowCount(len(rows))
        self.no_match_table.setColumnCount(3)
        self.no_match_table.setHorizontalHeaderLabels(["Имя", "Фамилия", "Рекорд в Flappy Bird"])

        for r, row in enumerate(rows):
            item1 = QTableWidgetItem(row[0])
            self.style_item(item1, r)
            self.no_match_table.setItem(r, 0, item1)

            item2 = QTableWidgetItem(row[1])
            self.style_item(item2, r)
            self.no_match_table.setItem(r, 1, item2)

            item3 = QTableWidgetItem(str(row[-1]))
            self.style_item(item3, r)
            self.no_match_table.setItem(r, 2, item3)

        h = self.no_match_table.horizontalHeader()
        h.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Table("s")
    window.show()
    sys.exit(app.exec())