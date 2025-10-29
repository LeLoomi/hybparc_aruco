from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QImage
import cv2 as cv

class AlignmentWizardWidget(QWidget):
    
    PREVIEW_TICKS_PER_S = 30
    SKIP_FRAMES = 15
    
    wizard_done_signal = pyqtSignal()
    
    reload_overlay = True
    saved_skeleton = None
    preview_clock = QTimer()
    
    def __init__(self, arucoroi_detector, capture0: cv.VideoCapture, capture1: cv.VideoCapture):
        super().__init__()

        self.detector = arucoroi_detector
        self.capture0 = capture0
        self.capture1 = capture1

        explainer_label = QLabel("<b>Willkommen bei der Kamera-Einstellungshilfe</b> <br>Die pinken Boxen des Overlays sollten gut mit den in Grün markierten Markerkanten übereinstimmen. Im Idealfall \"verschwimmen\" sie mit den jeweiligen Kantenmarkierungen. Leichte Abweichungen sind in der Regel aber nicht schlimm.  In der Einstellungshilfe sind nur Marker interessant, welche an der Puppe angebracht sind.")

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
        if(self.saved_skeleton is None):
            try:
                self.save_current()
            except:
                pass
        
        if(self.reload_overlay or self.saved_skeleton is None):
            try:
                self.saved_skeleton = cv.imread("./alignment-save.png")
                self.saved_skeleton = cv.cvtColor(self.saved_skeleton, cv.COLOR_BGRA2RGBA) # pyright: ignore[reportCallIssue, reportArgumentType]
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
            self.current_live_skeleton = self.detector.grab_skeleton(self.raw_frame, line_color_bgr=(0, 255, 0), line_thickness=3)
            
        else:
            self.frame_n = 0
        
        height, width, channel = self.current_live_skeleton.shape
        bytesPerLine = 4 * width
        
        try:
            raw_with_saved_skeleton = self.overlay_opaque(self.raw_frame, self.saved_skeleton) # pyright: ignore[reportArgumentType, reportCallIssue]
        except: 
            # if we don't have a saved overlay
            raw_with_saved_skeleton = self.raw_frame
        
        print(self.current_live_skeleton.shape, self.current_live_skeleton[..., 3].min(), self.current_live_skeleton[..., 3].max())
        raw_with_both = self.overlay_opaque(raw_with_saved_skeleton, self.current_live_skeleton)
        
        qImg = QImage(
            raw_with_both.data, 
            width, 
            height, 
            bytesPerLine, 
            QImage.Format.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qImg).scaledToWidth(2300, Qt.TransformationMode.FastTransformation)  # 2300 is a good fit for our local scrren setup
        self.imageLabel.setPixmap(pixmap)
    
    def save_current(self):
        img = self.detector.grab_skeleton(self.raw_frame, line_color_bgr=(255, 0, 127), line_thickness=7)
        cv.imwrite("./alignment-save.png", cv.cvtColor(img, cv.COLOR_BGRA2RGBA))
        self.reload_overlay = True
    
    # ! assumes, that the two images are the same size
    # https://docs.opencv.org/3.4/d0/d86/tutorial_py_image_arithmetics.html
    @staticmethod
    def overlay_opaque(base_img: cv.typing.MatLike, overlay_img: cv.typing.MatLike) -> cv.typing.MatLike:
        # create mask from non-black pixels in overlay
        gray = cv.cvtColor(overlay_img, cv.COLOR_BGRA2GRAY)  # threshold needs single channel grayscale image
        ret, mask = cv.threshold(gray, 10, 255, cv.THRESH_BINARY)
        mask_inv = cv.bitwise_not(mask)

        # use mask to clear out pixels
        background = cv.bitwise_and(base_img, base_img, mask=mask_inv)
        foreground = cv.bitwise_and(overlay_img, overlay_img, mask=mask)
        combined = cv.add(background, foreground)

        return combined
    
    def emit_wizard_done_signal(self):
        self.wizard_done_signal.emit()
