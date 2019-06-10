from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QEasingCurve
import copy

class Dialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.resize(500, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.button = QtWidgets.QPushButton()
        self.paintWidget = PaintWidget()

        self.button.clicked.connect(self.paintWidget.startMoving)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.button)
        lay.addWidget(self.paintWidget)


class PaintWidget(QtWidgets.QWidget):
    def __init__(self):
        super(PaintWidget, self).__init__()

        self.isLooping = True
        self.yPosition = 100

        self.dotsRadius = 8
        self.dotsColor = QtGui.QColor(255, 0, 15)
        self.dotsAmount = 3
        self.dotsSpeed = 500
        self.dotsSeparation = 70

        # ANIMATION PARAMETERS
        self.customEasing = QEasingCurve()
        self.customEasing.setCustomType(self.customEasingFunc)
        self.animationSize = 500

        self.dotsPosition = []
        self.dotsAnimations = []

        self.createPosition()
        self.createAnimation()

    @staticmethod
    def customEasingFunc(x):
        return 3.3 * (x - 0.51) ** 3 + 0.2 * (x - 7.9) + 2

    def startMoving(self):
        print(self.dotsAnimations)
        separationTime = (self.dotsSeparation / self.dotsSpeed) * 1000
        for i, animation in enumerate(self.dotsAnimations):
            QtCore.QTimer.singleShot(i * separationTime, animation.start)

    def createPosition(self):
        for i in range(self.dotsAmount):
            self.dotsPosition.append(QtCore.QPoint(0, self.yPosition))


    def createAnimation(self):
        duration = (self.animationSize / self.dotsSpeed)*1000

        for i, _ in enumerate(self.dotsPosition):
            anim = QtCore.QVariantAnimation(self, startValue=0, endValue=self.animationSize,
                                            duration=duration, easingCurve=self.customEasing)
            wrapper = partial(self.updatePosition, i)
            anim.valueChanged.connect(wrapper)

            if self.isLooping:
                anim.finished.connect(anim.start)

            self.dotsAnimations.append(anim)

    @QtCore.pyqtSlot(int, QtCore.QVariant)
    def updatePosition(self, i, position):
        self.dotsPosition[i] = QtCore.QPoint(position, self.yPosition)
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.transparent)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.NoPen)

        for position in self.dotsPosition:
            painter.setBrush(
                QtGui.QBrush(self.dotsColor, QtCore.Qt.SolidPattern)
            )
            painter.drawEllipse(position, self.dotsRadius, self.dotsRadius)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    dial = Dialog()
    dial.show()
    sys.exit(app.exec_())
