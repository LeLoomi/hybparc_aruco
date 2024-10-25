from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QTreeWidget, QVBoxLayout, QTreeWidgetItem, QDialogButtonBox
from PyQt6.QtGui import QPixmap, QIcon, QMovie
from PyQt6.QtCore import QSize

class ResultsWidget(QWidget):
    
    def __init__(self, config_data, roi_statuses):
        super().__init__()
        self.roi_statuses = roi_statuses
    
        # loop align markers/"big body regions" like torso
        rois = list()   # to store the individual rois
        for big_region in config_data['region_marker']:
            # loop rois in the big regions
            for roi in big_region['rois']:
                rois.append(roi)
    
        allDetectionsCorrect = True
    
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

        print('\n')
        print(self.roi_statuses)
        print('\n')

        for roi in rois:
            # Create a item for each detected electrode
            item = QTreeWidgetItem()
            item.setText(0, '{} ({})'.format(roi['reg_name'], roi['reg_desc']))
            item.setIcon(0, QIcon('./icons/wrong.svg'))
            
            # update icon to being correct in case the electrode is in the right spot
            try:
                if self.roi_statuses[roi['desired_marker_id']]['fullfilled']:
                    item.setIcon(0, QIcon('./icons/correct.svg'))
            except:
                # if we end up here, not all desired markers were detected (no biggie, hopefully)
                print('[Hybparc] {} was not detected!'.format(roi['desired_marker_id']))

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
