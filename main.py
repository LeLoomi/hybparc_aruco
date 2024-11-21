import cv2 as cv    # sadly we have to load cv here, since we use it to capture the images
from lib.detector import Detector
from PyQt6.QtWidgets import QApplication, QMainWindow
from welcome_widget import WelcomeWidget
from login_widget import LoginWidget
from place_electrodes_widget import PlaceElectrodesWidget
from processing_widget import ProcessingWidget
from results_widget import ResultsWidget
from qt_material import apply_stylesheet    # optional prettifier
from json import load

class MainWindow(QMainWindow):
    
    config_path = './roi-config-mockup.json'
    
    roi_statuses = dict()
    
    # Entry into the GUI
    def __init__(self):
        print('[Hybparc] Booting up')
        super().__init__()
        
        # Detector setup, loaded file is the ROI config
        self.detector = Detector(self.config_path)
        
        # load config file so we can construct the UI accordingly later
        with open(self.config_path, 'r') as f:
            self.config_data = load(f)
        
        # Window setup
        self.showMaximized()
        self.setWindowTitle('Hybparc EKG (Aruco)')
        self.show_welcome_widget()

    # Welcome screen on the 
    def show_welcome_widget(self):
        print('[Hybparc] Diplaying login widget')
        welcome_widget = WelcomeWidget()
        welcome_widget.start_pressed.connect(self.show_place_electrodes)
        self.setCentralWidget(welcome_widget)

    # Helper func for login_widget
    def set_login_info(self, login_name, login_domain):
        print('[Hybparc] Logged in as {}@{}'.format(login_name, login_domain))
        self.login_name = login_name
        self.login_domain = login_domain

    # For loggin in with your institution, so your result can be uploaded (CURRENTLY DEPRECATED)
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
        
        # Setup and warm up cameras
        self.stream0 = cv.VideoCapture(index=0, apiPreference=cv.CAP_ANY)
        self.stream1 = cv.VideoCapture(index=1, apiPreference=cv.CAP_ANY)
    
    def show_processing_widget(self):
        print('[Hybparc] Displaying processing widget')
        
        # show ui, disappears after time by its own (fake loading screen to give cams time)
        processing_widget = ProcessingWidget()
        processing_widget.processing_complete.connect(self.show_results_widget)
        self.setCentralWidget(processing_widget)
        
        # ! DETECTION CALL
        for i in range(3):  # we do n passes of analysis and aggregate the correct detections.
            ret0, in0 = self.stream0.read()
            ret1, in1 = self.stream1.read()
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
        self.stream0.release()
        self.stream1.release()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    apply_stylesheet(app, theme='light_blue.xml')
    window.show()
    app.exec()