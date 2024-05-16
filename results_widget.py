from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QTreeWidget, QVBoxLayout, QTreeWidgetItem, QDialogButtonBox, QPushButton
from PyQt6.QtGui import QPalette, QColor, QPixmap, QIcon, QMovie
from PyQt6.QtCore import QSize

class ResultsWidget(QWidget):
    
    def __init__(self, electrode_detections):
        super().__init__()
        self.correct_electrodes = electrode_detections
    
        # Create ui
        allDetectionsCorrect = True

        feedbackLabel = QLabel(
                'Alle Elektroden wurden richtig erkannt! Prima!'
                if allDetectionsCorrect else
                'Das sieht noch nicht ganz richtig aus. Versuch es nochmal.'
            )

        font = feedbackLabel.font()
        font.setPointSize(32)
        feedbackLabel.setFont(font)

        palette = feedbackLabel.palette()
        palette.setColor(QPalette.ColorGroup.Normal, QPalette.ColorRole.Base, QColor(98, 122, 54) if allDetectionsCorrect else QColor(166, 110, 38))
        feedbackLabel.setPalette(palette)

        upperLayout = QHBoxLayout()
        if allDetectionsCorrect:
            iconLabel = QLabel()
            pixmap = QPixmap('./icons/correct.svg')
            scaledPixmap = pixmap.scaled(QSize(250, 200))

            iconLabel.setPixmap(scaledPixmap)
            upperLayout.addWidget(iconLabel)

        upperLayout.addWidget(feedbackLabel)

        treeWidget = QTreeWidget()
        treeWidget.headerItem().setText(0, 'Elektrodenstatus')

        for key in self.correct_electrodes.keys():
            # Create a item for each detected electrode
            item = QTreeWidgetItem()
            item.setText(0, self.correct_electrodes[key]['roi_name'])
            #item.setIcon(0, QIcon(detection.isCorrect ? './icons/correct.svg' : './icons/wrong.svg'))

            # Set the icon
            #if (!detection.isCorrect) {
                # For misaligned electrodes, create a child item suggesting the correct positioning
            #    const placementSuggestion = getPlacementSuggestion(detection.name)
            #    item.setText(0, item.text(0) + ' - ' + placementSuggestion)
            #}

            treeWidget.insertTopLevelItem(treeWidget.topLevelItemCount(), item)

        treeWidget.expandAll()
        treeWidget.setIconSize(QSize(40, 40))
        treeWidget.setFont(font)
        treeWidget.setFixedHeight(treeWidget.topLevelItemCount() * 70 + 80)

        buttonBox = QDialogButtonBox()
        movie = QMovie('./gifs/bulb_flashing.gif')

        logoutButton = buttonBox.addButton('Logout', QDialogButtonBox.ButtonRole.AcceptRole)
        logoutButton.setFont(font)
        helpButton = buttonBox.addButton('Tipps', QDialogButtonBox.ButtonRole.HelpRole)
        helpButton.setFont(font)

        contentLayout = QVBoxLayout()
        contentLayout.addStretch()
        contentLayout.addLayout(upperLayout)
        contentLayout.addWidget(treeWidget)

        contentLayout.addWidget(buttonBox)
        contentLayout.addStretch()

        mainLayout = QHBoxLayout()
        mainLayout.addStretch()
        mainLayout.addLayout(contentLayout)
        mainLayout.addStretch()
        
        self.setLayout(mainLayout)
