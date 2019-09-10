import os
import sys
from PyQt5 import uic, QtWidgets
from mainwindow import MainWindow


os.chdir(os.path.dirname(os.path.realpath(__file__)))


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec_()
