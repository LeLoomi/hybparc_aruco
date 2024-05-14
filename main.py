from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt

app = QApplication([])
window = QMainWindow()

# Window setup
window.showFullScreen()
window.setWindowTitle('Hybparc EKG (Aruco)')


# Widgets
label = QLabel('MITZ x NCT Hybparc EKG Training', alignment=Qt.AlignmentFlag.AlignLeading)
window.setCentralWidget(label)

window.show()
app.exec()