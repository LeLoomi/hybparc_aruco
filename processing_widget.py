from PyQt6.QtWidgets import QWidget, QDialogButtonBox, QHBoxLayout, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QTimer

#include <QTimer>

class ProcessingWidget(QWidget):
    
    processing_complete = pyqtSignal()
    
    def __init__(self):
        super().__init__()
    
        # Setup ui
        self.iconLabel = QLabel()
        pixmap = QPixmap('./icons/correct.svg')
        scaledPixmap = pixmap.scaled(QSize(250, 200))
        self.iconLabel.setPixmap(scaledPixmap)
        self.iconLabel.setVisible(False)

        self.textLabel = QLabel('Berechne Daten. Bitte trete von der Puppe zurück und berühre diese nicht mehr.')
        self.textLabel.setTextFormat(Qt.TextFormat.RichText)

        font = self.textLabel.font()
        font.setPointSize(32)
        self.textLabel.setFont(font)

        self.gifLabel = QLabel()
        self.movie = QMovie('./gifs/animation.gif')
        self.movie.setScaledSize(QSize(200, 200))
        self.gifLabel.setMovie(self.movie)
        self.gifLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        iconTextLayout = QHBoxLayout()
        iconTextLayout.addStretch()
        iconTextLayout.addWidget(self.iconLabel)
        iconTextLayout.addWidget(self.textLabel)
        iconTextLayout.addStretch()

        self.buttonBox = QDialogButtonBox()
        okButton = self.buttonBox.addButton('Ok', QDialogButtonBox.ButtonRole.AcceptRole)
        okButton.setFont(font)
        self.buttonBox.setVisible(False)

        contentLayout = QVBoxLayout()
        contentLayout.addStretch()
        contentLayout.addLayout(iconTextLayout)
        contentLayout.addSpacing(50)
        contentLayout.addWidget(self.gifLabel)
        contentLayout.addWidget(self.buttonBox)
        contentLayout.addStretch()

        mainLayout = QHBoxLayout()
        mainLayout.addStretch()
        mainLayout.addLayout(contentLayout)
        mainLayout.addStretch()

        self.setLayout(mainLayout)
        self.movie.start()

        isFirstTry = False
        QTimer.singleShot(1000 if isFirstTry else 1000, lambda: self.handle_timeout(
            self.iconLabel, self.textLabel, self.gifLabel, self.movie, self.buttonBox))

    # We go here after fake processing time
    def handle_timeout(self, iconLabel, textLabel, gifLabel, movie, buttonBox):
        iconLabel.setVisible(True)
        movie.stop()
        gifLabel.setVisible(False)
        textLabel.setText('Auswertung erfolgreich! <br> Klicke auf Ok, um fortzufahren.')
        buttonBox.setVisible(True)
        
        self.processing_complete.emit()
