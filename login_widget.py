from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QLineEdit, QWidget, QComboBox, QFormLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette

class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Setup ui
        headerLabel = QLabel("<b>Hybparc-GUI: Login</b>")
        largeFont = headerLabel.font()
        largeFont.setPointSize(48)
        largeFont.setBold(True)
        headerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerLabel.setFont(largeFont)

        mediumFont = QFont()
        mediumFont.setPointSize(32)

        nameLabel = QLabel("Name:")
        nameLabel.setFont(mediumFont)
        idTypeLabel = QLabel("ID-Typ:")
        idTypeLabel.setFont(mediumFont)

        m_lineEditName = QLineEdit()
        m_lineEditName.setFont(mediumFont)

        m_comboBoxType = QComboBox()
        m_comboBoxType.addItem("ZIH (@tu-dresden.de)", 0)
        m_comboBoxType.addItem("MED (@med.tu-dresden.de)", 1)
        m_comboBoxType.setFont(mediumFont)

        formLayout = QFormLayout()
        formLayout.addRow(nameLabel, m_lineEditName)
        formLayout.addRow(idTypeLabel, m_comboBoxType)

        loginButton = QPushButton("Login")
        loginButton.clicked.connect(LoginWidget.attempt_login)
        loginButton.setShortcut(Qt.Key.Key_Return)
        loginButton.setFont(mediumFont)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(loginButton)

        #m_loginFailedLabel = QLabel("Bitte gültige ID eingeben.")
        #loginFailedLabelPalette = QPalette
        #loginFailedLabelPalette.setColor(self, QPalette.ColorGroup.Normal, QPalette.ColorRole.Base, Qt.GlobalColor.red)
        #m_loginFailedLabel.setPalette(loginFailedLabelPalette)
        #m_loginFailedLabel.setVisible(False)
        #m_loginFailedLabel.setFont(largeFont)

        elementsLayout = QVBoxLayout()
        elementsLayout.addWidget(headerLabel)
        elementsLayout.addSpacing(50)
        elementsLayout.addLayout(formLayout)
        elementsLayout.addLayout(buttonLayout)
        #elementsLayout.addWidget(m_loginFailedLabel)

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addStretch()
        horizontalLayout.addLayout(elementsLayout)
        horizontalLayout.addStretch()

        mainLayout = QVBoxLayout()
        mainLayout.addStretch()
        mainLayout.addLayout(horizontalLayout)
        mainLayout.addStretch()

        # Setup ui
        headerLabel = QLabel("<b>Hybparc-GUI: Login</b>")
        largeFont = headerLabel.font()
        largeFont.setPointSize(48)
        largeFont.setBold(True)
        headerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerLabel.setFont(largeFont)

        mediumFont = QFont()
        mediumFont.setPointSize(32)

        nameLabel = QLabel("Name:")
        nameLabel.setFont(mediumFont)
        idTypeLabel = QLabel("ID-Typ:")
        idTypeLabel.setFont(mediumFont)

        m_lineEditName = QLineEdit()
        m_lineEditName.setFont(mediumFont)

        m_comboBoxType = QComboBox()
        m_comboBoxType.addItem("ZIH (@tu-dresden.de)", 0)
        m_comboBoxType.addItem("MED (@med.tu-dresden.de)", 1)
        m_comboBoxType.setFont(mediumFont)

        formLayout = QFormLayout()
        formLayout.addRow(nameLabel, m_lineEditName)
        formLayout.addRow(idTypeLabel, m_comboBoxType)

        loginButton = QPushButton("Login")
        loginButton.clicked.connect(LoginWidget.attempt_login)
        loginButton.setShortcut(Qt.Key.Key_Return)
        loginButton.setFont(mediumFont)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(loginButton)

        #m_loginFailedLabel = QLabel("Bitte gültige ID eingeben.")
        #loginFailedLabelPalette = QPalette()
        #loginFailedLabelPalette.setColor(QPalette.windowText, Qt.GlobalColor.red)
        #m_loginFailedLabel.setPalette(loginFailedLabelPalette)
        #m_loginFailedLabel.setVisible(False)
        #m_loginFailedLabel.setFont(largeFont)

        elementsLayout = QVBoxLayout()
        elementsLayout.addWidget(headerLabel)
        elementsLayout.addSpacing(50)
        elementsLayout.addLayout(formLayout)
        elementsLayout.addLayout(buttonLayout)
        #elementsLayout.addWidget(m_loginFailedLabel)

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addStretch()
        horizontalLayout.addLayout(elementsLayout)
        horizontalLayout.addStretch()

        mainLayout = QVBoxLayout()
        mainLayout.addStretch()
        mainLayout.addLayout(horizontalLayout)
        mainLayout.addStretch()

        self.setLayout(mainLayout)

    
    def attempt_login():
        pass