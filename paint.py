import sys
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QWidget, QApplication, QColorDialog, QPushButton,
    QLabel, QInputDialog, QFileDialog,
    QHBoxLayout, QVBoxLayout, QFrame, QMainWindow
)


APP_STYLE = """
QMainWindow, QWidget {
    background-color: #1e1f22;
    color: #e6e6e6;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 13px;
}

QToolButton, QPushButton {
    background-color: #2b2d31;
    color: #e6e6e6;
    border: 1px solid #3a3d42;
    border-radius: 8px;
    padding: 8px 14px;
    min-height: 22px;
}
QToolButton:hover, QPushButton:hover {
    background-color: #3a3d42;
    border-color: #5865f2;
}
QToolButton:pressed, QPushButton:pressed {
    background-color: #5865f2;
}
QToolButton:checked {
    background-color: #5865f2;
    border-color: #5865f2;
}

QLabel#status {
    background-color: #2b2d31;
    border: 1px solid #3a3d42;
    border-radius: 6px;
    padding: 4px 10px;
}

QFrame#toolbar {
    background-color: #2b2d31;
    border: 1px solid #3a3d42;
    border-radius: 12px;
}

QFrame#canvasFrame {
    background-color: #2b2d31;
    border: 1px solid #3a3d42;
    border-radius: 12px;
}
"""


class Info(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 420, 260)
        self.setWindowTitle('Информация')
        self.setStyleSheet(APP_STYLE)

        label = QLabel(
            '<h3 style="color:#5865f2; margin:0 0 8px 0;">Горячие клавиши</h3>'
            '<table cellspacing="6">'
            '<tr><td><b>SPACE</b></td><td>— сменить цвет кисти</td></tr>'
            '<tr><td><b>R</b></td><td>— поднять / опустить кисть</td></tr>'
            '<tr><td><b>S</b></td><td>— изменить размер кисти</td></tr>'
            '<tr><td><b>C</b></td><td>— очистить холст</td></tr>'
            '</table>'
            '<p style="color:#9aa0a6; margin-top:10px;">',
            self
        )
        label.setWordWrap(True)
        label.setGeometry(15, 15, 390, 230)


class Paint(QMainWindow):
    def __init__(self, login):
        super().__init__()
        self.login = login
        self.shapes = []
        self.flag = False
        self.size = 5
        self.color = '#fffff'
        self.background = QPixmap()

        self.initUI()
        self.update_status()

    def initUI(self):
        self.setWindowTitle('Paint')
        self.resize(1100, 760)
        self.setStyleSheet(APP_STYLE)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        toolbar = QFrame()
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(12, 10, 12, 10)
        tb_layout.setSpacing(8)

        self.btn_color = QPushButton('🎨  Цвет')
        self.btn_color.clicked.connect(self.color_change)
        self.btn_color.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.btn_size = QPushButton('📏  Размер')
        self.btn_size.clicked.connect(self.size_change)
        self.btn_size.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.btn_brush = QPushButton('✏️  Кисть: поднята')
        self.btn_brush.clicked.connect(self.up_down)
        self.btn_brush.setCheckable(True)
        self.btn_brush.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_brush.setChecked(False)

        self.btn_open = QPushButton('📂  Открыть')
        self.btn_open.clicked.connect(self.open_file)
        self.btn_open.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.btn_save = QPushButton('💾  Сохранить')
        self.btn_save.clicked.connect(self.save)
        self.btn_save.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.btn_clear = QPushButton('🗑  Очистить')
        self.btn_clear.clicked.connect(self.clear)
        self.btn_clear.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.btn_exit = QPushButton('Lobby')
        self.btn_exit.clicked.connect(self.exit)
        self.btn_exit.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.btn_info = QPushButton('❓  Информация')
        self.btn_info.clicked.connect(self.info)
        self.btn_info.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        for b in (self.btn_color, self.btn_size, self.btn_brush,
                  self.btn_open, self.btn_save, self.btn_clear, self.btn_exit):
            tb_layout.addWidget(b)
        tb_layout.addStretch()
        tb_layout.addWidget(self.btn_info)

        canvas_frame = QFrame()
        canvas_frame.setObjectName('canvasFrame')
        cf_layout = QVBoxLayout(canvas_frame)
        cf_layout.setContentsMargins(8, 8, 8, 8)

        self.canvas = QWidget()
        self.canvas.setMinimumSize(400, 300)
        self.canvas.setMouseTracking(True)
        self.canvas.setStyleSheet("""
            background-color: white;
            border-radius: 8px;
        """)
        self.canvas.paintEvent = self.paint_event
        self.canvas.mouseMoveEvent = self.mouse_move_event

        cf_layout.addWidget(self.canvas)

        status_bar = QHBoxLayout()
        self.lbl_mode = QLabel('Режим: кисть поднята')
        self.lbl_mode.setObjectName('status')
        self.lbl_size = QLabel(f'Размер: {self.size} px')
        self.lbl_size.setObjectName('status')
        self.lbl_color = QLabel('Цвет: #fffff')
        self.lbl_color.setObjectName('status')

        status_bar.addWidget(self.lbl_mode)
        status_bar.addWidget(self.lbl_size)
        status_bar.addWidget(self.lbl_color)
        status_bar.addStretch()

        root.addWidget(toolbar)
        root.addWidget(canvas_frame, 1)
        root.addLayout(status_bar)

    def exit(self):
        from proect import Lobby
        self.close()
        self.exit1 = Lobby(None, self.login)
        self.exit1.show()

    def paint_event(self, event):
        qp = QPainter(self.canvas)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        qp.fillRect(self.canvas.rect(), Qt.GlobalColor.white)
        if not self.background.isNull():
            qp.drawPixmap(0, 0, self.background)
        self.draw_shapes(qp)
        qp.end()

    def mouse_move_event(self, event):
        if self.flag:
            self.shapes.append(
                ('square', event.pos().x(), event.pos().y(),
                 self.size, self.color)
            )
            self.canvas.update()

    def update_status(self):
        self.lbl_mode.setText('Режим: кисть опущена' if self.flag else 'Режим: кисть поднята')
        self.lbl_size.setText(f'Размер: {self.size} px')
        self.lbl_color.setText(f'Цвет: {self.color}')
        pix = QPixmap(14, 14)
        pix.fill(QColor(self.color))
        self.lbl_color.setPixmap(pix)
        self.lbl_color.setText(f'  Цвет: {self.color}')

        self.btn_brush.setText('✏️  Кисть: опущена' if self.flag else '✏️  Кисть: поднята')

    def info(self):
        self.info_win = Info()
        self.info_win.show()

    def clear(self):
        self.shapes.clear()
        self.background = QPixmap()
        self.canvas.update()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Открыть изображение', '',
            'Изображения (*.png *.jpg *.jpeg *.bmp);;Все файлы (*)'
        )
        if not file_path:
            return
        pix = QPixmap(file_path)
        if pix.isNull():
            return
        self.background = pix.scaled(
            self.canvas.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.shapes.clear()
        self.canvas.update()

    def save(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Сохранить рисунок', 'рисунок.png',
            'PNG (*.png);;JPEG (*.jpg);;BMP (*.bmp)'
        )
        if not file_path:
            return
        pixmap = QPixmap(self.canvas.size())
        pixmap.fill(Qt.GlobalColor.white)
        painter = QPainter(pixmap)
        if not self.background.isNull():
            painter.drawPixmap(0, 0, self.background)
        self.draw_shapes(painter)
        painter.end()
        pixmap.save(file_path)

    def draw_shapes(self, painter: QPainter):
        for shape_type, cx, cy, size, color in self.shapes:
            painter.setBrush(QColor.fromString(color))
            painter.setPen(Qt.PenStyle.NoPen)
            if shape_type == 'square':
                rect = QRectF(cx - size / 2, cy - size / 2, size, size)
                painter.drawRect(rect)

    def color_change(self):
        color = QColorDialog.getColor(QColor(self.color), self, 'Цвет кисти')
        if color.isValid():
            self.color = color.name()
            self.update_status()

    def up_down(self):
        self.flag = not self.flag
        self.btn_brush.setChecked(self.flag)
        self.update_status()

    def size_change(self):
        size, ok = QInputDialog.getText(
            self, 'Размер кисти',
            'На сколько изменить размер?\n(например 5 или -5)'
        )
        if ok:
            try:
                self.size = max(1, self.size + int(size))
                self.update_status()
            except Exception as e:
                print(e)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.color_change()
        elif event.key() == Qt.Key.Key_R:
            self.up_down()
        elif event.key() == Qt.Key.Key_S:
            self.size_change()
        elif event.key() == Qt.Key.Key_C:
            self.clear()
        else:
            super().keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('abc')
    ex = Paint()
    ex.show()
    sys.exit(app.exec())