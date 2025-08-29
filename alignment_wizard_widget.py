from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QImage
import cv2 as cv

class AlignmentWizardWidget(QWidget):
    
    PREVIEW_FPS = 23
    
    reload_overlay = True
    current_overlay = None
    preview_clock = QTimer()
    stream = cv.VideoCapture(1)
    
    def __init__(self, arucoroi_detector):
        super().__init__()

        self.detector = arucoroi_detector


        self.imageLabel = QLabel()

        save_new_button = QPushButton()
        save_new_button.setText("Overlay speichern")
        save_new_button.clicked.connect(self.save_current)

        contentLayout = QVBoxLayout()
        contentLayout.addStretch()
        contentLayout.addWidget(self.imageLabel)
        contentLayout.addWidget(save_new_button)
        contentLayout.addStretch()
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addStretch()
        horizontalLayout.addLayout(contentLayout)
        horizontalLayout.addStretch()
        
        while not self.stream.isOpened():
            pass
        
        self.start_preview()

        self.setLayout(horizontalLayout)
    
    def start_preview(self):
        if(self.preview_clock.isActive()):
            return
        
        self.preview_clock.timeout.connect(self.update_preview)
        self.preview_clock.start(round(1000 / self.PREVIEW_FPS))
    
    def update_preview(self):
        if(self.current_overlay is None):
            try:
                self.save_current()
            except:
                pass
        
        if(self.reload_overlay or self.current_overlay is None):
            try:
                print("reloaded")
                self.current_overlay = cv.imread("./alignment-save.png")
                self.current_overlay = cv.cvtColor(self.current_overlay, cv.COLOR_BGRA2RGBA)
            except:
                print("fail!")
                pass
        
        ret0, self.raw_frame = self.stream.read()
        self.raw_frame = cv.cvtColor(self.raw_frame, cv.COLOR_BGR2RGBA)
        
        unfinished_result = self.detector.grab_skeleton(self.raw_frame)
        self.overlay_result = cv.cvtColor(unfinished_result, cv.COLOR_BGRA2RGBA)
        height, width, channel = self.overlay_result.shape
        bytesPerLine = 4 * width
        try:
            combined = cv.add(self.raw_frame, self.current_overlay)
        except:
            combined = self.raw_frame
        combined = cv.add(combined, self.overlay_result)
        qImg = QImage(combined.data, width, height, bytesPerLine, QImage.Format.Format_RGBA8888)    
        pixmap = QPixmap.fromImage(qImg).scaledToHeight(900, Qt.TransformationMode.FastTransformation)
        self.imageLabel.setPixmap(pixmap)
    
    def save_current(self):
        cv.imwrite("./alignment-save.png", cv.cvtColor(self.overlay_result, cv.COLOR_BGRA2RGBA))