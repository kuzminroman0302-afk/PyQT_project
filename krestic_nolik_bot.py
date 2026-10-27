import json
import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QRadioButton, QPushButton, QLabel, QLineEdit, QLCDNumber, QMessageBox
import random

class TicTacToe_bot(QWidget):
    def __init__(self, login):
        super().__init__()
        self.login = login
        self.button_grid = []
        self.pl = 'X'
        self.v = True
        self.r = True
        self.initUI()

    def initUI(self):
        self.setFixedSize(1540, 900)
        self.setWindowTitle('Крестики нолики')
        x = 500
        y = 150

        for i in range(3):
            g = []
            for j in range(3):
                self.x1 = QPushButton(' ', self)
                self.x1.resize(200, 200)
                self.x1.move(x, y)
                self.x1.clicked.connect(lambda h, i=i, j=j: self.clic(i, j))
                x += 210
                g.append(self.x1)
            self.button_grid.append(g)
            y += 210
            x = 500
        self.x_radio = QRadioButton(self)
        self.x_radio.move(550, 50)
        self.x_radio.setText("X")
        self.x_radio.setChecked(True)
        self.x_radio.clicked.connect(self.game)

        self.o_radio = QRadioButton(self)
        self.o_radio.move(600, 50)
        self.o_radio.setText("O")
        self.o_radio.setChecked(False)
        self.o_radio.clicked.connect(self.game)

        self.new_game_button = QPushButton(self)
        self.new_game_button.resize(300, 80)
        self.new_game_button.move(650, 800)
        self.new_game_button.setText("Новая игра")
        self.new_game_button.clicked.connect(self.game)
        self.new_game_button.setStyleSheet("""
            QPushButton {
                background-color: #ffd166;
                color: #1e3c72;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover   { background-color: #ffe08a; }
            QPushButton:pressed { background-color: #e6b94a; }
        """)
        self.result = QLabel("", self)
        self.result.move(700, 50)
        self.result.setStyleSheet("color: #dc2626; font-size: 42px; font-weight: bold;")

        self.exit_btn = QPushButton(self)
        self.exit_btn.resize(300, 80)
        self.exit_btn.move(0, 800)
        self.exit_btn.setText("Lobby")
        self.exit_btn.clicked.connect(self.exit)
        self.exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: #1e3c72;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover   { background-color: #dc2626; }
            QPushButton:pressed { background-color: #dc2626; }
        """)

    def exit(self):
        from proect import Lobby
        self.close()
        self.lobby = Lobby(None, self.login)
        self.lobby.show()


    def clic(self, i, j):
        btn = self.button_grid[i][j]
        if btn.text() != ' ' or self.v is False:
            return

        btn.setText(self.pl)
        self.check()
        if self.mb_win() is not None:
            y, x = self.mb_win()
            btn = self.button_grid[y][x]
            if self.pl == "X":
                btn.setText("O")
            else:
                btn.setText("X")
        else:
            if not self.over():
                while 1:
                    y, x = random.randint(0, 2), random.randint(0, 2)
                    btn = self.button_grid[y][x]
                    if btn.text() == ' ':
                        if self.pl == "X":
                            btn.setText("O")
                        else:
                            btn.setText("X")
                        break
        self.check()

    def check(self):
        if self.win() is not True:
            self.dis()
            if self.win() == "X":
                if self.pl == "O":
                    self.result.setText("Выиграл БОТ!")
                else:
                    with open("info.json", "r") as f:
                        prof = json.load(f)
                    self.result.setText(f"Выиграл {prof[self.login]["surname"] + prof[self.login]["name"]}!")
                    self.result.resize(500, 80)
                    QMessageBox.information(self, 'Победа!', 'Поздравляю вы прошли первый уровень!\n'
                                                             'Вам начислено 25 ฿.\n'
                                                             'Ex + 10')
                    self.close()
                    from proect import Lobby
                    self.lobby = Lobby(None, self.login)
                    self.lobby.show()
                    prof[self.login]["money"] += 25
                    if prof[self.login]["level"] == 1:
                        prof[self.login]["level"] += 1
                    prof[self.login]["ex"] += 10
                    with open('info.json', 'w') as f:
                        json.dump(prof, f)
                self.result.resize(500, 80)
                self.result.show()
                self.v = False
            elif self.win() == "O":
                if self.pl == "X":
                    self.result.setText("Выиграл БОТ!")
                else:
                    with open("info.json", "r") as f:
                        prof = json.load(f)
                    self.result.setText(f"Выиграл {prof[self.login]["surname"] + prof[self.login]["name"]}!")
                    self.result.resize(500, 80)
                    QMessageBox.information(self, 'Победа!', 'Поздравляю вы прошли первый уровень!\n'
                                                             'Вам начислено 25 ฿.\n'
                                                             'Ex + 10')
                    self.close()
                    from proect import Lobby
                    self.lobby = Lobby(None, self.login)
                    self.lobby.show()
                    prof[self.login]["money"] += 25
                    if prof[self.login]["level"] == 1:
                        prof[self.login]["level"] += 1
                    prof[self.login]["ex"] += 10
                    with open('info.json', 'w') as f:
                        json.dump(prof, f)
                self.result.resize(500, 80)
                self.result.show()
                self.v = False
        if self.over():
            self.dis()
            self.result.setText("Ничья!")
            self.result.resize(500, 80)
            self.result.show()
            return

    def mb_win(self):
        all = [[i.text() for i in self.button_grid[0]], [i.text() for i in self.button_grid[1]],
             [i.text() for i in self.button_grid[2]]]
        for i in range(len(all)):
            prom = ''
            for j in range(len(all[i])):
                prom += all[i][j]
            if (prom.count('X') == 2 and self.pl == 'X' and " " in prom) or (prom.count('O') == 2 and self.pl == 'O' and " " in prom):
                return i, prom.index(' ')

        for i in range(3):
            prom = ''
            for j in range(3):
                prom += self.button_grid[j][i].text()
            if (prom.count('X') == 2 and self.pl == 'X' and " " in prom) or (prom.count('O') == 2 and self.pl == 'O' and " " in prom):
                return prom.index(' '), i

        left = self.button_grid[0][0].text() + self.button_grid[1][1].text() + self.button_grid[2][2].text()
        if left == 'XX ' or left == 'OO ':
            return 2, 2

        if left == 'X X' or left == 'O O':
            return 1, 1

        if left == ' XX' or left == ' OO':
            return 0, 0

        right = self.button_grid[2][0].text() + self.button_grid[1][1].text() + self.button_grid[0][2].text()
        if right == 'XX ' or right == 'OO ':
            return 0, 2

        if right == 'X X' or right == 'O O':
            return 1, 1

        if right == ' XX' or right == ' OO':
            return 2, 0
        return None

    def game(self):
        if self.sender().text() == "X" and self.r:
            return
        if self.sender().text() == "O" and self.r is False:
            return
        self.gaz()
        self.v = True
        self.result.setText('')
        if self.x_radio.isChecked():
            self.pl = 'X'
            self.r = True
        elif self.o_radio.isChecked():
            self.pl = 'O'
            self.r = False

        for i in self.button_grid:
            for j in i:
                j.setText(' ')

    def dis(self):
        for i in self.button_grid:
            for j in i:
                j.setEnabled(False)

    def gaz(self):
        for i in self.button_grid:
            for j in i:
                j.setEnabled(True)

    def over(self):
        h = 0
        for i in self.button_grid:
            for j in i:
                if j.text() != ' ':
                    h += 1
        if h == 9:
            self.v = False
            return True
        return False

    def win(self):
        all = [[i.text() for i in self.button_grid[0]], [i.text() for i in self.button_grid[1]],
             [i.text() for i in self.button_grid[2]]]
        vertikal = []
        for i in range(3):
            prom = []
            for j in range(3):
                prom.append(self.button_grid[j][i].text())
            vertikal.append(prom)

        all.extend(vertikal)
        left = [self.button_grid[0][0].text()] + [self.button_grid[1][1].text()] + [self.button_grid[2][2].text()]
        right = [self.button_grid[0][2].text()] + [self.button_grid[1][1].text()] + [self.button_grid[2][0].text()]
        all.append(left)
        all.append(right)
        if ['X', 'X', 'X'] in all:
            return "X"
        elif ['O', 'O', 'O'] in all:
            return "O"
        return True
