import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.number_buttons = []
        self.prim = ''
        self.t = True
        self.mena = False
        self.eror = False
        self.zn = False
        self.ev = False
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 600)
        self.setWindowTitle('Калькулятор')

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                color: black;
            }
            QPushButton {
                background-color: #e0e0e0;
                color: black;
                border: 1px solid #b0b0b0;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid #b0b0b0;
                border-radius: 5px;
                padding: 5px;
                font-size: 30px;
            }
        """)

        self.float_point_button = QPushButton(self)
        self.float_point_button.resize(125, 90)
        self.float_point_button.move(0, 510)
        self.float_point_button.setText(".")
        self.float_point_button.clicked.connect(self.hello)

        font = QFont()
        font.setPointSize(50)
        font.setBold(True)
        self.float_point_button.setFont(font)

        self.plus_minus_button = QPushButton(self)
        self.plus_minus_button.resize(125, 90)
        self.plus_minus_button.move(125, 510)
        self.plus_minus_button.setText("±")
        self.plus_minus_button.clicked.connect(self.men)
        self.plus_minus_button.setFont(font)

        self.equals_button = QPushButton(self)
        self.equals_button.resize(250, 90)
        self.equals_button.move(250, 510)
        self.equals_button.setText("=")
        self.equals_button.clicked.connect(self.ravn)
        self.equals_button.setFont(font)

        self.clear_button = QPushButton(self)
        self.clear_button.resize(125, 90)
        self.clear_button.move(0, 420)
        self.clear_button.setText("C")
        self.clear_button.clicked.connect(self.clear)
        self.clear_button.setFont(font)

        self.btn0 = QPushButton(self)
        self.btn0.resize(125, 90)
        self.btn0.move(125, 420)
        self.btn0.setText("0")
        self.btn0.clicked.connect(self.hello)
        self.number_buttons.append(self.btn0)
        self.btn0.setFont(font)

        self.clear_entry_button = QPushButton(self)
        self.clear_entry_button.resize(125, 90)
        self.clear_entry_button.move(250, 420)
        self.clear_entry_button.setText("CE")
        self.clear_entry_button.clicked.connect(self.clear_entry)
        self.clear_entry_button.setFont(font)

        self.add_button = QPushButton(self)
        self.add_button.resize(125, 90)
        self.add_button.move(375, 420)
        self.add_button.setText("+")
        self.add_button.clicked.connect(self.hello)
        self.add_button.setFont(font)

        x = 0
        y = 330
        for i in range(1, 10):
            btn = QPushButton(self)
            btn.resize(125, 90)
            btn.move(x, y)
            btn.setText(str(i))
            btn.clicked.connect(self.hello)
            btn.setFont(font)
            self.number_buttons.append(btn)

            x += 125
            if i % 3 == 0:
                y -= 90
                x = 0

        self.substract_button = QPushButton(self)
        self.substract_button.resize(125, 90)
        self.substract_button.move(375, 330)
        self.substract_button.setText("-")
        self.substract_button.clicked.connect(self.hello)
        self.substract_button.setFont(font)

        self.multiply_button = QPushButton(self)
        self.multiply_button.resize(125, 90)
        self.multiply_button.move(375, 240)
        self.multiply_button.setText("*")
        self.multiply_button.clicked.connect(self.hello)
        self.multiply_button.setFont(font)

        self.divide_button = QPushButton(self)
        self.divide_button.resize(125, 90)
        self.divide_button.move(375, 150)
        self.divide_button.setText("/")
        self.divide_button.clicked.connect(self.hello)
        self.divide_button.setFont(font)

        self.main_label = QLineEdit("0", self)
        self.main_label.resize(500, 100)
        self.main_label.move(0, 50)

        self.secondary_label = QLineEdit(self)
        self.secondary_label.resize(500, 50)
        self.secondary_label.move(0, 0)

    def hello(self):
        n = self.sender().text()

        if n not in "+-/*.":
            self.zn = False
        if self.zn:
            return
        if self.eror and n in "+-/*.":
            return

        if n == "0":
            if self.t or self.main_label.text() == "0":
                self.t = False
                return

        if n == "." and self.main_label.text() == "0":
            self.prim = "0."
            self.main_label.setText("0.")
            self.t = False
            return

        if self.t:
            if not self.mena:
                self.main_label.setText('')
                if self.ev:
                    self.prim = ''
                    self.ev = False
                self.t = False
                self.eror = False

        if n == "." and self.main_label.text() == "":
            self.prim = "0."
            self.main_label.setText("0.")
            self.t = False
            return

        if n in "-*+/":
            if self.main_label.text() == "":
                self.main_label.setText('0')
                self.prim += "0"
            if self.mena:
                self.prim += ")"
                self.main_label.setText(self.main_label.text() + ")")
                self.mena = False
            self.secondary_label.setText(self.main_label.text() + " " + n)
            self.prim += n
            self.t = True
            self.zn = True
            self.ev = False
            return

        if (n == "." and self.main_label.text() == "") or (n == "." and "." in self.main_label.text()):
            return

        if self.main_label.text() == "0" and n not in "0.":
            self.main_label.setText(n)
            self.prim = n
            return

        self.prim += n
        self.main_label.setText(self.main_label.text() + n)

    def ravn(self):
        self.secondary_label.setText('')
        if self.mena:
            self.prim += ")"
            self.main_label.setText(self.main_label.text() + ")")
            self.mena = False
        try:
            if len(str(eval(self.prim))) > 11 and str(eval(self.prim))[-2:] == ".0":
                self.main_label.setText(f"{int(eval(self.prim)):.2e}")
            elif len(str(eval(self.prim))) > 11:
                self.main_label.setText(f"{eval(self.prim):.2e}")
            else:
                if str(eval(self.prim))[-2:] == ".0":
                    self.main_label.setText(str(int(eval(self.prim))))
                    self.prim = str(int(eval(self.prim)))
                else:
                    self.main_label.setText(str(eval(self.prim)))
                    self.prim = str(eval(self.prim))
        except ZeroDivisionError:
            self.main_label.setText('ОШИБКА')
            self.prim = ''
            self.t = True
            self.eror = True
            self.ev = True

    def clear(self):
        self.main_label.setText('0')
        self.secondary_label.setText('')
        self.prim = ''
        self.t = True

    def clear_entry(self):
        self.main_label.setText('0')
        n = 0
        p = False
        for i in self.prim:
            n += 1
            if i in "-*/+":
                p = True
                break
        if p:
            self.prim = self.prim[:n]
        else:
            self.prim = ''
        self.t = True

    def men(self):
        if self.mena:
            return
        if self.main_label.text() == '0':
            return
        if self.main_label.text()[0] == "0":
            for i in self.prim:
                if i in "123456789":
                    pass
            else:
                return
        if not self.prim[-1].isdigit():
            self.main_label.setText('(-')
            self.prim += "(-"
            self.mena = True
            return
        if self.secondary_label.text() != '':
            self.mena = True
            c = 0
            for i, j in enumerate(self.prim):
                if not j.isdigit():
                    c = i
            self.main_label.setText("(-" + self.main_label.text())
            self.prim = self.prim[:c + 1] + "(-" + self.prim[c + 1:]

        else:
            self.main_label.setText("-" + self.main_label.text())
            self.prim = "-" + self.prim

    def zero(self):
        for i in self.prim:
            if i in "123456789":
                return True
        return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calculator()
    ex.show()
    sys.exit(app.exec())