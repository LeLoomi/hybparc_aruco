from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QTreeWidget, QVBoxLayout, QTreeWidgetItem, QDialogButtonBox
from PyQt6.QtGui import QPixmap, QIcon, QMovie
from PyQt6.QtCore import QSize

class ResultsWidget(QWidget):
    
    def __init__(self, roi_statuses):
        super().__init__()
        self.roi_statuses = roi_statuses
    
        # default all correct, if one is incorrect set false flag
        allDetectionsCorrect = True
        for key in roi_statuses:
            if roi_statuses[key]['fullfilled'] == False:
                allDetectionsCorrect = False
    
        # Create ui
        feedbackLabel = QLabel(
                'Alle Elektroden wurden richtig erkannt! Prima!'
                if allDetectionsCorrect else
                'Das sieht noch nicht ganz richtig aus. Versuch es nochmal.'
            )

        font = feedbackLabel.font()
        font.setPointSize(32)
        feedbackLabel.setFont(font)

        upperLayout = QHBoxLayout()
        iconLabel = QLabel()
        pixmap = QPixmap('./icons/correct.svg' if allDetectionsCorrect else './icons/wrong.svg') 
        scaledPixmap = pixmap.scaled(QSize(100, 100))

        iconLabel.setPixmap(scaledPixmap)
        upperLayout.addWidget(iconLabel)
        upperLayout.addWidget(feedbackLabel)

        treeWidget = QTreeWidget()
        treeWidget.headerItem().setText(0, 'Elektrodenstatus')

        for key in self.roi_statuses.keys():
            # Create a item for each detected electrode
            item = QTreeWidgetItem()
            item.setText(0,
                self.roi_statuses[key]['roi_name'] + '({})'.format(self.roi_statuses[key]['roi_desc'])
            )
            item.setIcon(0, 
                QIcon('./icons/correct.svg' if roi_statuses[key]['fullfilled'] == True else './icons/wrong.svg'))

            # Set the icon
            #if (!detection.isCorrect) {
                # For misaligned electrodes, create a child item suggesting the correct positioning
            #    const placementSuggestion = getPlacementSuggestion(detection.name)
            #    item.setText(0, item.text(0) + ' - ' + placementSuggestion)
            #}

            treeWidget.insertTopLevelItem(treeWidget.topLevelItemCount(), item)

        treeWidget.expandAll()
        treeWidget.setIconSize(QSize(30, 30))
        treeWidget.setFont(font)

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
