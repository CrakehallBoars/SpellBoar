import sys

from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6 import QtGui

import cv2

from card_identificator import CardIdentificator
from card_separator import CardSeparator

class InterfaceManager():
    def __init__(self) -> None:
        self.camera = cv2.VideoCapture(0)

        self.window_setup()

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start(33)

        self.card_separator = CardSeparator()
        self.card_identificator = CardIdentificator()
        

    def window_setup(self) -> None:
        self.app = QtWidgets.QApplication([])

        self.main_window = QtWidgets.QMainWindow()
        self.main_window.setWindowTitle("SpellBoar")

        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.main_window.setCentralWidget(main_widget)

        self.camera_viewport = QtWidgets.QLabel()
        main_layout.addWidget(self.camera_viewport)

        self.main_window.show()

    
    def update(self) -> None:
        ret, frame = self.camera.read()
        self.frame = frame

        converted_image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                                       QtGui.QImage.Format.Format_BGR888)
        
        self.camera_viewport.setPixmap(QtGui.QPixmap.fromImage(converted_image))

    def run(self) -> None:
        sys.exit(self.app.exec())


    ## PLACEHOLDER
    def on_card_click(self, pos_x: int, pos_y: int) -> None:
        separated_card = self.card_separator.separate_card(self.frame, pos_x, pos_y)

        identified_card = self.card_identificator.identify_card(separated_card)