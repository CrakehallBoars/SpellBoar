import sys
import numpy

from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6 import QtGui

import cv2

from card_identificator import CardIdentificator
from card_separator import CardSeparator

class InterfaceManager():
    def __init__(self) -> None:
        # Configure camera capture
        self.camera = cv2.VideoCapture(0)

        self.window_setup()

        # Timer to update camera image
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

        # Label to display camera output
        self.camera_viewport = QtWidgets.QLabel()
        main_layout.addWidget(self.camera_viewport)

        # Define function to be triggered on mouse clicked
        self.camera_viewport.mousePressEvent = self.on_mouse_click

        self.main_window.show()

    def numpy_image_to_qimage(self, raw_image: numpy.ndarray) -> QtGui.QImage:
        height, width, _ = raw_image.shape
        converted_image = QtGui.QImage(raw_image, width, height, QtGui.QImage.Format.Format_BGR888)
        return converted_image
    
    def update(self) -> None:
        ret, frame = self.camera.read()
        
        camera_image = self.numpy_image_to_qimage(frame)

        self.camera_viewport.setPixmap(QtGui.QPixmap.fromImage(camera_image))

    def run(self) -> None:
        sys.exit(self.app.exec())


    def on_mouse_click(self, event: QtGui.QMouseEvent) -> None:
        x = event.pos().x()
        y = event.pos().y()
        #separated_card = self.card_separator.separate_card(self.frame, x, y)

        #identified_card = self.card_identificator.identify_card(separated_card)