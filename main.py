from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from WaitingDotsWidget import WaitingDotsWidget2


class Dialog(QDialog):
    def __init__(self, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)
        self.resize(500, 500)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setLayout(QVBoxLayout())
        self.button = QPushButton()
        self.layout().addWidget(self.button)
        self.button.clicked.connect(self.startAnim)

        self.waiter = WaitingDotsWidget2()
        self.layout().addWidget(self.waiter)

    def startAnim(self):
        self.waiter.start()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dial = Dialog()
    dial.show()
    sys.exit(app.exec_())
