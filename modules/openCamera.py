from modules.VideoThread import VideoThread

def openCamera(self):
    self.thread = VideoThread()
    self.thread.change_pixmap_signal.connect(self.update_frame)
    self.thread.start()
    self.threadOn = True
    self.playButton.setEnabled(True)
    self.playButton.setIcon(self.pauseIcon)