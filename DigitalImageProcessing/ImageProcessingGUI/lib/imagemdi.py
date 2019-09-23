import os
import numpy as np
from collections import deque
from PyQt5 import QtWidgets, QtGui, QtCore, uic

from ImageOperations import GrayscaleTransformation as gt

class ImageMdi(QtWidgets.QMdiSubWindow):
    def __init__(self, parent, file_path, is_main=True, image=None):
        super(ImageMdi, self).__init__(parent)
        self.parent = parent

        self._is_main = is_main
        self.file_path = file_path

        self.__setup_window__()

        if image is None:
            self.__open_image__()
        else:
            self._raw = image
            self.image = image.image

        self.show_image()
        self.show()

        if self._is_main:
            self._result = ImageMdi(self.parent,
                                        self.file_path,
                                        False, self)
        else:
            self._undo_stack = []
            self._redo_stack = []
            self._file_changed = False

    def show_image(self):
        height, width, channel = self.image.shape

        bytes_per_line = channel * width
        qimage = QtGui.QImage(self.image, width, height,
                              bytes_per_line,
                              QtGui.QImage.Format_RGBA8888)

        pixmap = QtGui.QPixmap.fromImage(qimage)

        self.canvas.setPixmap(pixmap)

        self.canvas.setFixedSize(width, height)
        self.canvas.setMaximumSize(width, height)
        self.resize(width + 30, height + 50)
        self.repaint()

    def __open_image__(self):
        image = QtGui.QImage(self.file_path)

        if image.format() != QtGui.QImage.Format_RGBA8888:
            image.convertTo(QtGui.QImage.Format_RGBA8888)

        width = image.width()
        height = image.height()

        ptr = image.bits()
        ptr.setsize(height * width * 4)

        self.image = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
        self.qimage = image

    def __setup_window__(self):
        flags = QtCore.Qt.WindowTitleHint if self._is_main else QtCore.Qt.CustomizeWindowHint
        self.parent.addSubWindow(self, flags)

        _, file_name = os.path.split(self.file_path)
        win_type = "Result: " if not self._is_main else ""

        self.setWindowTitle(win_type + file_name)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.content = QtWidgets.QWidget(self)

        layout = QtWidgets.QGridLayout(self.content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.canvas = QtWidgets.QLabel(self)
        layout.addWidget(self.canvas, 0, 0, 1, 1)

        self.setWidget(self.content)

    def save(self):
        pass

    def save_as(self):
        if self._is_main:
            self._result.save_as()
        else:
            self.file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self.parent, "Save Image as...", filter="Portable Network Graphics: *.png")

            print(self.file_path)
            self.save()

    def undo(self):
        if self._is_main:
            self._result.undo()
        else:
            if len(self._undo_stack) > 0:
                image = self._undo_stack.pop()
                self.__set_image__(image, True)

    def redo(self):
        if self._is_main:
            self._result.redo()
        else:
            if len(self._redo_stack) > 0:
                image = self._redo_stack.pop()
                self.__set_image__(image, is_redo=True)

    def discard(self):
        if self._is_main:
            self._result.discard()
        else:
            image = self._raw.image
            self.__set_image__(image)

    def closeEvent(self, event):
        if self._is_main and self._result._file_changed:
            choice = QtWidgets.QMessageBox.question(self.parent, "File not save!",
                                                    "File {} was not save!\n Do you want to Save change?".format(
                                                        self.file_path),
                                                    QtWidgets.QMessageBox.Save |
                                                    QtWidgets.QMessageBox.Discard |
                                                    QtWidgets.QMessageBox.Cancel)

            print(choice)
            if choice == QtWidgets.QMessageBox.Cancel:
                event.ignore()
                return
            elif choice == QtWidgets.QMessageBox.Save:
                self._result.save()

        self._result.close()

    def apply_histogram_equalize(self):
        if self._is_main:
            self._result.apply_histogram_equalize()
        else:
            image = gt.histogramEqualize(self.image, adaptive_size="full")
            self.__set_image__(image)
    
    def apply_grayscale(self):
        if self._is_main:
            self._result.apply_grayscale()
        else:
            image = gt.toGrayscale(self.image)
            self.__set_image__(image)

    def apply_contrast_auto_adjust(self):
        if self._is_main:
            self._result.apply_grayscale()
        else:
            image = gt.contrastAutoAdjust(self.image)
            self.__set_image__(image)

    def apply_gamma_correction(self):
        if self._is_main:
            self._result.apply_grayscale()
        else:
            image = gt.expoTransform(self.image)
            self.__set_image__(image)
            
    
    def apply_invert_color(self):
        if self._is_main:
            self._result.apply_grayscale()
        else:
            image = gt.invert(self.image)
            self.__set_image__(image)

    def __set_image__(self, image, is_undo=False, is_redo=False):
        if is_undo:
            self._redo_stack.append(self.image)
        else:
            self._undo_stack.append(self.image)
            if not is_redo:
                self._redo_stack = []

        self.image = image
        self.show_image()

            