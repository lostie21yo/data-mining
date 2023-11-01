import cv2
import numpy as np
from PyQt6 import uic
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QImage, QPixmap, QPalette
from PyQt6.QtWidgets import QLabel, QSizePolicy, QWidgetAction, QStyle

# classes and funsctions
from modules.openImage import openImage
from modules.openVideo import openVideo
from modules.openCamera import openCamera

# UI
# from ui.app_ui import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        # self.setupUi(self) # из файла .py с помощью pyuic6 ui\app.ui -o ui\app_ui.py
        uic.loadUi('ui/app.ui', self) # напрямую из ui-файла

        self.thread = None
        self.fsw = None
        self.scale = 0.0
        self.threadOn = False
        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.ColorRole.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.scrollPictureArea.setWidget(self.imageLabel)
        self.scrollPictureArea.setVisible(False)
        self.createActions()
        self.playIcon = self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_MediaPlay"))
        self.pauseIcon = self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_MediaPause"))
        self.playButton.setIcon(self.playIcon)

    
    def __clean_frame(self):
        if self.thread is not None:
            self.thread.resume()
            self.threadOn = False 
            self.thread.close()

    def openImage(self):
        self.__clean_frame()
        openImage(self)

    def openVideo(self):
        self.__clean_frame()
        openVideo(self)

    def openCamera(self):
        self.__clean_frame()
        openCamera(self)

    @pyqtSlot()
    def toggle_video(self):
        """
        Метод изменения состояния веб-камеры (выкл/вкл)
        :return:
        """
        if self.thread is None:
            return
        if self.threadOn:
            self.thread.pause()
            print('Video thread PAUSED')
            self.playButton.setIcon(self.playIcon)
            self.threadOn = False
        else:
            self.thread.resume()
            print('Video thread RESUMED')
            self.playButton.setIcon(self.pauseIcon)
            self.threadOn = True

    @pyqtSlot(np.ndarray)
    def update_frame(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = image.shape
        bytes_per_line = ch * w
        q_image = QImage(image.data, w, h, bytes_per_line, 
                         QImage.Format.Format_RGB888)
        self.imageLabel.setPixmap(QPixmap(q_image))
        self.fitToWindowAct.setEnabled(True)
        self.scale = 1.0
        self.scrollPictureArea.setVisible(True)
        self.updateActions()

        if not self.fitToWindowAct.isChecked():
            self.imageLabel.adjustSize()


    def updateActions(self):
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

    def scaleImage(self, factor):
        self.scale *= factor
        self.imageLabel.resize(self.scale * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollPictureArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollPictureArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scale < 3.0)
        self.zoomOutAct.setEnabled(self.scale > 0.333)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scale = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollPictureArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def createActions(self):
        self.actionOpenImage.triggered.connect(self.openImage)
        self.actionOpenImage.setShortcut("Ctrl+O")
        self.actionOpenVideo.triggered.connect(self.openVideo)
        self.actionOpenCamera.triggered.connect(self.openCamera)

        self.normalSizeAct = QWidgetAction(self)
        self.normalSizeAct.setText("&Normal Size")
        self.normalSizeAct.setShortcut("Ctrl+S")
        self.normalSizeAct.setEnabled(False)
        self.normalSizeAct.triggered.connect(self.normalSize)

        self.fitToWindowAct = QWidgetAction(self)
        self.fitToWindowAct.setText("&Fit to Window")
        self.fitToWindowAct.setShortcut("Ctrl+F")
        self.fitToWindowAct.setEnabled(False)
        self.fitToWindowAct.setCheckable(True)
        self.fitToWindowAct.triggered.connect(self.fitToWindow)

        self.playButton.clicked.connect(self.toggle_video)
        self.playButton.setDisabled(True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MyWindow = MainWindow()
    MyWindow.show()
    sys.exit(app.exec())
