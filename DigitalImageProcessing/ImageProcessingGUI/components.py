from PyQt5 import QtWidgets, QtGui, QtCore, uic

from lib.mainwindow import Ui_main_window
from lib.imagemdi import ImageMdi

class MainWindow(QtWidgets.QWidget, Ui_main_window):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setupUi(self)

        self.workspace.setWindowFlags(QtCore.Qt.Widget)

        self._child = []

        self.__setup_mouse_event__()
        self.__setup_workspace__()
        self.__setup_signal__()
        self.__setup_shortcut__()

    def __setup_signal__(self):
        self.btn_resize.clicked.connect(self.__toggle_fullscreen__)
        
        self.btn_open.clicked.connect(self.__open_image__)
        self.btn_save.clicked.connect(self.__save_image__)
        self.btn_saveas.clicked.connect(self.__save_image_as__)
        self.btn_undo.clicked.connect(self.__undo_change__)
        self.btn_redo.clicked.connect(self.__redo_change__)
        self.btn_reset.clicked.connect(self.__discard_change__)
        
        self.btn_gray.clicked.connect(self.__convert_grayscale__)
        self.btn_invcolor.clicked.connect(self.__invert_color__)
        self.btn_contrast.clicked.connect(self.__gamma_correction__)
        self.btn_eq.clicked.connect(self.__histogram_equalize__)
        self.btn_iso.clicked.connect(self.__contrast_auto_adjust__)

    def __setup_shortcut__(self):
        self.btn_open.setShortcut("Ctrl+O")
        self.btn_save.setShortcut("Ctrl+S")
        self.btn_saveas.setShortcut("Ctrl+Shift+S")
        self.btn_undo.setShortcut("Ctrl+Z")
        self.btn_redo.setShortcut("Ctrl+Y")
        self.btn_reset.setShortcut("Ctrl+R")

    def __setup_workspace__(self):
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
            "main_window", "Apply Contrast Auto Adjustment"))
        self.btn_contrast.setToolTip(_translate(
            "main_window", "Apply Gamma Correction"))
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
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                             "Open Image...", filter="Image formats: *.png; *.jpg; *.tif")

        if (file_path):
            child = ImageMdi(self.mdi_area, file_path)

            def close_event(ev):
                self._child.remove(child)
            child.closeEvent = close_event
            
            self._child.append(child)
    
    def __save_image__(self):
        if len(self._child) > 0:
            self.mdi_area.currentSubWindow().save()
    def __save_image_as__(self):
        if len(self._child) > 0:
            self.mdi_area.currentSubWindow().save_as()

    def __undo_change__(self):
        if len(self._child) > 0:
            self.mdi_area.currentSubWindow().undo()
    def __redo_change__(self):
        if len(self._child) > 0:
            self.mdi_area.currentSubWindow().redo()
    def __discard_change__(self):
        if len(self._child) > 0:
            self.mdi_area.currentSubWindow().discard()

    def __convert_grayscale__(self):
        if len(self._child) > 0:
            self.mdi_area.currentSubWindow().apply_grayscale()

    def __invert_color__(self):
        if len(self._child) > 0:
            self.mdi_area.currentSubWindow().apply_invert_color()

    def __gamma_correction__(self):
        if len(self._child) > 0:
            self.mdi_area.currentSubWindow().apply_gamma_correction()

    def __histogram_equalize__(self):
        if len(self._child) > 0:
            self.mdi_area.currentSubWindow().apply_histogram_equalize()

    def __contrast_auto_adjust__(self):
        if len(self._child) > 0:
            self.mdi_area.currentSubWindow().apply_contrast_auto_adjust()
    


class SliderMdi(QtWidgets.QMdiSubWindow):
    def __init__(self, parent, label):
        super(SliderMdi, self).__init__()
