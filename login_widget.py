from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QLineEdit, QWidget, QComboBox, QFormLayout, QHBoxLayout, QSpacerItem
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class LoginWidget(QWidget):
    loginSuccessful = pyqtSignal(str, str)
    
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
        mediumFont.setPointSize(28)
        
        nameLabel = QLabel("Login-Name:")
        nameLabel.setFont(mediumFont)
        idTypeLabel = QLabel("ID-Typ:")
        idTypeLabel.setFont(mediumFont)

        self.m_lineEditName = QLineEdit()
        self.m_lineEditName.setMinimumWidth(300)
        self.m_lineEditName.setFont(mediumFont)

        self.m_comboBoxType = QComboBox()
        self.m_comboBoxType.setMinimumWidth(300)
        self.m_comboBoxType.addItem("ZIH (@tu-dresden.de)", 0)
        self.m_comboBoxType.addItem("MED (@med.tu-dresden.de)", 1)
        self.m_comboBoxType.setFont(mediumFont)

        loginButton = QPushButton("Login")
        loginButton.clicked.connect(self.attempt_login)
        loginButton.setShortcut(Qt.Key.Key_Return)
        loginButton.setFont(mediumFont)
        loginButton.setMaximumWidth(150)

        buttonLayout = QHBoxLayout()
        #buttonLayout.addStretch()
        buttonLayout.addWidget(loginButton)

        formLayout = QFormLayout()
        formLayout.addRow(nameLabel, self.m_lineEditName)
        formLayout.addRow(idTypeLabel, self.m_comboBoxType)
        formLayout.addRow(buttonLayout)
        
        self.m_loginFailedLabel = QLabel("Bitte gültige ID eingeben.")
        self.m_loginFailedLabel.setVisible(False)
        self.m_loginFailedLabel.setFont(mediumFont)

        elementsLayout = QVBoxLayout()
        elementsLayout.addWidget(headerLabel)
        elementsLayout.addSpacing(50)
        elementsLayout.addLayout(formLayout)
        elementsLayout.addLayout(buttonLayout)
        elementsLayout.addWidget(self.m_loginFailedLabel)

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addStretch()
        horizontalLayout.addLayout(elementsLayout)
        horizontalLayout.addStretch()

        mainLayout = QVBoxLayout()
        mainLayout.addStretch()
        mainLayout.addLayout(horizontalLayout)
        mainLayout.addStretch()

        self.setLayout(mainLayout)

    def attempt_login(self):
        if self.m_lineEditName.text() == '':
            self.m_loginFailedLabel.setVisible(True)
            return
        else:
            login_type = 'tu-dresden.de' if self.m_comboBoxType.currentIndex() == 0 else 'med.tu-dresden.de'
            self.loginSuccessful.emit(self.m_lineEditName.text(), login_type)