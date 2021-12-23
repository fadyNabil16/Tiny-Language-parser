from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 Drawing Tutorial"
        self.top = 150
        self.left = 150
        self.width = 500
        self.height = 500
        self.all_point = []
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.paintEvent(x=50, y=50)
        self.show()

    def paintEvent(self, event=None, x=None, y=None):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.green,  8, Qt.SolidLine))
        painter.drawEllipse(x, y, 40, 40)


App = QApplication(sys.argv)

window = Window()

sys.exit(App.exec())
