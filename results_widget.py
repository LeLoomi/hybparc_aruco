from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QTreeWidget, QVBoxLayout, QTreeWidgetItem, QDialogButtonBox
from PyQt6.QtGui import QPixmap, QIcon, QMovie, QFont
from PyQt6.QtCore import QSize, pyqtSignal
from tips_dialog import TipsDialog

class ResultsWidget(QWidget):
    
    retry_triggered = pyqtSignal()
    
    def __init__(self, config_data, roi_statuses):
        super().__init__()
        self.roi_statuses = roi_statuses
    
        # loop config for align markers/"big body regions" like torso
        rois = list()   # to store the individual rois
        for big_region in config_data['region_marker']:
            # loop rois in the big regions
            for roi in big_region['rois']:
                rois.append(roi)
    
        # we make a list of markers and add all wrong ones to it
        # if any are on it, we can work with this
        # TODO if needed otherwise we might have to flip the entire concept but that might require a rewrite of what ArucoRoi returns; mb
        wrongMarkers = list()
        

        font = QFont()
        font.setPointSize(32)

        # building the central table UI
        treeWidget = QTreeWidget()
        treeWidget.headerItem().setText(0, 'Elektrodenstatus')

        # loop all desired ROIs and make list entries, we also check which are right and wrong here
        # TODO move the analysis outside of the UI building??!?!?!??!! Would be nice ngl
        for roi in rois:
            # Create a item for each detected electrode
            item = QTreeWidgetItem()
            
            wanted = roi['desired_marker_id']
            
            # update icon and text to being correct in case the electrode is in the right spot
            try:
                if self.roi_statuses[roi['desired_marker_id']]['fulfilled']:
                    item.setText(0, '{}'.format(roi['reg_name']))
                    item.setIcon(0, QIcon('./icons/check-solid.svg'))
                    print('[Hybparc] \U0001F44D {} was in the RIGHT spot!'.format(wanted))
                else:
                    item.setText(0, '{} ({})'.format(roi['reg_name'], roi['reg_desc']))
                    item.setIcon(0, QIcon('./icons/xmark-solid.svg'))
                    wrongMarkers.append(wanted)
                    print('[Hybparc] \U0001F44E {} was in the WRONG spot!'.format(wanted))
            except:
                # if we end up here, not all desired markers were detected (no biggie, hopefully)
                item.setText(0, '{} ({})'.format(roi['reg_name'], roi['reg_desc']))
                item.setIcon(0, QIcon('./icons/eye-slash-solid.svg'))
                wrongMarkers.append(wanted)
                print('[Hybparc] \U0001F6A8 {} was NOT detected!'.format(wanted))

            treeWidget.insertTopLevelItem(treeWidget.topLevelItemCount(), item)
        
        treeWidget.expandAll()
        treeWidget.setFixedHeight(600)
        treeWidget.setIconSize(QSize(30, 30))
        treeWidget.setFont(font)
        
        eyeExplainer = QLabel("Elektroden mit Augensymbol konnten nicht gefunden werden. Überprüfe dann,\nob Marker verdeckt sind, oder nicht zur Kamera zeigen.")
        eyeFont = QFont(font)
        eyeFont.setPointSize(24)
        eyeExplainer.setFont(eyeFont)

        # short logic check we can reuse down the line
        allDetectionsCorrect = len(wrongMarkers) == 0

        # Create upper UI, we do it down here so we have our analysis already
        feedbackLabel = QLabel(
                'Alle Elektroden wurden richtig erkannt! Prima!'
                if allDetectionsCorrect else
                'Das sieht noch nicht ganz richtig aus. Versuch es nochmal.'
            )

        #font = feedbackLabel.font()
        font.setPointSize(32)
        feedbackLabel.setFont(font)

        upperLayout = QHBoxLayout()
        iconLabel = QLabel()
        pixmap = QPixmap('./icons/check-solid.svg' if allDetectionsCorrect else './icons/xmark-solid.svg') 
        scaledPixmap = pixmap.scaledToHeight(100)

        iconLabel.setPixmap(scaledPixmap)
        upperLayout.addWidget(iconLabel)
        upperLayout.addWidget(feedbackLabel)

        # create lower UI
        buttonBox = QDialogButtonBox()
        movie = QMovie('./gifs/bulb_flashing.gif')

        retryButton = buttonBox.addButton('Neuer Versuch', QDialogButtonBox.ButtonRole.AcceptRole)
        retryButton.setFont(font)
        buttonBox.accepted.connect(self.emit_retry_triggered)
        
        helpButton = buttonBox.addButton('Tipps', QDialogButtonBox.ButtonRole.HelpRole)
        helpButton.setFont(font)
        helpButton.clicked.connect(self.help_button_clicked)

        # assemble it all together
        contentLayout = QVBoxLayout()
        contentLayout.addStretch()
        contentLayout.addLayout(upperLayout)
        contentLayout.addWidget(treeWidget)
        
        contentLayout.addWidget(eyeExplainer)

        contentLayout.addWidget(buttonBox)
        contentLayout.addStretch()

        mainLayout = QHBoxLayout()
        mainLayout.addStretch()
        mainLayout.addLayout(contentLayout)
        mainLayout.addStretch()
        
        self.setLayout(mainLayout)

    def emit_retry_triggered(self):
        self.retry_triggered.emit()
    
    def help_button_clicked(self):
        dialog = TipsDialog()
        dialog.exec()