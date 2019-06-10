from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import QVariantAnimation, QVariant, QEasingCurve, Qt, QTimer, pyqtSlot
import time


class WaitingDotsWidget2(QWidget):
    def __init__(self):
        super(WaitingDotsWidget2, self).__init__()
        '''
        TECHNIQUE: 
        - Separate position of dots in 3 different animations: linear, x^3, linear
        - Start timer of launching animation at different times
        - Reset animations
        '''
        # WIDGET PARAMETERS
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # DOTS PARAMETERS
        self.dotsAmount = 3
        self.dotsSpacing = 10  # [pixels]
        self.dotsColor = QColor(255, 120, 120)  # (r,g,b)
        self.dotsRadius = 10  # [pixels]

        # ANIMATION PARAMETERS
        self.relativePointOfDeceleration = 0.7  # [%]
        self.relativePointOfAcceleration = 0.9  # [%]
        self.amountOfPointOnTrajectory = 1000  # [amount]
        self.normalVelocity = 500  # [pixels/s]
        self.lowVelocity = 200  # [pixels/s]

        self.dotsPosition = [0, 0]
        self.dotsAnimations = {}
        self.initializePositionCurves()

    def start(self):
        self.timer = QTimer(self)
        for i in range(self.dotsAmount):
            self.dotsAnimations[i][0].start()
            time.sleep(self.dotsSpacing*1000/self.normalVelocity)

    def initializePositionCurves(self):
        midStartPoint = self.amountOfPointOnTrajectory*self.relativePointOfDeceleration
        lastStartPoint = self.amountOfPointOnTrajectory*self.relativePointOfAcceleration
        duration1 = self.relativePointOfDeceleration*self.amountOfPointOnTrajectory/self.normalVelocity
        duration2 = (self.relativePointOfAcceleration-self.relativePointOfDeceleration)*self.amountOfPointOnTrajectory/self.normalVelocity
        duration3 = (1 - self.relativePointOfAcceleration)*self.amountOfPointOnTrajectory/self.normalVelocity
        motion_linearInitial = QVariantAnimation(self, startValue=0, endValue=midStartPoint, duration=duration1)
        motion_deceleration = QVariantAnimation(self, startValue=midStartPoint, endValue=lastStartPoint, duration=duration2)
        motion_linearEnd = QVariantAnimation(self, startValue=lastStartPoint, endValue=self.amountOfPointOnTrajectory, duration=duration3)

        for i in range(self.dotsAmount):
            self.dotsAnimations[i] = [motion_linearInitial, motion_deceleration, motion_linearEnd]
            for j in range(len(self.dotsAnimations[i])):
                self.dotsAnimations[i][j].valueChanged.connect(self.updateDotsPosition)
                try:
                    self.dotsAnimations[i][j].finished.connect(self.dotsAnimations[i][j+1].start)
                except Exception as err:
                    print(err)
                    self.dotsAnimations[i][j].finished.connect(self.dotsAnimations[i][j-(self.dotsAmount-1)].start)

    @pyqtSlot(QVariant)
    def updateDotsPosition(self, position):
        self.dotsPosition = [position, 0]
        self.print(self.sender())
        self.update()

    def paintEvent(self, event):
        if not self.paintingActive():
            painter = QPainter(self)
            painter.fillRect(self.rect(), Qt.transparent)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setPen(Qt.NoPen)

            for i in range(self.dotsAmount):
                painter.save()
                painter.translate(0, 0)
                position = (self.dotsPosition[0], self.dotsPosition[1])
                color = self.dotsColor
                painter.setBrush(QBrush(color, Qt.SolidPattern))
                painter.drawEllipse(position[0], position[1], self.dotsRadius, self.dotsRadius)

                painter.restore()
                del painter




