import os
import numpy as np
from collections import deque
from PyQt5 import QtWidgets, QtGui, QtCore, uic

from ImageOperations import GrayscaleTransformation as gt
from ImageOperations import SpatialDomainFilter as sdf

class DotDict(dict):
    """
    a dictionary that supports dot notation
    as well as dictionary access notation
    usage: d = DotDict() or d = DotDict({'val1':'first'})
    set attributes: d.val2 = 'second' or d['val2'] = 'second'
    get attributes: d.val2 or d['val2']
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct=None):
        dct = dict() if not dct else dct
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = Dotdict(value)
            self[key] = value

class ImageMdi(QtWidgets.QMdiSubWindow):
    def __init__(self, parent, file_path, is_main=True, image=None):
        super(ImageMdi, self).__init__(parent)
        self.parent = parent

        self._is_main = is_main
        self.file_path = file_path

        self.__setup_window__()

        if image is None:
            self.image = self.__open_image__()
        else:
            self._raw = image
            self.image = image.image

        self.__show_image__()
        self.show()

        if self._is_main:
            self._result = ImageMdi(self.parent,
                                        self.file_path,
                                        False, self)
        else:
            self._undo_stack = []
            self._redo_stack = []
            self._file_changed = False

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

    def __open_image__(self):
        r_image = DotDict()
        image = QtGui.QImage(self.file_path)

        if image.format() != QtGui.QImage.Format_RGBA8888:
            image.convertTo(QtGui.QImage.Format_RGBA8888)

        r_image.width = image.width()
        r_image.height = image.height()

        ptr = image.constBits()
        ptr.setsize(r_image.height * r_image.width * 4)

        np_image = np.frombuffer(ptr, np.uint8).reshape((r_image.height, r_image.width, 4))

        r_image.rgb = np_image[:,:,:3].copy()
        r_image.alpha = np_image[:,:,-1].copy()
        
        return r_image

    def __set_image__(self, image, is_undo=False, is_redo=False):
        if is_undo:
            self._redo_stack.append(self.image)
        else:
            self._undo_stack.append(self.image)
            if not is_redo:
                self._redo_stack = []

        self._file_changed = True
        self.image = image
        self.__show_image__()

    def __get_pixmap__(self):
        # print(self.image.rgb.shape, self.image.alpha.shape)
        image = np.dstack((self.image.rgb, self.image.alpha))

        height, width, channel = image.shape

        # print(height, width, channel)

        bytes_per_line = channel * width
        qimage = QtGui.QImage(image, width, height,
                              bytes_per_line,
                              QtGui.QImage.Format_RGBA8888)

        pixmap = QtGui.QPixmap.fromImage(qimage)
        
        return pixmap

    def __show_image__(self):
        pixmap = self.__get_pixmap__()

        self.canvas.setPixmap(pixmap)

        self.canvas.setFixedSize(self.image.width, self.image.height)
        self.canvas.setMaximumSize(self.image.width, self.image.height)
        self.resize(self.image.width + 30, self.image.height + 50)
        self.repaint()

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

    def closeEvent(self, event):cmd
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
            image = DotDict(self.image)
            image.rgb = gt.histogramEqualize(self.image.rgb, adaptive_size="full")
            self.__set_image__(image)
    
    def apply_grayscale(self):
        if self._is_main:
            self._result.apply_grayscale()
        else:
            image = DotDict(self.image)
            image.rgb = gt.toGrayscale(self.image.rgb)
            self.__set_image__(image)

    def apply_contrast_auto_adjust(self):
        if self._is_main:
            self._result.apply_grayscale()
        else:
            image = DotDict(self.image)
            image.rgb = gt.contrastAutoAdjust(self.image.rgb)
            self.__set_image__(image)

    def apply_gamma_correction(self):
        if self._is_main:
            self._result.apply_grayscale()
        else:
            image = DotDict(self.image)
            image.rgb = gt.expoTransform(self.image.rgb)
            self.__set_image__(image)
    
    def apply_invert_color(self):
        if self._is_main:
            self._result.apply_grayscale()
        else:
            image = DotDict(self.image)
            image.rgb = gt.invert(self.image.rgb)
            self.__set_image__(image)

    def apply_mean_filter(self):
        if self._is_main:
            self._result.apply_mean_filter()
        else:
            image = DotDict(self.image)
            image.rgb = sdf.meanFilter(self.image.rgb)
            self.__set_image__(image)

    def apply_median_filter(self):
        if self._is_main:
            self._result.apply_median_filter()
        else:
            image = DotDict(self.image)
            image.rgb = sdf.medianFilter(self.image.rgb)
            self.__set_image__(image)

    def apply_gaussian_filter(self):
        if self._is_main:
            self._result.apply_gaussian_filter()
        else:
            image = DotDict(self.image)
            image.rgb = sdf.gaussianFilter(self.image.rgb)
            self.__set_image__(image)

    def apply_laplacian_filter(self):
        if self._is_main:
            self._result.apply_laplacian_filter()
        else:
            image = DotDict(self.image)
            image.rgb = sdf.laplacianFilter(self.image.rgb)
            self.__set_image__(image)

    def apply_log_filter(self):
        if self._is_main:
            self._result.apply_log_filter()
        else:
            image = DotDict(self.image)
            image.rgb = sdf.LoGFilter(self.image.rgb)
            self.__set_image__(image)

    def apply_highboost_filter(self):
        if self._is_main:
            self._result.apply_highboost_filter()
        else:
            image = DotDict(self.image)
            image.rgb = sdf.highboostFilter(self.image.rgb)
            self.__set_image__(image)

    def apply_unsharp_mask_filter(self):
        if self._is_main:
            self._result.apply_unsharp_mask_filter()
        else:
            image = DotDict(self.image)
            image.rgb = sdf.unsharpMaskFilter(self.image.rgb, 'laplacian')
            self.__set_image__(image)

    def apply_discrete_fourier_tranform(self):
        pass

    def apply_butterworth_low_pass(self):
        pass

    def apply_butterworth_high_pass(self):
        pass