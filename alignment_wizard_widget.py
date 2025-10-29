from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QImage
import cv2 as cv

class AlignmentWizardWidget(QWidget):
    
    PREVIEW_TICKS_PER_S = 30
    SKIP_FRAMES = 15
    
    wizard_done_signal = pyqtSignal()
    
    reload_overlay = True
    current_overlay = None
    preview_clock = QTimer()
    
    def __init__(self, arucoroi_detector, capture0: cv.VideoCapture, capture1: cv.VideoCapture):
        super().__init__()

        self.detector = arucoroi_detector
        self.capture0 = capture0
        self.capture1 = capture1

        explainer_label = QLabel("<b>Willkommen bei der Kamera-Einstellungshilfe</b> <br>Die Rosa Boxen des Overlays sollten gut mit den ebenfalls markierten Markerkanten übereinstimmen. Im Idealfall \"verschwimmen\" sie mit den jeweiligen Kantenmarkierungen. Leichte Abweichungen sind in der Regel aber nicht schlimm.")

        font = explainer_label.font()
        font.setPointSize(28)
        explainer_label.setTextFormat(Qt.TextFormat.RichText)
        explainer_label.setAlignment(Qt.AlignmentFlag.AlignLeading)
        explainer_label.setWordWrap(True)
        explainer_label.setFont(font)

        self.imageLabel = QLabel()

        save_new_button = QPushButton()
        save_new_button.setText("Aktuelle Position speichern")
        save_new_button.setFont(font)
        save_new_button.clicked.connect(self.save_current)
        
        done_button = QPushButton()
        done_button.setText("Anwendung starten")
        done_button.setFont(font)
        done_button.clicked.connect(self.emit_wizard_done_signal)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(save_new_button)
        button_layout.addSpacing(15)
        button_layout.addWidget(done_button)
        button_layout.addStretch()

        contentLayout = QVBoxLayout()
        contentLayout.addStretch()
        contentLayout.addWidget(explainer_label)
        contentLayout.addWidget(self.imageLabel)
        contentLayout.addLayout(button_layout)
        contentLayout.addStretch()
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addStretch()
        horizontalLayout.addLayout(contentLayout)
        horizontalLayout.addStretch()
        
        while not self.capture0.isOpened() and self.capture1.isOpened():
            pass
        
        self.setLayout(horizontalLayout)
        
        self.start_preview()
    
    # starts UI clock to let us show "video" aka single frames in rapid succession
    def start_preview(self):
        if(self.preview_clock.isActive()):
            return
        
        # needed to initially run the detection on frame 0
        self.frame_n = self.SKIP_FRAMES
        
        self.preview_clock.timeout.connect(self.update_preview)
        self.preview_clock.start(round(1000 / self.PREVIEW_TICKS_PER_S))
    
    # refreshes the preview image and reloads the overlay, if necessary / if reload flag is set
    def update_preview(self):
        if(self.current_overlay is None):
            try:
                self.save_current()
            except:
                pass
        
        if(self.reload_overlay or self.current_overlay is None):
            try:
                self.current_overlay = cv.imread("./alignment-save.png")
                self.current_overlay = cv.cvtColor(self.current_overlay, cv.COLOR_BGRA2RGBA) # pyright: ignore[reportCallIssue, reportArgumentType]
                self.reload_overlay = False
            except:
                pass
        
        ret0, raw0 = self.capture0.read()
        ret1, raw1 = self.capture1.read()
        rs1 = cv.resize(raw1, raw1.shape[:2][::-1])     # We resize the second image to fit the first just in case theres a mismatch
                                                        # TODO: Check which image is bigger and match that
        self.raw_frame = cv.hconcat((raw0, rs1))        # we hconcat instead if vocncat for UI reasons
        self.raw_frame = cv.cvtColor(self.raw_frame, cv.COLOR_BGR2RGBA)
        
        if(self.frame_n < self.SKIP_FRAMES):
            self.frame_n += 1
            
        elif(self.frame_n == self.SKIP_FRAMES):
            self.frame_n = 0
            unfinished_result = self.detector.grab_skeleton(self.raw_frame, line_color_bgr=(0, 255, 0), line_thickness=5)
            self.overlay_result = cv.cvtColor(unfinished_result, cv.COLOR_BGRA2RGBA)
            
        else:
            self.frame_n = 0
        
        height, width, channel = self.overlay_result.shape
        bytesPerLine = 4 * width
        
        try:
            combined = cv.add(self.raw_frame, self.current_overlay) # pyright: ignore[reportArgumentType, reportCallIssue]
        except:
            combined = self.raw_frame
        combined = cv.add(combined, self.overlay_result)
        combined = combined
        qImg = QImage(combined.data, width, height, bytesPerLine, QImage.Format.Format_RGBA8888)    
        pixmap = QPixmap.fromImage(qImg).scaledToWidth(2300, Qt.TransformationMode.FastTransformation)
        self.imageLabel.setPixmap(pixmap)
    
    def save_current(self):
        img = self.detector.grab_skeleton(self.raw_frame, line_color_bgr=(127, 0, 255), line_thickness=5)
        cv.imwrite("./alignment-save.png", cv.cvtColor(img, cv.COLOR_BGRA2RGBA))
        self.reload_overlay = True
    
    def emit_wizard_done_signal(self):
        self.wizard_done_signal.emit()
