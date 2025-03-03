from PyQt6.QtWidgets import QDialogButtonBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QDialog
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import *

class TipsDialog(QDialog):
    
    current_tip = 0
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tipps")
        
        self.firstWidgetDisplayed = False

        self.svgWidget = QSvgWidget()

        self.pngWidget = QLabel()

        self.mainTipLabel = QLabel()
        font = self.mainTipLabel.font()
        font.setPointSize(28)
        self.mainTipLabel.setFont(font)

        self.goBackButton = QPushButton(" Zurück")
        pixmapBackwardButton = QPixmap("./graphics/angle-left-solid.svg")
        self.goBackButton.setIcon(QIcon(pixmapBackwardButton))
        self.goBackButton.setIconSize(QSize(26, 26))
        self.goBackButton.setFont(font)
        self.goBackButton.clicked.connect(self.backward_btn_clicked)

        okButton = QPushButton("Ok")
        okButton.setFont(font)
        okButton.clicked.connect(self.close)

        self.goForwardButton = QPushButton("Weiter ")
        pixmapForwardButton = QPixmap("./graphics/angle-right-solid.svg")
        self.goForwardButton.setIcon(QIcon(pixmapForwardButton))
        self.goForwardButton.setIconSize(QSize(26, 26))
        self.goForwardButton.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.goForwardButton.setFont(font)
        self.goForwardButton.clicked.connect(self.forward_btn_clicked)

        buttonBox = QDialogButtonBox()
        buttonBox.addButton(okButton, QDialogButtonBox.ButtonRole.AcceptRole)
        buttonBox.addButton(self.goForwardButton, QDialogButtonBox.ButtonRole.ActionRole)
        buttonBox.setMinimumHeight(100)

        upperLayout = QVBoxLayout()
        upperLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upperLayout.addStretch()
        upperLayout.addWidget(self.svgWidget)
        upperLayout.addWidget(self.pngWidget)
        upperLayout.addWidget(self.mainTipLabel)
        upperLayout.addStretch()

        buttonLayout = QHBoxLayout()
        buttonLayout.addSpacing(60)
        buttonLayout.addWidget(self.goBackButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(buttonBox)
        buttonLayout.addSpacing(60)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addSpacing(70)
        self.mainLayout.addLayout(upperLayout)
        self.mainLayout.addSpacing(70)
        self.mainLayout.addLayout(buttonLayout)

        self.setLayout(self.mainLayout)
        self.setFixedSize(1900, 850)
        
        self.load_tip(self.current_tip)

    def forward_btn_clicked(self):
        self.load_tip(self.current_tip + 1)
    
    def backward_btn_clicked(self):
        self.load_tip(self.current_tip - 1)

    def load_tip(self, index):
        self.current_tip = index
        self.svgWidget.setHidden(True)
        self.pngWidget.setHidden(True)
        
        # prod is py3.9 so we don't have switch statements...
        if index == 0:
            self.svgWidget.setHidden(False)
            self.svgWidget.load("./graphics/tip_distance.svg")
            self.svgWidget.setFixedSize(QSize(900, 292))    #this svgs aspect = 308:100
            self.mainTipLabel.setText("Die Elektroden sollten in der richtigen Reihenfolge angebracht <br> und nicht zu weit voneinander entfernt sein!")
            self.goBackButton.setEnabled(False)
            self.goForwardButton.setEnabled(True)
            
        elif index == 1:
            self.pngWidget.setHidden(False)
            self.pngWidget.setPixmap(QPixmap("./graphics/brustwandableitungen.png")) #this pngs aspect = 251:100
            self.pngWidget.setScaledContents(True)
            self.pngWidget.setFixedSize(QSize(1650, 657))
            self.mainTipLabel.setText("")
            self.goBackButton.setEnabled(True)
            self.goForwardButton.setEnabled(False)
