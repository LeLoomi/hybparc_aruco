from PyQt6.QtWidgets import QDialogButtonBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QDialog
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import *

class TipsDialog(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tipps")
        
        self.svgWidget = QSvgWidget()
        self.firstWidgetDisplayed = False
        
        self.svgWidget.setFixedSize(QSize(400, 150))

        self.mainTipLabel = QLabel()

        font = self.mainTipLabel.font()
        font.setPointSize(24)
        self.mainTipLabel.setFont(font)

        self.goBackButton = QPushButton(" Zurück")
        pixmapBackwardButton = QPixmap("./icons/angle-left-solid.svg")
        self.goBackButton.setIcon(QIcon(pixmapBackwardButton))
        self.goBackButton.setIconSize(QSize(20, 20))
        self.goBackButton.setFont(font)
        self.goBackButton.clicked.connect(self.backward_btn_clicked)

        okButton = QPushButton("Ok")
        okButton.setFont(font)
        okButton.clicked.connect(self.close)

        self.goForwardButton = QPushButton("Weiter ")
        pixmapForwardButton = QPixmap("./icons/angle-right-solid.svg")
        self.goForwardButton.setIcon(QIcon(pixmapForwardButton))
        self.goForwardButton.setIconSize(QSize(20, 20))
        self.goForwardButton.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.goForwardButton.setFont(font)
        self.goForwardButton.clicked.connect(self.forward_btn_clicked)

        buttonBox = QDialogButtonBox()
        buttonBox.addButton(okButton, QDialogButtonBox.ButtonRole.AcceptRole)
        buttonBox.addButton(self.goForwardButton, QDialogButtonBox.ButtonRole.ActionRole)
        buttonBox.setMinimumHeight(100)

        upperLayout = QHBoxLayout()
        upperLayout.addStretch()
        upperLayout.addWidget(self.svgWidget)
        upperLayout.addWidget(self.mainTipLabel)
        upperLayout.addStretch()

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.goBackButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(buttonBox)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addSpacing(100)
        self.mainLayout.addLayout(upperLayout)
        self.mainLayout.addSpacing(100)
        self.mainLayout.addLayout(buttonLayout)

        self.setLayout(self.mainLayout)
        self.setFixedSize(1600, 500)
        
        self.navigateThroughElements()

    def forward_btn_clicked(self):
        self.firstWidgetDisplayed = True
        self.navigateThroughElements()
    
    def backward_btn_clicked(self):
        self.firstWidgetDisplayed = False
        self.navigateThroughElements()

    def navigateThroughElements(self):
        tips = [ "Die Elektroden sollten in der richtigen Reihenfolge angebracht <br> und nicht zu weit voneinander entfernt sein!",
            "Stelle sicher, dass die Elektroden komplett aufliegen." ]
        
        self.svgWidget.load("./icons/tip_placement.svg" if self.firstWidgetDisplayed else "./icons/tip_distance.svg")
        self.svgWidget.setFixedSize(QSize(750 if self.firstWidgetDisplayed else 450, 140))
        
        self.mainTipLabel.setText(tips[0] if not self.firstWidgetDisplayed else tips[1])
        self.goBackButton.setEnabled(self.firstWidgetDisplayed)
        self.goForwardButton.setDisabled(self.firstWidgetDisplayed)