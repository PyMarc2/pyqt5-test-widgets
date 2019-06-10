from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDialog, QPushButton
from PyQt5.QtCore import Qt, pyqtSlot, QVariantAnimation, QVariant, QTimer
from PyQt5.QtGui import QColor, QPainter, QBrush
import time

class Dialog(QDialog):
    def __init__(self, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)
        self.resize(500, 500)
        self.setLayout(QVBoxLayout())
        self.button = QPushButton()
        self.layout().addWidget(self.button)
        self.paintWidget = PaintWidget()
        self.layout().addWidget(self.paintWidget)
        self.button.clicked.connect(self.paintWidget.startPainting)
        self.button.clicked.connect(self.reverse)

    def reverse(self):
        if self.paintWidget.isMoving:
            self.paintWidget.stopPainting()

class PaintWidget(QWidget):
    def __init__(self):
        super(PaintWidget, self).__init__()
        self.dotRadius = 10
        self.dotColor = QColor(255, 100, 100)
        self.numberOfDots = 3

        self.isMoving = False

        self.animation = []
        self.createAnimation()

        self.dotPosition = [[0, 0], [0, 0], [0, 0]]

    def startPainting(self):
        for i in range(self.numberOfDots):
            self.animation[i].start()
            time.sleep(200)
        self.isActive = True

    def createAnimation(self):
        for i in range(self.numberOfDots):
            self.animation.append(QVariantAnimation(self, startValue=0, endValue=500, duration=3000))
            self.animation[i].valueChanged.connect(self.updatePosition)

    @pyqtSlot(QVariant)
    def updatePosition(self, position):
        self.dotPosition = [position, 0]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.transparent)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)

        for i in range(self.numberOfDots):
            painter.save()
            painter.translate(0, 0)
            position = (self.dotPosition[i][0], self.dotPosition[i][1])
            color = self.dotColor
            painter.setBrush(QBrush(color, Qt.SolidPattern))
            painter.drawEllipse(position[0], position[1], self.dotRadius, self.dotRadius)
            painter.restore()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dial = Dialog()
    dial.show()
    sys.exit(app.exec_())
