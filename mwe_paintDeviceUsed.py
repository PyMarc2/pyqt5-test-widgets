from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDialog, QPushButton
from PyQt5.QtCore import Qt, pyqtSlot, QVariantAnimation
from PyQt5.QtGui import QColor, QPainter, QBrush


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


class PaintWidget(QWidget):
    def __init__(self):
        super(PaintWidget, self).__init__()
        self.dotRadius = 10
        self.dotColor = QColor(255, 100, 100)

        self.animation = []
        self.createAnimation()

        self.dotPosition = [0, 0]

    def startPainting(self):
        self.animation.start()

    def createAnimation(self):
        self.animation = QVariantAnimation(self, startValue=0, endValue=500, duration=3000)
        self.animation.valueChanged.connect(self.updatePosition)

    @pyqtSlot()
    def updatePosition(self, *args):
        print(args)
        self.dotPosition = [args[0], 0]
        self.update()

    def paintEvent(self, event):
        if not self.paintingActive():
            painter = QPainter(self)
            painter.fillRect(self.rect(), Qt.transparent)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setPen(Qt.NoPen)

            painter.save()
            painter.translate(0, 0)
            position = (self.dotPosition[0], self.dotPosition[1])
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
