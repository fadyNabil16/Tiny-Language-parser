from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *

import sys, os, pathlib
from scanner import Scanner
from _parser import Tree
from draw_tree import get_tree

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cwd = os.getcwd()
        self.opened_file = None
        # os.environ["PATH"] += os.pathsep + str(pathlib.Path(os.getcwd()).parent) + '/Graphviz/bin' + os.pathsep
        os.environ["PATH"] += os.pathsep + os.getcwd() + '/Graphviz/bin' + os.pathsep
        self.title = "PyQt5 Drawing Tutorial"
        self.setGeometry(100,100,750, 585)
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.top, self.left, self.width, self.height)
        self.gui = Gui()
        self.gui.btn2.clicked.connect(self.openFileDialog)
        self.gui.btn1.clicked.connect(self.convert)
        self.setCentralWidget(self.gui)#DrawTree(self.tre.getRoot().children[0])
        self.show()
    def openFileDialog(self):
        filename = QFileDialog.getOpenFileName(self,'Open File')
        self.opened_file = filename[0]
        if filename[0]:
            self.gui.text2.setPlainText('')
            if os.path.exists(self.cwd+'/output/graph.gv'):
                open(self.cwd+'/output/graph.gv', 'w').close()
            f = open(filename[0],'r')
            with f:
                data = f.read()
                self.gui.text1.setPlainText(data)
                self.gui.text1.setStyleSheet("color: white; background-color: #3a3a3a; font: 14pt calibri;")

    def convert(self):
        if self.opened_file is not None:
            data = open(self.opened_file,'r').read()
            src = Scanner(data)
            final_tokens = src.get_all_tokens()
            self.gui.text2.setPlainText(final_tokens)
            self.gui.text2.setStyleSheet("color: white; background-color: #3a3a3a; font: 14pt calibri;")
            path = self.opened_file
            get_tree(path)
        else:
            self.gui.text2.setPlainText("Nothing to Convert Choose File")
            self.gui.text2.setStyleSheet("color: white; background-color: #3a3a3a; font: 14pt calibri;")

class Gui(QDialog):
    def __init__(self):
        super(Gui, self).__init__()
        loadUi("./ui/gui.ui", self)
    


App = QApplication(sys.argv)

window = Window()

sys.exit(App.exec())
