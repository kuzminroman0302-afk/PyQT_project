import sys
import math
import random
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QColor, QPainter, QPolygonF
from PyQt6.QtWidgets import QWidget, QApplication, QColorDialog


class Paint(QWidget):
    def __init__(self):
        super().__init__()
        self.shapes = []
        self.shape = []
        self.idx = -1
        self.color_change()
        self.initUI()


    def initUI(self):
        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowTitle('Paint')
        self.setMouseTracking(True)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        try:

            self.shapes[self.idx] = self.shape
            for shape in self.shapes[self.idx]:
                shape_type, cx, cy, size, color = shape
                qp.setBrush(QColor.fromString(color))
                qp.setPen(Qt.PenStyle.NoPen)

                if shape_type == 'square':
                    rect = QRectF(cx - size / 2, cy - size / 2, size, size)
                    qp.drawRect(rect)
            qp.end()
        except Exception as e:
            print(self.shapes[self.idx])
            print(e)


    def mouseMoveEvent(self, event):
        size = random.randint(20, 100)
        self.shape.append(('square', event.pos().x(), event.pos().y(), size, self.color))

        self.update()

    def color_change(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.shape = []
            self.idx += 1
            self.shapes.append(self.shape)
            self.color = color.name()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.color_change()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Paint()
    ex.show()
    sys.exit(app.exec())
