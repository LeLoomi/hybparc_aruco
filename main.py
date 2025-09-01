import cv2 as cv    # sadly we have to load cv here, since we use it to capture the images
from lib.detector import Detector
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from welcome_widget import WelcomeWidget
from login_widget import LoginWidget
from place_electrodes_widget import PlaceElectrodesWidget
from processing_widget import ProcessingWidget
from results_widget import ResultsWidget
from alignment_wizard_widget import AlignmentWizardWidget
from json import load
from time import sleep

class MainWindow(QMainWindow):
    
    config_path = './mitz-ekg-config.json'
    detector_passes = 7
    warmup_passes = 11
    
    roi_statuses = dict()
    
    # Entry into the GUI
    def __init__(self):
        print('[Hybparc] Booting up')
        super().__init__()
        
        # ! TMP
        self.showMaximized()
        self.setWindowTitle('Hybparc EKG (Aruco)')
        self.detector = Detector(self.config_path)
        
        # Detector setup, loaded file is the ROI config
        self.detector = Detector(self.config_path)
        
        # load config file so we can construct the UI accordingly later
        with open(self.config_path, 'r') as f:
            self.config_data = load(f)
        
        # Setup and warm up cameras
        #! Adjustments are specific to the HP 960 4K in our physical setup
        self.stream0 = cv.VideoCapture(index=0, apiPreference=cv.CAP_ANY)
        self.stream0.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        self.stream0.set(cv.CAP_PROP_FRAME_WIDTH, 3840)
        self.stream0.set(cv.CAP_PROP_FRAME_HEIGHT, 2160)
        self.stream1 = cv.VideoCapture(index=4, apiPreference=cv.CAP_ANY)
        self.stream1.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        self.stream1.set(cv.CAP_PROP_FRAME_WIDTH, 3840)
        self.stream1.set(cv.CAP_PROP_FRAME_HEIGHT, 2160)
        
        # Window setup
        self.showMaximized()
        self.setWindowTitle('Hybparc EKG (Aruco)')
        self.show_welcome_widget()

    # Welcome screen on the 
    def show_welcome_widget(self):
        print('[Hybparc] Diplaying welcome widget')
        welcome_widget = WelcomeWidget()
        welcome_widget.start_pressed.connect(self.show_alignment_wizard)
        self.setCentralWidget(welcome_widget)
        
    def show_alignment_wizard(self):
        print('[Hybparc] Displaying alignemnt wizard widget')
        alignemt_wizard_widget = AlignmentWizardWidget(self.detector, self.stream0, self.stream1)
        alignemt_wizard_widget.wizard_done_signal.connect(self.show_place_electrodes)
        self.setCentralWidget(alignemt_wizard_widget)

    # Helper func for login_widget
    def set_login_info(self, login_name, login_domain):
        print('[Hybparc] Logged in as {}@{}'.format(login_name, login_domain))
        self.login_name = login_name
        self.login_domain = login_domain

    # For logging in with your institution, so your result can be uploaded (CURRENTLY DEPRECATED)
    def show_login_widget(self):
        print('[Hybparc] Diplaying login widget')
        login_widget = LoginWidget()
        login_widget.loginSuccessful.connect(self.set_login_info)
        login_widget.loginSuccessful.connect(self.show_place_electrodes)
        self.setCentralWidget(login_widget)

    # Displayed after successful login
    def show_place_electrodes(self):
        print('[Hybparc] Diplaying electrode placement widget')
        place_electrodes_widget = PlaceElectrodesWidget()
        place_electrodes_widget.electrodes_placed.connect(self.show_processing_widget)
        self.setCentralWidget(place_electrodes_widget)
        
        self.roi_statuses.clear()
    
    def show_processing_widget(self):
        print('[Hybparc] Displaying processing widget')
        
        # show ui, disappears after time by its own (fake loading screen to give cams time)
        processing_widget = ProcessingWidget()
        processing_widget.processing_complete.connect(self.show_results_widget)
        self.setCentralWidget(processing_widget)
        
        # ! DETECTION CALL
        for i in range(self.detector_passes + self.warmup_passes):  # we do n passes of analysis and aggregate the correct detections.
            sleep(0.05)
            ret0, in0 = self.stream0.read()
            ret1, in1 = self.stream1.read()
            
            # We take useless frames to warm up the autofocus
            if i <= self.warmup_passes:
                sleep(0.01)
                continue
            
            rs1 = cv.resize(in1, in0.shape[:2][::-1])   # We resize the second image to fit the first just in case theres a mismatch
                                                        # TODO: Check which image is bigger and match that
            frame = cv.vconcat((in0, rs1))
            result_frame, result_dict = self.detector.image_detect(frame)
            self.roi_statuses.update(result_dict)

    def show_results_widget(self):
        print('[Hybparc] Displaying results widget')
        results_widget = ResultsWidget(self.config_data, self.roi_statuses)
        results_widget.retry_triggered.connect(self.show_place_electrodes)
        self.setCentralWidget(results_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()