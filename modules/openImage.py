from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QFileDialog, QMessageBox

def openImage(self):
    fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                            'Images (*.png *.jpeg *.jpg *.bmp *.gif)')
    if fileName:
        print("Image OPENED")
        image = QImage(fileName)
        if image.isNull():
            QMessageBox.information(
                self, "Image Viewer", "Cannot load %s." % fileName)
            return
        self.fitToWindowAct.setEnabled(True)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))
        self.scaleFactor = 1.0
        self.scrollPictureArea.setVisible(True)
        self.updateActions()
        self.playButton.setDisabled(True)
        self.playButton.setIcon(self.playIcon)

        if not self.fitToWindowAct.isChecked():
            self.imageLabel.adjustSize()
