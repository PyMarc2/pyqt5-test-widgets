from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import QVariantAnimation, QEasingCurve, Qt


class WaitingDotWidget(QWidget):
    def __init__(self):
        super(WaitingDotWidget, self).__init__()
        self.dotsAmount = 3
        self.dotsSpacing = 10  # [pixels]
        self.dotsColor = QColor(255, 120, 120)  # (r,g,b)
        self.dotsSize = 50  # [pixels]
        self.initialVelocity = 500  # [pixels/s]
        self.endVelocity = 200  # [pixels/s]
        self.relativePointOfDeceleration = 0.6  # [%]
        self.animationSize = (200, self.dotsSize)  # [pixels, pixels]
        self.amountOfPointOnTrajectory = 1000  # [amount]
        self.duration = 2500  # [miliseconds]
        self.initialVelocityDuration = 1500
        self.decelerationDuration = 200  # [miliseconds]

        self.dotsPosition = {}
        self.dotsTimers = {}
        self.animations = {}

    def createDotAnimations(self):
        for i in range(self.dotsAmount):
            self.anim_velocity[i] = QVariantAnimation(self, startValue=self.initialVelocity, endValue=self.endVelocity,
                                                       duration=self.decelerationDuration, easingCurve=QEasingCurve.OutInExpo())
    def createTimers(self):
        pass

    def calculateNextPosition(self):
        pass


class WaitingDotsWidget2(QWidget):
    def __init__(self):
        super(WaitingDotsWidget2, self).__init__()
        '''
        TECHNIQUE: 
        - Separate position of dots in 3 different animations: linear, x^3, linear
        - Start timer of launching animation at different times
        - Reset animations
        '''
        # DOTS PARAMETERS
        self.dotsAmount = 3
        self.dotsSpacing = 10  # [pixels]
        self.dotsColor = QColor(255, 120, 120)  # (r,g,b)
        self.dotsRadius = 10  # [pixels]



        # ANIMATION PARAMETERS
        self.animationSize = (2000, self.dotsRadius)  # [pixels, pixels]
        self.relativePointOfDeceleration = 0.7  # [%]
        self.relativePointOfAcceleration = 0.9  # [%]
        self.amountOfPointOnTrajectory = 1000  # [amount]
        self.normalVelocity = 500  # [pixels/s]
        self.lowVelocity = 200  # [pixels/s]

        self.dotsPosition = {}
        self.dotsTimers = {}
        self.dotsAnimations = {}

    def initializePositionCurves(self):
        midStartPoint = self.amountOfPointOnTrajectory*self.relativePointOfDeceleration
        lastStartPoint = endValue=self.amountOfPointOnTrajectory*self.relativePointOfAcceleration
        duration1 = self.relativePointOfDeceleration*self.amountOfPointOnTrajectory/self.normalVelocity
        duration2 = (self.relativePointOfAcceleration-self.relativePointOfDeceleration)*self.amountOfPointOnTrajectory/self.normalVelocity
        duration3 = (1 - self.relativePointOfAcceleration)*self.amountOfPointOnTrajectory/self.normalVelocity
        motion_linearInitial = QVariantAnimation(self, startValue=0, endValue=midStartPoint, duration=duration1)
        motion_deceleration = QVariantAnimation(self, startValue=midStartPoint, endValue=lastStartPoint, duration=duration2)
        motion_linearEnd = QVariantAnimation(self, startValue=lastStartPoint, endValue=self.amountOfPointOnTrajectory, duration1=duration3)

        for i in range(self.dotsAmount):
            self.dotsAnimations[i] = [motion_linearInitial, motion_deceleration, motion_linearEnd]

    def paintEvent(self, event):
        #self.updatePosition()
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.transparent)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)

        for i in range(self.amountOfPointOnTrajectory):
            painter.save()
            painter.translate(0, 0)
            position = (i, 0)
            color = self.dotsColor
            painter.setBrush(QBrush(color, Qt.SolidPattern))
            painter.drawEllipse(position[0], position[1], self.dotsRadius, self.dotsRadius)






