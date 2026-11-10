import sqlite3
import sys

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtMultimedia import QSoundEffect, QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGraphicsDropShadowEffect


class History_boom(QWidget):
    def __init__(self, txt):
        super().__init__()
        self.txt = txt

        self.boom = QSoundEffect()
        self.boom.setSource(QUrl.fromLocalFile("door.wav"))
        self.boom.setVolume(0.5)

        self.boom_click = QSoundEffect()
        self.boom_click.setSource(QUrl.fromLocalFile("boom.wav"))
        self.boom_click.setVolume(1)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("☠ СТРАШНАЯ ИСТОРИЯ ☠")
        self.setFixedSize(700, 600)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.boom_click.play()

        if self.txt == 1:
            text = (
                "ОНА УСЛЫШАЛА СВОЙ ГОЛОС\n\n"
                "Девушка жила одна в старом доме у леса. Каждую ночь\n"
                "ровно в 3:33 она слышала, как кто-то тихо напевает\n"
                "колыбельную — её собственным голосом.\n\n"
                "Однажды она не выдержала и пошла на звук. В подвале,\n"
                "в самом тёмном углу, стояло зеркало. В отражении\n"
                "стояла ОНА. Но улыбалась — хотя сама девушка не\n"
                "улыбалась.\n\n"
                "Отражение подняло руку и медленно поманило её\n"
                "пальцем. А потом прошептало:\n\n"
                "«Теперь я выйду. А ты останешься тут. Навсегда.»\n\n"
                "С тех пор в том доме каждую ночь в 3:33 слышен\n"
                "женский крик. Но никто не может найти комнату,\n"
                "откуда он доносится..."
            )
            title = "☠ ИСТОРИЯ О ЗЕРКАЛЕ ☠"
            accent = "#ff1a1a"
        else:
            text = (
                "МАЛЬЧИК, КОТОРЫЙ ИГРАЛ С ТЕНЬЮ\n\n"
                "Маленький мальчик боялся темноты. Мама говорила:\n"
                "«Не бойся, в темноте никого нет». Но каждую ночь\n"
                "из-под его кровати вылезала тень — и садилась\n"
                "рядом. Она не трогала его. Просто смотрела.\n\n"
                "Однажды мальчик спросил шёпотом: «Кто ты?»\n"
                "И тень ответила его же голосом:\n\n"
                "«Я — это ты. Только тот, кого ты боишься больше\n"
                "всего. Я живу здесь, под кроватью, уже семь лет.\n"
                "С тех пор, как ты... не проснулся.»\n\n"
                "Мальчик закричал и включил свет. Тени не было.\n"
                "Но на полу лежала фотография — он сам, спящий\n"
                "в этой кровати. Только на снимке он не дышал.\n\n"
                "И с тех пор каждую ночь из детской слышен\n"
                "тихий детский плач. Но в комнате никого нет."
            )
            title = "☠ ИСТОРИЯ О ТЕНИ ☠"
            accent = "#cc0000"

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #000000, stop:0.5 #1a0000,
                                            stop:1 #3a0000);
                font-family: 'Georgia', serif;
                color: #d4b3b3;
            }
        """)

        self.title_label = QLabel(title, self)
        self.title_label.setGeometry(0, 15, 700, 60)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(f"""
            color: {accent};
            font-family: 'Georgia', serif;
            font-size: 28px;
            font-weight: bold;
            letter-spacing: 3px;
            background: transparent;
        """)
        title_shadow = QGraphicsDropShadowEffect()
        title_shadow.setBlurRadius(35)
        title_shadow.setColor(QColor(255, 0, 0, 220))
        title_shadow.setOffset(0, 0)
        self.title_label.setGraphicsEffect(title_shadow)

        self.drip_l = QLabel("🩸", self)
        self.drip_l.setGeometry(20, 5, 50, 70)
        self.drip_l.setStyleSheet("background: transparent; font-size: 36px;")
        self.drip_l.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.drip_r = QLabel("🩸", self)
        self.drip_r.setGeometry(630, 5, 50, 70)
        self.drip_r.setStyleSheet("background: transparent; font-size: 36px;")
        self.drip_r.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.history = QLabel(text, self)
        self.history.setGeometry(60, 85, 580, 410)
        self.history.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.history.setWordWrap(True)
        self.history.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(10, 0, 0, 200);
                border: 3px solid {accent};
                border-radius: 15px;
                color: #e6cccc;
                font-family: 'Georgia', serif;
                font-size: 15px;
                padding: 20px;
                line-height: 140%;
            }}
        """)
        history_shadow = QGraphicsDropShadowEffect()
        history_shadow.setBlurRadius(45)
        history_shadow.setColor(QColor(255, 0, 0, 140))
        history_shadow.setOffset(0, 0)
        self.history.setGraphicsEffect(history_shadow)

        self.btn = QPushButton("ЗАКРЫТЬ", self)
        self.btn.setGeometry(200, 510, 300, 70)
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #3a0000;
                color: {accent};
                font-size: 22px;
                font-weight: bold;
                font-family: 'Arial Black', sans-serif;
                border: 3px solid #8b0000;
                border-radius: 15px;
                letter-spacing: 3px;
            }}
            QPushButton:hover {{
                background-color: #8b0000;
                color: white;
                border: 3px solid {accent};
            }}
            QPushButton:pressed {{
                background-color: {accent};
                color: black;
            }}
        """)
        btn_shadow = QGraphicsDropShadowEffect()
        btn_shadow.setBlurRadius(30)
        btn_shadow.setColor(QColor(255, 0, 0, 180))
        btn_shadow.setOffset(0, 0)
        self.btn.setGraphicsEffect(btn_shadow)
        self.btn.clicked.connect(self.close)


class Horror(QWidget):
    def __init__(self, login):
        super().__init__()
        self.login = login

        self.imgs = [
            "one_close_door.jpg", "two_close_door.jpg", "three_close_door.jpg",
            "four_close_door.jpg", "five_close_door.jpg", "six_close_door.jpg",
            "seven_close_door.jpg", "eight_close_door.jpg", "nine_close_door.jpg",
            "ten_close_door.jpg", "eleven_close_door.jpg"
        ]

        self.count1 = 0
        self.count2 = 0
        self.count3 = 0

        self.door_open = QSoundEffect()
        self.door_open.setSource(QUrl.fromLocalFile("door.wav"))
        self.door_open.setVolume(0.5)

        self.scrim = QSoundEffect()
        self.scrim.setSource(QUrl.fromLocalFile("scrim.wav"))
        self.scrim.setVolume(0.5)

        self.woman = QSoundEffect()
        self.woman.setSource(QUrl.fromLocalFile("woman.wav"))
        self.woman.setVolume(0.5)

        self.cry = QSoundEffect()
        self.cry.setSource(QUrl.fromLocalFile("cry.wav"))
        self.cry.setVolume(0.5)

        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile("dead.mp3"))
        self.player.setLoops(QMediaPlayer.Loops.Infinite)
        self.audio_output.setVolume(0.3)

        self.r = QAudioOutput()
        self.heartbeat = QMediaPlayer()
        self.heartbeat.setAudioOutput(self.r)
        self.heartbeat.setSource(QUrl.fromLocalFile("heartbeat.mp3"))
        self.heartbeat.setLoops(QMediaPlayer.Loops.Infinite)
        self.r.setVolume(1)

        self.level = 0
        self.is_animating = False
        self.history_open = False

        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.next_frame1)

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.next_frame2)

        self.timer3 = QTimer(self)
        self.timer3.timeout.connect(self.next_frame3)

        con = sqlite3.connect("proect.db")
        cur = con.cursor()
        res = cur.execute("Select music from profile where login = ?", (self.login,)).fetchone()
        self.music = res[0]
        con.commit()
        con.close()

        self.initUI()

    def initUI(self):
        if self.music == 1:
            self.player.play()

        self.setWindowTitle("☠ ХОРРОР ☠")
        self.setFixedSize(1000, 900)
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
        )

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #000000, stop:0.7 #1a0000, stop:1 #3a0000);
                font-family: 'Georgia', serif;
                color: #8b0000;
            }
        """)

        self.title_label = QLabel("ВЫБЕРИ ДВЕРЬ", self)
        self.title_label.setGeometry(0, 20, 1000, 100)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            color: #8b0000;
            font-family: 'Georgia', serif;
            font-size: 64px;
            font-weight: bold;
            letter-spacing: 8px;
            background: transparent;
        """)
        title_shadow = QGraphicsDropShadowEffect()
        title_shadow.setBlurRadius(40)
        title_shadow.setColor(QColor(255, 0, 0, 200))
        title_shadow.setOffset(0, 0)
        self.title_label.setGraphicsEffect(title_shadow)

        self.drip_left = QPushButton("🩸", self)
        self.drip_left.setGeometry(30, 30, 80, 80)
        self.drip_left.setStyleSheet("""
            QPushButton { background-color: transparent; color: #8b0000; font-size: 50px; border: none; }
            QPushButton:hover { color: #ff0000; }
        """)
        self.drip_left.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.drip_left.setCursor(Qt.CursorShape.PointingHandCursor)
        self.drip_left.clicked.connect(self.blood1)

        self.drip_right = QPushButton("🩸", self)
        self.drip_right.setGeometry(930, 30, 80, 80)
        self.drip_right.setStyleSheet("""
            QPushButton { background-color: transparent; color: #8b0000; font-size: 50px; border: none; }
            QPushButton:hover { color: #ff0000; }
        """)
        self.drip_right.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.drip_right.setCursor(Qt.CursorShape.PointingHandCursor)
        self.drip_right.clicked.connect(self.blood2)

        drip_shadow_left = QGraphicsDropShadowEffect()
        drip_shadow_left.setBlurRadius(20)
        drip_shadow_left.setColor(QColor(255, 0, 0, 200))
        drip_shadow_left.setOffset(0, 0)
        self.drip_left.setGraphicsEffect(drip_shadow_left)

        drip_shadow_right = QGraphicsDropShadowEffect()
        drip_shadow_right.setBlurRadius(20)
        drip_shadow_right.setColor(QColor(255, 0, 0, 200))
        drip_shadow_right.setOffset(0, 0)
        self.drip_right.setGraphicsEffect(drip_shadow_right)

        self.lbl1 = QLabel(self)
        self.lbl1.move(50, 140)
        self.lbl1.resize(300, 450)
        self.lbl1.setStyleSheet("""
            border: 5px solid #4a0000;
            border-radius: 5px;
            background-color: #0a0000;
            padding: 4px;
        """)
        shadow1 = QGraphicsDropShadowEffect()
        shadow1.setBlurRadius(50)
        shadow1.setColor(QColor(255, 0, 0, 150))
        shadow1.setOffset(0, 0)
        self.lbl1.setGraphicsEffect(shadow1)
        self.lbl1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_door_image(self.lbl1, "zero_close_door.jpg")

        self.btn_open_one = QPushButton("ОТКРЫТЬ", self)
        self.btn_open_one.resize(200, 100)
        self.btn_open_one.move(100, 620)
        self.btn_open_one.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_open_one.setStyleSheet("""
            QPushButton {
                background-color: #3a0000;
                color: #ff3333;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Arial Black', sans-serif;
                border: 3px solid #8b0000;
                border-radius: 10px;
                letter-spacing: 2px;
            }
            QPushButton:hover { background-color: #8b0000; color: white; border: 3px solid #ff0000; }
            QPushButton:pressed { background-color: #ff0000; }
            QPushButton:disabled { background-color: #1a0000; color: #4a0000; border: 3px solid #2a0000; }
        """)
        self.btn_open_one.clicked.connect(self.open_one)

        self.lbl2 = QLabel(self)
        self.lbl2.move(350, 140)
        self.lbl2.resize(300, 450)
        self.lbl2.setStyleSheet("""
            border: 5px solid #4a0000;
            border-radius: 5px;
            background-color: #0a0000;
            padding: 4px;
        """)
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(50)
        shadow2.setColor(QColor(255, 0, 0, 150))
        shadow2.setOffset(0, 0)
        self.lbl2.setGraphicsEffect(shadow2)
        self.lbl2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_door_image(self.lbl2, "zero_close_door.jpg")

        self.btn_open_two = QPushButton("ОТКРЫТЬ", self)
        self.btn_open_two.resize(200, 100)
        self.btn_open_two.move(400, 620)
        self.btn_open_two.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_open_two.setStyleSheet(self.btn_open_one.styleSheet())
        self.btn_open_two.clicked.connect(self.open_two)

        self.lbl3 = QLabel(self)
        self.lbl3.move(650, 140)
        self.lbl3.resize(300, 450)
        self.lbl3.setStyleSheet("""
            border: 5px solid #4a0000;
            border-radius: 5px;
            background-color: #0a0000;
            padding: 4px;
        """)
        shadow3 = QGraphicsDropShadowEffect()
        shadow3.setBlurRadius(50)
        shadow3.setColor(QColor(255, 0, 0, 150))
        shadow3.setOffset(0, 0)
        self.lbl3.setGraphicsEffect(shadow3)
        self.lbl3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_door_image(self.lbl3, "zero_close_door.jpg")

        self.btn_open_three = QPushButton("ОТКРЫТЬ", self)
        self.btn_open_three.resize(200, 100)
        self.btn_open_three.move(700, 620)
        self.btn_open_three.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_open_three.setStyleSheet(self.btn_open_one.styleSheet())
        self.btn_open_three.clicked.connect(self.open_three)

        self.block()

    def set_door_image(self, label, image_path):
        pix = QPixmap(image_path)
        scaled = pix.scaled(
            300, 450,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        label.setPixmap(scaled)

    def block(self):
        busy = (
                self.is_animating
                or self.timer1.isActive()
                or self.timer2.isActive()
                or self.timer3.isActive()
        )
        for b in (self.btn_open_one, self.btn_open_two, self.btn_open_three):
            b.setEnabled(not busy)
        self.drip_left.setEnabled(not busy)
        self.drip_right.setEnabled(not busy)

    def blood1(self):
        if self.history_open:
            return
        self.history_open = True
        self.woman.play()
        self.prom = History_boom(1)
        self.prom.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.prom.destroyed.connect(self._on_history_closed)
        self.prom.show()

    def blood2(self):
        if self.history_open:
            return
        self.history_open = True
        self.cry.play()
        self.prom = History_boom(2)
        self.prom.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.prom.destroyed.connect(self._on_history_closed)
        self.prom.show()

    def _on_history_closed(self, *args):
        self.history_open = False

    def win(self):
        self.title_label.hide()
        self.btn_open_three.hide()
        self.btn_open_one.hide()
        self.btn_open_two.hide()
        self.lbl1.hide()
        self.lbl2.hide()
        self.lbl3.hide()
        self.drip_left.hide()
        self.drip_right.hide()
        if self.music == 1:
            self.heartbeat.play()
        self.player.stop()

        self.win_bg = QLabel(self)
        self.win_bg.setGeometry(0, 0, 1000, 900)
        self.win_bg.setStyleSheet("background-color: rgba(0, 0, 0, 220);")
        self.win_bg.show()

        self.win_frame = QLabel(self)
        self.win_frame.setGeometry(150, 250, 700, 400)
        self.win_frame.setStyleSheet("""
            QLabel {
                background-color: #1a0000;
                border: 4px solid #ff0000;
                border-radius: 20px;
                color: #ffcccc;
                font-family: 'Georgia', serif;
                font-size: 32px;
                font-weight: bold;
                padding: 30px;
            }
        """)
        self.win_frame.setText(
            "☠ ВЫ ВЫБРАЛИСЬ ☠\n\n"
            "Вы прошли все 5 испытаний\n"
            "и смогли покинуть этот\n"
            "проклятый дом.\n\n"
            "Но помните...\n"
            "Он всегда будет ждать вас."
        )
        self.win_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.win_frame.setWordWrap(True)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(60)
        shadow.setColor(QColor(255, 0, 0, 200))
        shadow.setOffset(0, 0)
        self.win_frame.setGraphicsEffect(shadow)

        self.win_frame.show()

        self.exit = QPushButton("Exit", self)
        self.exit.resize(300, 80)
        self.exit.move(350, 680)
        self.exit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.exit.setStyleSheet("""
            QPushButton {
                background-color: #3a0000;
                color: #ff3333;
                font-size: 22px;
                font-weight: bold;
                font-family: 'Arial Black', sans-serif;
                border: 3px solid #8b0000;
                border-radius: 15px;
                letter-spacing: 2px;
            }
            QPushButton:hover { background-color: #8b0000; color: white; border: 3px solid #ff0000; }
            QPushButton:pressed { background-color: #ff0000; }
        """)
        self.exit.clicked.connect(self.close_game)
        self.exit.show()

    def close_game(self):
        self.heartbeat.stop()
        self.player.stop()
        self.close()
        if self.level >= 5:
            con = sqlite3.connect("proect.db")
            cur = con.cursor()
            money = cur.execute("SELECT money FROM profile WHERE login = ?", (self.login,)).fetchone()
            cur.execute("UPDATE profile SET money=?, horror=? WHERE login=?", (money[0] + 30, 1, self.login))
            con.commit()
            con.close()
        from proect import Lobby
        self.lobby = Lobby(None, self.login)
        self.lobby.show()

    def open_one(self):
        self.count1 = 0
        self.is_animating = True
        self.timer1.start(220)
        self.block()
        if self.music == 1:
            self.door_open.play()
        self.level += 1

    def next_frame1(self):
        if self.count1 >= len(self.imgs):
            self.timer1.stop()
            self.is_animating = False
            self.block()
            if self.level != 4:
                self.scare_by("scare_one.jpg")
            else:
                self.set_door_image(self.lbl1, "zero_close_door.jpg")
                if self.level == 5:
                    self.win()
            return
        self.set_door_image(self.lbl1, self.imgs[self.count1])
        self.count1 += 1

    def open_two(self):
        self.count2 = 0
        self.is_animating = True
        self.block()
        if self.music == 1:
            self.door_open.play()
        self.level += 1
        self.timer2.start(220)

    def next_frame2(self):
        if self.count2 >= len(self.imgs):
            self.timer2.stop()
            self.is_animating = False
            self.block()
            if self.level != 2 and self.level != 3:
                self.scare_by("scare_two.jpg")
            else:
                self.set_door_image(self.lbl2, "zero_close_door.jpg")
                if self.level == 5:
                    self.win()
            return
        self.set_door_image(self.lbl2, self.imgs[self.count2])
        self.count2 += 1

    def open_three(self):
        self.count3 = 0
        self.is_animating = True
        self.block()
        if self.music == 1:
            self.door_open.play()
        self.level += 1
        self.timer3.start(220)

    def next_frame3(self):
        if self.count3 >= len(self.imgs):
            self.timer3.stop()
            self.is_animating = False
            self.block()
            if self.level != 1 and self.level != 5:
                self.scare_by("scare_three.jpg")
            else:
                self.set_door_image(self.lbl3, "zero_close_door.jpg")
                if self.level == 5:
                    self.win()
            return
        self.set_door_image(self.lbl3, self.imgs[self.count3])
        self.count3 += 1

    def scare_by(self, path):
        self.player.stop()
        if self.music == 1:
            self.heartbeat.play()
            self.scrim.play()
        self.image8 = QPixmap(path)
        self.lbl8 = QLabel(self)
        self.lbl8.move(0, 0)
        self.lbl8.resize(1000, 900)
        scaled = self.image8.scaled(
            1000, 900,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.lbl8.setPixmap(scaled)
        self.lbl8.setStyleSheet("background-color: black;")
        self.lbl8.show()
        self.lbl8.raise_()

        self.exit = QPushButton("Exit", self)
        self.exit.resize(300, 80)
        self.exit.move(0, 820)
        self.exit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.exit.setStyleSheet("""
            QPushButton {
                background-color: #3a0000;
                color: #ff3333;
                font-size: 22px;
                font-weight: bold;
                font-family: 'Arial Black', sans-serif;
                border: 3px solid #8b0000;
                border-radius: 15px;
                letter-spacing: 2px;
            }
            QPushButton:hover { background-color: #8b0000; color: white; border: 3px solid #ff0000; }
            QPushButton:pressed { background-color: #ff0000; }
        """)
        self.exit.clicked.connect(self.close_game)
        self.exit.show()

        self.is_animating = True
        self.block()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Horror("s")
    game.show()
    sys.exit(app.exec())
