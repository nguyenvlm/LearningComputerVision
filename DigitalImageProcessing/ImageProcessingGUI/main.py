import sys
import os
from PyQt5 import QtWidgets, QtCore, uic

import resource
from components import MainWindow

os.chdir(os.path.dirname(os.path.realpath(__file__)))

css_file = QtCore.QFile("./resource/css/style.css")

app = QtWidgets.QApplication([])

if css_file.open(QtCore.QFile.ReadOnly):
    ts = QtCore.QTextStream(css_file)
    app.setStyleSheet(ts.readAll())

window = MainWindow()

window.show()
app.exec_()
