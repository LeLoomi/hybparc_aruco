from PyQt6.QtWidgets import QWidget, QDialogButtonBox, QHBoxLayout, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

class PlaceElectrodesWidget(QWidget):
    electrodes_placed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Setup ui
        iconLabel = QLabel()
        pixmap = QPixmap('./icons/ecg.svg')
        iconLabel.setPixmap(pixmap)

        textLabel = QLabel('Klebe nun die Elektroden an. <br>Drücke <b>danach</b> auf Ok. \nBitte achte darauf, dass die Marker an den Elektroden "zur Kamera hin schauen"!')
        textLabel.setTextFormat(Qt.TextFormat.RichText)

        font = textLabel.font()
        font.setPointSize(32)
        textLabel.setFont(font)

        iconTextLayout = QHBoxLayout()
        iconTextLayout.addStretch()
        iconTextLayout.addWidget(iconLabel)
        iconTextLayout.addWidget(textLabel)
        iconTextLayout.addStretch()

        buttonBox = QDialogButtonBox()
        okButton = buttonBox.addButton('Ok', QDialogButtonBox.ButtonRole.AcceptRole)
        okButton.setFont(font)
        okButton.setShortcut(Qt.Key.Key_Return)
        buttonBox.accepted.connect(self.emit_placed)

        contentLayout = QVBoxLayout()
        contentLayout.addStretch()
        contentLayout.addLayout(iconTextLayout)
        contentLayout.addWidget(buttonBox)
        contentLayout.addStretch()

        mainLayout = QHBoxLayout()
        mainLayout.addStretch()
        mainLayout.addLayout(contentLayout)
        mainLayout.addStretch()

        self.setLayout(mainLayout)
    
    def emit_placed(self):
        self.electrodes_placed.emit()