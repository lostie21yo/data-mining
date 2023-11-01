from PyQt6.QtWidgets import QFileDialog

from modules.VideoThread import VideoThread


def openVideo(self):
    fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '', 
                                                'Images (*.mp4 *.avi *.mov *.mkv)')
    try:
        self.thread = VideoThread(source=fileName, fps=30)
        self.thread.change_pixmap_signal.connect(self.update_frame)
        self.thread.start()
        self.threadOn = True
        self.playButton.setEnabled(True)
        self.playButton.setIcon(self.pauseIcon)

    except Exception as e:
        print(e)