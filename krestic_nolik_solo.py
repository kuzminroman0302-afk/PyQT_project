import sys

from PyQt6.QtWidgets import QApplication, QWidget, QRadioButton, QPushButton, QLabel, QLineEdit, QLCDNumber

class TicTacToe_friend(QWidget):
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
                self.x1 = QPushButton('', self)
                self.x1.resize(200, 200)
                self.x1.move(x, y)
                self.x1.clicked.connect(lambda h, i=i, j=j: self.hello(i, j))
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
            QPushButton:hover   { background-color: #ffe08a; }
            QPushButton:pressed { background-color: #e6b94a; }
        """)

    def exit(self):
        from proect import Lobby
        self.close()
        self.lobby = Lobby(None, self.login)
        self.lobby.show()


    def hello(self, i, j):
        btn = self.button_grid[i][j]
        if btn.text() != '' or self.v is False:
            return

        btn.setText(self.pl)
        if self.pl == "X":
            self.pl = 'O'
        else:
            self.pl = 'X'
        if self.win() is not True:
            self.dis()
            if self.win() == "X":
                self.result.setText("Выиграл X!")
                self.result.show()
                self.v = False
            elif self.win() == "O":
                self.result.setText("Выиграл O!")
                self.result.show()
                self.v = False
        if self.over():
            self.dis()
            self.result.setText("Ничья!")
            self.result.show()
            return

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
                j.setText('')

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
                if j.text() != '':
                    h += 1
        if h == 9:
            self.v = False
            return True
        return False

    def win(self):
        k = [[i.text() for i in self.button_grid[0]], [i.text() for i in self.button_grid[1]],
             [i.text() for i in self.button_grid[2]]]
        f = []
        for i in range(3):
            d = []
            for j in range(3):
                d.append(self.button_grid[j][i].text())
            f.append(d)

        k.extend(f)
        b = [self.button_grid[0][0].text()] + [self.button_grid[1][1].text()] + [self.button_grid[2][2].text()]
        c = [self.button_grid[0][2].text()] + [self.button_grid[1][1].text()] + [self.button_grid[2][0].text()]
        k.append(b)
        k.append(c)
        if ['X', 'X', 'X'] in k:
            return "X"
        elif ['O', 'O', 'O'] in k:
            return "O"
        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TicTacToe_friend()
    ex.show()
    sys.exit(app.exec())
