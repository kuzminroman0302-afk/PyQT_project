import random
import sqlite3
import sys

from PyQt6.QtCore import Qt, QTimer, QPointF, QUrl
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen
from PyQt6.QtMultimedia import QSoundEffect, QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout


class FlappyBird(QWidget):
    def __init__(self, login):
        super().__init__()
        self.login = login
        self.setWindowTitle("🐦 Flappy Bird")
        self.setFixedSize(800, 900)

        self.setStyleSheet("background-color: #4ec0ca;")

        self.gravity = 0.6
        self.jump_strength = -10
        self.pipe_width = 90
        self.pipe_gap = 200
        self.pipe_speed = 5
        self.ground_height = 100
        self.scores = []

        self.bird_x = 150
        self.bird_y = 400
        self.bird_radius = 25
        self.bird_velocity = 0

        self.pipes = []
        self.score = 0
        self.game_over = False
        self.started = False

        self.over = QSoundEffect()
        self.over.setSource(QUrl.fromLocalFile("over.wav"))
        self.over.setVolume(0.3)

        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile("bird.mp3"))
        self.player.setLoops(QMediaPlayer.Loops.Infinite)
        self.audio_output.setVolume(0.05)

        self.buy_click = QSoundEffect()
        self.buy_click.setSource(QUrl.fromLocalFile("buy.wav"))
        self.buy_click.setVolume(0.05)

        self.con = sqlite3.connect("proect.db")
        self.cur = self.con.cursor()
        self.res = self.cur.execute("Select music, record_flappy_bird from profile where login = ?",
                                    (self.login,)).fetchone()
        self.music, self.record_flappy_bird = self.res

        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)

    def initUI(self):
        if self.music == 1:
            self.player.play()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.ground_btn = QPushButton(self)
        self.ground_btn.setGeometry(0, 800, 800, 100)
        self.ground_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ground_btn.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ground_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ded895, stop:1 #c4bd74);
                border: none;
                border-top: 5px solid #d1c85a;
                color: #555;
                font-size: 24px;
                font-weight: bold;
            }
        """)

        self.btn_exit = QPushButton("Lobby", self)
        self.btn_exit.setGeometry(640, 20, 130, 50)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background-color: #dc2626; color: white; 
                border-radius: 10px; font-size: 18px; font-weight: bold;
                border: 2px solid #991b1b;
            }
            QPushButton:hover { background-color: #ef4444; }
        """)
        self.btn_exit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_exit.clicked.connect(self.lobby)

        self.score_label = QLabel("0", self)
        self.score_label.setGeometry(0, 50, 800, 100)
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setStyleSheet("""
            color: white; font-size: 60px; font-weight: bold; font-family: Arial;
            background: transparent;
        """)
        self.score_label.raise_()

        self.start_label = QLabel("Нажмите ПРОБЕЛ\nчтобы начать игру", self)
        self.start_label.setGeometry(200, 350, 400, 150)
        self.start_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_label.setStyleSheet("""
            color: white; font-size: 30px; font-weight: bold; 
            background-color: rgba(0, 0, 0, 150); border-radius: 15px;
        """)
        self.start_label.show()
        self.start_label.raise_()

        self.game_over_label = QLabel(self)
        self.game_over_label.setGeometry(0, 0, 800, 900)
        self.game_over_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.game_over_label.setStyleSheet("""
            color: white; background-color: rgba(0, 0, 0, 180);
            font-size: 30px; font-weight: bold;
        """)

        over_layout = QVBoxLayout(self.game_over_label)
        over_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        over_layout.setSpacing(20)

        self.go_title = QLabel("GAME OVER")
        self.go_title.setStyleSheet("color: #ef4444; font-size: 60px; font-weight: bold; background: transparent;")
        self.go_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.go_score = QLabel("Ваш счет: 0")
        self.go_score.setStyleSheet("color: white; font-size: 30px; background: transparent;")
        self.go_score.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.go_record = QLabel(f"Ваш рекорд: {self.record_flappy_bird}")
        self.go_record.setStyleSheet("color: white; font-size: 30px; background: transparent;")
        self.go_record.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.go_restart = QLabel("Нажмите ПРОБЕЛ для рестарта")
        self.go_restart.setStyleSheet("color: white; font-size: 24px; background: transparent;")
        self.go_restart.setAlignment(Qt.AlignmentFlag.AlignCenter)

        over_layout.addWidget(self.go_title)
        over_layout.addWidget(self.go_score)
        over_layout.addWidget(self.go_record)
        over_layout.addWidget(self.go_restart)

        self.game_over_label.hide()

        self.setFocus()

    def true_false(self):
        for i in self.scores:
            if i >= 20:
                return True
        return False

    def lobby(self):
        if self.true_false():
            self.buy_click.play()
            con = sqlite3.connect("proect.db")
            cur = con.cursor()
            money, ex, level = cur.execute("SELECT money, ex, level FROM profile WHERE login=?",
                                           (self.login,)).fetchone()
            if level == 9:
                level += 1
            cur.execute("UPDATE profile SET money=?, ex=?, level=? WHERE login=?",
                        (money + 40, ex + 35, level, self.login))
            con.commit()
            con.close()
        self.con.commit()
        self.con.close()
        self.player.stop()
        from proect import Lobby
        self.live = Lobby(None, self.login)
        self.live.show()
        self.close()

    def jump(self):
        if self.game_over:
            self.reset_game()
        elif not self.started:
            self.started = True
            self.start_label.hide()
            self.bird_velocity = self.jump_strength
        else:
            self.bird_velocity = self.jump_strength
        self.setFocus()

    def reset_game(self):
        self.bird_y = 400
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.score_label.setText("0")
        self.game_over = False
        self.started = False

        self.game_over_label.hide()
        self.start_label.show()

        self.timer.start(16)
        self.setFocus()
        self.update()

    def spawn_pipe(self):
        top_h = random.randint(100, 500)
        self.pipes.append({
            'x': 800,
            'top_h': top_h,
            'scored': False
        })

    def update_game(self):
        if self.game_over or not self.started:
            return

        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity

        if self.bird_y > 800 - self.bird_radius * 2 or self.bird_y < 0:
            self.end_game()

        if len(self.pipes) == 0 or self.pipes[-1]['x'] < 500:
            self.spawn_pipe()

        for pipe in self.pipes:
            pipe['x'] -= self.pipe_speed

            if not pipe['scored'] and pipe['x'] + self.pipe_width < self.bird_x:
                pipe['scored'] = True
                self.score += 1
                self.score_label.setText(str(self.score))

            if pipe['x'] < self.bird_x + self.bird_radius and pipe[
                'x'] + self.pipe_width > self.bird_x - self.bird_radius:
                if self.bird_y - self.bird_radius < pipe['top_h']:
                    self.end_game()
                if self.bird_y + self.bird_radius > pipe['top_h'] + self.pipe_gap:
                    self.end_game()

        self.pipes = [p for p in self.pipes if p['x'] > -self.pipe_width]
        self.update()

    def end_game(self):
        self.scores.append(self.score)
        if self.music == 1:
            self.over.play()
        self.game_over = True
        self.timer.stop()
        self.go_score.setText(f"Ваш счет: {self.score}")
        if int(self.record_flappy_bird) < self.score:
            self.record_flappy_bird = self.score
        self.cur.execute("UPDATE profile SET record_flappy_bird=? WHERE login = ?",
                         (self.record_flappy_bird, self.login))
        self.con.commit()
        self.go_record.setText(f"Ваш рекорд: {self.record_flappy_bird}")
        self.game_over_label.show()
        self.game_over_label.raise_()
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.jump()
        elif event.key() == Qt.Key.Key_Escape:
            self.close()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)

        for pipe in self.pipes:
            qp.setBrush(QBrush(QColor("#74bf2e")))
            qp.setPen(QPen(QColor("#558c22"), 3))
            qp.drawRect(int(pipe['x']), 0, self.pipe_width, pipe['top_h'])

            qp.setBrush(QBrush(QColor("#8ed63b")))
            qp.drawRect(int(pipe['x'] - 5), pipe['top_h'] - 30, self.pipe_width + 10, 30)

            bottom_y = pipe['top_h'] + self.pipe_gap
            bottom_h = 800 - bottom_y
            qp.setBrush(QBrush(QColor("#74bf2e")))
            qp.setPen(QPen(QColor("#558c22"), 3))
            qp.drawRect(int(pipe['x']), bottom_y, self.pipe_width, bottom_h)

            qp.setBrush(QBrush(QColor("#8ed63b")))
            qp.drawRect(int(pipe['x'] - 5), bottom_y, self.pipe_width + 10, 30)

        qp.setBrush(QBrush(QColor("#f7d51d")))
        qp.setPen(QPen(QColor("#000000"), 2))
        qp.drawEllipse(QPointF(self.bird_x, self.bird_y), self.bird_radius, self.bird_radius)

        qp.setBrush(QBrush(QColor("#ffffff")))
        qp.drawEllipse(QPointF(self.bird_x + 10, self.bird_y - 10), 8, 8)
        qp.setBrush(QBrush(QColor("#000000")))
        qp.drawEllipse(QPointF(self.bird_x + 12, self.bird_y - 10), 3, 3)

        qp.setBrush(QBrush(QColor("#f77e1d")))
        qp.setPen(Qt.PenStyle.NoPen)
        qp.drawPolygon(
            QPointF(self.bird_x + 20, self.bird_y),
            QPointF(self.bird_x + 40, self.bird_y + 5),
            QPointF(self.bird_x + 20, self.bird_y + 15)
        )

        qp.setBrush(QBrush(QColor("#e6c514")))
        qp.setPen(QPen(QColor("#000000"), 1))
        qp.drawEllipse(QPointF(self.bird_x - 10, self.bird_y), 12, 8)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = FlappyBird("s")
    game.show()
    sys.exit(app.exec())
