import sys
import math
import random
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QColor, QPainter, QPolygonF, QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QColorDialog, QPushButton, QLabel, QInputDialog
from PySide6.scripts.qtpy2cpp_lib import qt


class Info(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Paint')

        self.label = QLabel(f'''SPACE - Поменять цвет кисти \n
                                R - Поднять кисть/Опустить кисть\n
                                S - Поменять Размер''', self)


class Paint(QWidget):
    def __init__(self):
        super().__init__()
        self.shapes = []
        self.flag = False
        self.size = 5
        self.initUI()
        self.color_change()

    def initUI(self):
        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowTitle('Paint')
        self.setMouseTracking(True)

        self.image = QLabel(self)
        self.image.move(25, 25)
        self.image.resize(350, 350)

        self.pixmap = QPixmap()

        scaled = self.pixmap.scaled(
            350, 350,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image.setPixmap(scaled)

        self.btn_info = QPushButton('Информация', self)
        self.btn_info.clicked.connect(self.info)
        self.btn_info.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.btn_save = QPushButton('Сохранить', self)
        self.btn_save.clicked.connect(self.save)
        self.btn_save.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def info(self):
        self.info = Info()
        self.info.show()

    def save(self):
        pass

    def paintEvent(self, event):
        if self.flag:
            qp = QPainter()
            qp.begin(self)

            for shape in self.shapes:
                shape_type, cx, cy, size, color = shape
                qp.setBrush(QColor.fromString(color))
                qp.setPen(Qt.PenStyle.NoPen)

                if shape_type == 'square':
                    rect = QRectF(cx - size / 2, cy - size / 2, size, size)
                    qp.drawRect(rect)
            qp.end()

    def mouseMoveEvent(self, event):
        if self.flag:
            self.shapes.append(('square', event.pos().x(), event.pos().y(), self.size, self.color))

            self.update()

    def color_change(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()

    def up_down(self):
        if self.flag:
            self.flag = False
        else:
            self.flag = True

    def size_change(self):
        size, ok = QInputDialog.getText(
            self,
            'Знакомство',
            'Сколько прибавить к размеру или убавить на сколько?\n'
            '(5 или -5 Например)')
        if ok:
            try:
                self.size += int(size)
            except Exception as e:
                print(e)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.color_change()
        elif event.key() == Qt.Key.Key_R:
            self.up_down()
        elif event.key() == Qt.Key.Key_S:
            self.size_change()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Paint()
    ex.show()
    sys.exit(app.exec())
