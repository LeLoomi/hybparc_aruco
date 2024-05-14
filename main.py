from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QLineEdit, QWidget, QSpacerItem
from login_widget import LoginWidget

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # Window setup
        self.showMaximized()
        self.setWindowTitle('Hybparc EKG (Aruco)')


app = QApplication([])
window = MainWindow()
window.setCentralWidget(LoginWidget())

window.show()
app.exec()