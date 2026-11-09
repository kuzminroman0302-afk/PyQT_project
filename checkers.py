import sys
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton
from PyQt6.QtCore import Qt


class checkers(QWidget):
    def __init__(self, login):
        super().__init__()
        self.login = login
        self.setWindowTitle("Шашки")
        self.setFixedSize(800, 800)

        self.board = [[0 for _ in range(8)] for _ in range(8)]

        for y in range(8):
            for x in range(8):
                if (x + y) % 2 == 1:
                    if y < 3:
                        self.board[y][x] = 1
                    elif y > 4:
                        self.board[y][x] = 2

        self.selected = None
        self.buttons = []

        self.initUI()

    def initUI(self):
        for y in range(8):
            row = []
            for x in range(8):
                btn = QPushButton(self)
                btn.setGeometry(x * 100, y * 100, 100, 100)
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                btn.clicked.connect(lambda checked=False, cx=x, cy=y: self.click(cx, cy))
                row.append(btn)
            self.buttons.append(row)

        self.draw_board()

    def draw_board(self):
        for y in range(8):
            for x in range(8):
                btn = self.buttons[y][x]

                if (x + y) % 2 == 0:
                    base_color = "tan"
                else:
                    base_color = "saddlebrown"

                if self.selected:
                    sx, sy = self.selected
                    if self.is_valid_move(sx, sy, x, y):
                        base_color = "limegreen"

                if self.selected == (x, y):
                    base_color = "limegreen"

                piece = self.board[y][x]

                if piece == 1:
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {base_color};
                            border-radius: 50px;
                            background: qradialgradient(cx:0.4, cy:0.4, radius:0.6, fx:0.4, fy:0.4, 
                                                        stop:0 red, stop:1 darkred);
                        }}
                    """)
                elif piece == 2:
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {base_color};
                            border-radius: 50px;
                            background: qradialgradient(cx:0.4, cy:0.4, radius:0.6, fx:0.4, fy:0.4, 
                                                        stop:0 white, stop:1 gray);
                        }}
                    """)
                else:
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {base_color};
                            border: none;
                        }}
                    """)

    def click(self, x, y):
        if self.selected:
            sx, sy = self.selected
            if (sx, sy) == (x, y):
                self.selected = None
                self.draw_board()
                return

            if self.is_valid_move(sx, sy, x, y):
                self.board[y][x] = self.board[sy][sx]
                self.board[sy][sx] = 0
                self.selected = None
                self.draw_board()
                return

        if self.board[y][x] != 0:
            self.selected = (x, y)
            self.draw_board()

    def is_valid_move(self, sx, sy, ex, ey):
        piece = self.board[sy][sx]
        dx = abs(ex - sx)
        dy = abs(ey - sy)

        if dx != 1 or dy != 1:
            return False

        if self.board[ey][ex] != 0:
            return False

        if piece == 1 and ey < sy:
            return False
        if piece == 2 and ey > sy:
            return False

        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = checkers("ads")
    game.show()
    sys.exit(app.exec())