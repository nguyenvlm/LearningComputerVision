import numpy as np
import cv2
from PyQt5 import QtWidgets, QtGui, QtCore, uic

from lib.gui import Ui_main_window
from lib import imtools


class MainWindow(QtWidgets.QWidget, Ui_main_window):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setupUi(self)

        self.workspace.setWindowFlags(QtCore.Qt.Widget)

        self.__setup_mouse_event__()
        self.__init_workspace__()
        self.__signal_connect__()

    def __signal_connect__(self):
        self.btn_resize.clicked.connect(self.__toggle_fullscreen__)
        self.btn_open.clicked.connect(self.__open_image__)
        self.btn_gray.clicked.connect(self.__convert_grayscale__)

    def __init_workspace__(self):
        self.__setup_tool_box__()

        self.mdi_area = QtWidgets.QMdiArea(self.workspace)
        self.mdi_area.setObjectName("mdi_area")
        self.mdi_area.setBackground(QtGui.QBrush(QtGui.QColor("#36393f")))
        self.mdi_area.setOption(
            QtWidgets.QMdiArea.DontMaximizeSubWindowOnActivation)
        self.mdi_area.setViewMode(QtWidgets.QMdiArea.SubWindowView)
        self.mdi_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdi_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        self.workspace.setCentralWidget(self.mdi_area)

    def __setup_tool_box__(self):
        self.tool_box = QtWidgets.QDockWidget(
            "Tools", self.workspace)

        self.tool_box.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea |
                                      QtCore.Qt.RightDockWidgetArea)
        self.tool_box.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable |
                                  QtWidgets.QDockWidget.DockWidgetFloatable)

        self.tool_box_content = QtWidgets.QWidget()
        self.tool_box_content.setObjectName("tool_box_content")
        self.tool_box_content.setFixedWidth(70)
        self.tool_box_content.setContentsMargins(0, 0, 0, 0)

        layout = QtWidgets.QGridLayout(self.tool_box_content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        self.btn_gray = QtWidgets.QToolButton(self.tool_box_content)
        icon = QtGui.QIcon(QtGui.QIcon(":/icon/img/dark/gray.svg"))
        self.btn_gray.setIcon(icon)
        self.btn_gray.setIconSize(QtCore.QSize(20, 20))

        self.btn_invcolor = QtWidgets.QToolButton(self.tool_box_content)
        icon = QtGui.QIcon(QtGui.QIcon(":/icon/img/dark/invert_color.svg"))
        self.btn_invcolor.setIcon(icon)
        self.btn_invcolor.setIconSize(QtCore.QSize(20, 20))

        self.btn_opacity = QtWidgets.QToolButton(self.tool_box_content)
        icon = QtGui.QIcon(QtGui.QIcon(":/icon/img/dark/opacity.svg"))
        self.btn_opacity.setIcon(icon)
        self.btn_opacity.setIconSize(QtCore.QSize(20, 20))

        self.btn_iso = QtWidgets.QToolButton(self.tool_box_content)
        icon = QtGui.QIcon(QtGui.QIcon(":/icon/img/dark/iso.svg"))
        self.btn_iso.setIcon(icon)
        self.btn_iso.setIconSize(QtCore.QSize(20, 20))

        self.btn_contrast = QtWidgets.QToolButton(self.tool_box_content)
        icon = QtGui.QIcon(QtGui.QIcon(":/icon/img/dark/contrast.svg"))
        self.btn_contrast.setIcon(icon)
        self.btn_contrast.setIconSize(QtCore.QSize(20, 20))

        self.btn_eq = QtWidgets.QToolButton(self.tool_box_content)
        icon = QtGui.QIcon(QtGui.QIcon(":/icon/img/dark/eq.svg"))
        self.btn_eq.setIcon(icon)
        self.btn_eq.setIconSize(QtCore.QSize(20, 20))

        layout.addWidget(self.btn_gray, 0, 0, 1, 1)
        layout.addWidget(self.btn_invcolor, 0, 1, 1, 1)
        layout.addWidget(self.btn_opacity, 1, 0, 1, 1)
        layout.addWidget(self.btn_iso, 1, 1, 1, 1)
        layout.addWidget(self.btn_contrast, 2, 0, 1, 1)
        layout.addWidget(self.btn_eq, 2, 1, 1, 1)

        _ = QtWidgets.QSpacerItem(20, 40,
                                  QtWidgets.QSizePolicy.Minimum,
                                  QtWidgets.QSizePolicy.Expanding)
        layout.addItem(_, 999, 0, 1, 1)

        self.tool_box.setWidget(self.tool_box_content)

        self.workspace.addDockWidget(
            QtCore.Qt.LeftDockWidgetArea, self.tool_box)

        _translate = QtCore.QCoreApplication.translate
        self.btn_gray.setToolTip(_translate(
            "main_window", "Convert to Grayscale"))
        self.btn_invcolor.setToolTip(_translate(
            "main_window", "Invert Color"))
        self.btn_opacity.setToolTip(
            _translate("main_window", "Change Opacity"))
        self.btn_iso.setToolTip(_translate(
            "main_window", "ISO"))
        self.btn_contrast.setToolTip(_translate(
            "main_window", "Apply Contrast Correction"))
        self.btn_eq.setToolTip(_translate(
            "main_window", "Apply Histogram Equalization"))

    def __setup_mouse_event__(self):
        self._pressing = False

        def mousePressEvent(event):
            if not self.isMaximized():
                self._start = self.mapToGlobal(event.pos())
                self._pressing = True

        def mouseMoveEvent(event):
            if self._pressing:
                self._end = self.mapToGlobal(event.pos())
                self._movement = self._end-self._start
                self.setGeometry(self.mapToGlobal(self._movement).x(),
                                 self.mapToGlobal(self._movement).y(),
                                 self.width(),
                                 self.height())
                self._start = self._end

        def mouseReleaseEvent(QMouseEvent):
            self._pressing = False

        def mouseDoubleClickEvent(QMouseEvent):
            self.__toggle_fullscreen__()

        self.title_bar.mousePressEvent = mousePressEvent
        self.title_bar.mouseMoveEvent = mouseMoveEvent
        self.title_bar.mouseReleaseEvent = mouseReleaseEvent
        self.title_bar.mouseDoubleClickEvent = mouseDoubleClickEvent

    def __toggle_fullscreen__(self):
        if self.isMaximized():
            self.showNormal()
            icon = QtGui.QIcon(":icon/img/dark/maximize.svg")
            self.btn_resize.setIcon(icon)
        else:
            self.showMaximized()
            icon = QtGui.QIcon(":icon/img/dark/restore.svg")
            self.btn_resize.setIcon(icon)

    def __open_image__(self):
        self.open_file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                       "Open Image...", filter="Image formats: *.png; *.jpg; *.tif")

        if (self.open_file_name):
            self.open_image = cv2.imread(self.open_file_name)

            self.image_viewer = ImageMdi(self.mdi_area, "Input")
            self.mdi_area.addSubWindow(self.image_viewer,
                                       QtCore.Qt.WindowTitleHint)

            self.image_viewer.load_image(self.open_image)

            self.result_image = self.open_image
            self.result_viewer = ImageMdi(self.mdi_area, "Processed Result")
            self.mdi_area.addSubWindow(self.result_viewer,
                                       QtCore.Qt.WindowTitleHint)

            self.result_viewer.load_image(self.result_image)

    def __convert_grayscale__(self):
        self.result_image = imtools.to_grayscale(self.result_image)
        self.result_viewer.load_image(self.result_image)


class ImageMdi(QtWidgets.QMdiSubWindow):
    def __init__(self, parent, label):
        super(ImageMdi, self).__init__(parent)
        self.parent = parent

        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle(label)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setOption(QtWidgets.QMdiSubWindow.RubberBandMove)
        self.setOption(QtWidgets.QMdiSubWindow.RubberBandResize)

        self.content = QtWidgets.QWidget(self)

        layout = QtWidgets.QGridLayout(self.content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.canvas = QtWidgets.QLabel(self)
        layout.addWidget(self.canvas, 0, 0, 1, 1)

        self.setWidget(self.content)

    def load_image(self, img):
        height, width, _ = img.shape
        bytesPerLine = 3 * width

        img = np.require(img, np.uint8, 'C')
        parsed_img = QtGui.QImage(img, width, height,
                                  bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
        self.canvas.setPixmap(QtGui.QPixmap.fromImage(parsed_img))

        # print(height, width)

        self.canvas.setFixedSize(width, height)
        self.canvas.setMaximumSize(width, height)
        self.resize(width + 30, height + 50)
        self.show()
