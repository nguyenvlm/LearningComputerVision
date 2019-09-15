import sys
from PyQt5 import QtWidgets, QtCore, uic, QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(r"./resources/main.ui", self)
        self.setup()

    def setup(self):
        self.btnOpen.clicked.connect(self.openImage)
        self.show()

    def openImage(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Image...", filter="Image formats: *.png; *.jpg; *.tif")
        print(filename)
        pixmap = QtGui.QPixmap(filename[0])
        print(pixmap)

        self.img.setPixmap(pixmap)
