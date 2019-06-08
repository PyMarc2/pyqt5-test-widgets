from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from WaitingDotsWidget import WaitingDotsWidget2


class Dialog(QDialog):
    def __init__(self, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.waiter = WaitingDotsWidget2()
        self.layout().addWidget(self.waiter)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dial = Dialog()
    dial.show()
    sys.exit(app.exec_())
