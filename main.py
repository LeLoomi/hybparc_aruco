from ArucoRoi.detector import Detector
from cv2 import imread
from PyQt6.QtWidgets import QApplication, QMainWindow
from login_widget import LoginWidget
from place_electrodes_widget import PlaceElectrodesWidget
from processing_widget import ProcessingWidget
from results_widget import ResultsWidget

class MainWindow(QMainWindow):
    
    # Entry into the GUI
    def __init__(self):
        print('[Hybparc] Booting up')
        super().__init__()
        
        # Detector setup
        self.detector = Detector('./config.json')
        
        # Window setup
        self.showMaximized()
        self.setWindowTitle('Hybparc EKG (Aruco)')
        self.show_login_widget()

    def set_login_info(self, login_name, login_domain):
        print('[Hybparc] Logged in as {}@{}'.format(login_name, login_domain))
        self.login_name = login_name
        self.login_domain = login_domain

    # First displayed widget
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
    
    def show_processing_widget(self):
        print('[Hybparc] Displaying processing widget')
        
        # show ui, disappears after time by its own (fake loading screen)
        processing_widget = ProcessingWidget()
        processing_widget.processing_complete.connect(self.show_results_widget)
        self.setCentralWidget(processing_widget)
        
        # actually run detection (this should work by its own)
        frame = imread('./tmp/test1.png')
        result_frame, self.roi_statuses = self.detector.image_detect(frame) # ! DETECTION CALL

    def show_results_widget(self):
        print('[Hybparc] Displaying results widget')
        results_widget = ResultsWidget(self.roi_statuses)
        #results_widget.retry_triggered.connect(self.show_place_electrodes)
        self.setCentralWidget(results_widget)
    
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()