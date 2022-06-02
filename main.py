import os
import sys
import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class DesktopPet(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)
        self.init()
        self.initPall()
        self.initPetImage()
        self.petNormalAction()


    def init(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()

    def initPall(self):
        icons = os.path.join('favicon.ico')
        showing = QAction('显示', self, triggered=self.showwin)
        showing.setIcon(QIcon(os.path.join('ico/sun.ico')))
        quit_action = QAction('退出', self, triggered=self.quit)
        quit_action.setIcon(QIcon(os.path.join('ico/star.ico')))
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(showing)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icons))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()

    def initPetImage(self):
        self.talkLabel = QLabel(self)
        self.talkLabel.setStyleSheet("font:15pt 'STCaiyun';border-width: 1px;color:blue;")
        self.image = QLabel(self)
        self.movie = QMovie("normal/normal1.gif")
        self.movie.setScaledSize(QSize(150, 150))
        self.image.setMovie(self.movie)
        self.movie.start()
        self.resize(1024, 1024)
        self.randomPosition()
        self.show()
        self.pet1 = []
        for i in os.listdir("normal"):
            self.pet1.append("normal/" + i)
        self.dialog = []
        with open("dialog.txt", "r") as f:
            text = f.read()
            self.dialog = text.split("\n")

    def petNormalAction(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.randomAct)
        self.timer.start(3000)
        self.condition = 0
        self.talkTimer = QTimer()
        self.talkTimer.timeout.connect(self.talk)
        self.talkTimer.start(3000)
        self.talk_condition = 0
        self.talk()

    def randomAct(self):
        if not self.condition:
            self.movie = QMovie(random.choice(self.pet1))
            self.movie.setScaledSize(QSize(150, 150))
            self.image.setMovie(self.movie)
            self.movie.start()
        else:
            self.movie = QMovie("./click/click.gif")
            self.movie.setScaledSize(QSize(150, 150))
            self.image.setMovie(self.movie)
            self.movie.start()
            self.condition = 0
            self.talk_condition = 0

    def talk(self):
        if not self.talk_condition:
            self.talkLabel.setText(random.choice(self.dialog))
            self.talkLabel.setStyleSheet(
                "font: bold;"
                "font:15pt 'STCaiyun';"
                "color:black;"
            )
            self.talkLabel.adjustSize()
        else:
            self.talkLabel.setText("别点我!去学习!")
            self.talkLabel.setStyleSheet(
                "font: bold;"
                "font:15pt 'STCaiyun';"
                "color:black;"
            )
            self.talkLabel.adjustSize()
            self.talk_condition = 0

    def quit(self):
        self.close()
        sys.exit()

    def showwin(self):
        self.setWindowOpacity(1)

    def randomPosition(self):
        screen_geo = QDesktopWidget().screenGeometry()
        pet_geo = self.geometry()
        width = (screen_geo.width() - pet_geo.width()) * random.random()
        height = (screen_geo.height() - pet_geo.height()) * random.random()
        self.move(width, height)

    def mousePressEvent(self, event):
        self.condition = 1
        self.talk_condition = 1
        self.talk()
        self.randomAct()
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
        self.mouse_drag_pos = event.globalPos() - self.pos()
        event.accept()
        self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def enterEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        hide = menu.addAction("隐藏")
        hide.setIcon(QIcon(os.path.join('ico/flower.ico')))
        quitAction = menu.addAction("退出")
        quitAction.setIcon(QIcon(os.path.join('ico/star.ico')))
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            qApp.quit()
        if action == hide:
            self.setWindowOpacity(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec_())
