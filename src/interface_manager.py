# 04/08/2022
# Leonardo Di Credico         11202130507
# Anthony Hlebania            11202131843 
# Fernando Hiroaki Suzuki     11202130281 
# Fernando Astolfo Dos Santos 11201920813 
# Instruções de Execução: ./run.sh

import sys
import numpy
import time

from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6 import QtGui

import cv2

from card_identificator import CardIdentificator
from card_separator import CardSeparator

VIEWPORT_MAX: tuple[int, int] = (1280,720)
CARD_MAX : tuple[int, int] = (480,360)

class Vector2():
    def __init__(self, x: int, y:int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"(X: {self.x}, Y: {self.y})"

class InterfaceManager():
    def __init__(self) -> None:
        # Configure camera capture
        self.camera = cv2.VideoCapture(0)

        self.window_setup()

        # Initialize image storage variables
        self.reference_images: list[QtGui.QImage] = []        
        self.current_frame: numpy.ndarray = numpy.zeros((0,0))
        self.current_frame_scale = Vector2(1,1)

        # Timer to update camera image
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start(33)

        self.card_separator = CardSeparator()
        self.card_identificator = CardIdentificator()

    def window_setup(self) -> None:
        self.app = QtWidgets.QApplication([])

        self.main_window = QtWidgets.QMainWindow()
        self.main_window.setWindowTitle("Crakehall Boars - SpellBoar")

        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QGridLayout()
        main_widget.setLayout(main_layout)
        self.main_window.setCentralWidget(main_widget)

        # Label to display camera output
        self.camera_viewport = QtWidgets.QLabel()
        self.camera_viewport.size
        main_layout.addWidget(self.camera_viewport, 0, 0, 3, 4)

        # Label to show cropped image
        self.cropped_image_label = QtWidgets.QLabel()
        main_layout.addWidget(self.cropped_image_label, 0, 5, 1, 1)

        # Label to show canny image
        self.canny_image_label = QtWidgets.QLabel()
        main_layout.addWidget(self.canny_image_label, 1, 5, 1, 1)

        # Layout to show reference images
        self.reference_images_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(self.reference_images_layout, 0, 6, 3, 1)

        self.reference_image_label = QtWidgets.QLabel()
        self.crop_time_label = QtWidgets.QLabel()
        self.match_time_label = QtWidgets.QLabel()
        self.total_time_label = QtWidgets.QLabel()
        self.reference_images_layout.addWidget(self.reference_image_label)
        self.reference_images_layout.addWidget(self.crop_time_label)
        self.reference_images_layout.addWidget(self.match_time_label)
        self.reference_images_layout.addWidget(self.total_time_label)

        # Define function to be triggered on mouse clicked
        self.camera_viewport.mousePressEvent = self.on_mouse_click

        self.main_window.show()

    def add_new_reference_image(self, new_image: numpy.ndarray) -> None:
        self.reference_images.append(new_image)

        pixmap_image = self.numpy_color_image_to_pixmap(new_image, CARD_MAX)

        new_label = QtWidgets.QLabel()
        new_label.setPixmap(pixmap_image)
        self.reference_images_layout.addWidget(new_label)

    def qimage_to_pixmap(self, qimage: QtGui.QImage, max_size: tuple[int, int]) -> QtGui.QPixmap:
        max_height, max_width = max_size
        pixmap = QtGui.QPixmap.fromImage(qimage)
        return pixmap.scaled(max_width, max_height, QtCore.Qt.AspectRatioMode.KeepAspectRatio)

    def numpy_color_image_to_pixmap(self, raw_image: numpy.ndarray, max_size: tuple[int, int]) -> QtGui.QPixmap:
        height, width, pixel_bytes = raw_image.shape
        converted_image = QtGui.QImage(raw_image, width, height, pixel_bytes * width, QtGui.QImage.Format.Format_BGR888)

        return self.qimage_to_pixmap(converted_image, max_size)
    
    def numpy_grayscale_image_to_pixmap(self, raw_image: numpy.ndarray, max_size: tuple[int, int]) -> QtGui.QPixmap:
        height, width = raw_image.shape
        converted_image = QtGui.QImage(raw_image, width, height, 1 * width, QtGui.QImage.Format.Format_Grayscale8)

        return self.qimage_to_pixmap(converted_image, max_size)
    
    def on_mouse_click(self, event: QtGui.QMouseEvent) -> None:
        print("clicked")
        start = time.time()
        
        # Normalize mouse position, because frame size is different from screen size
        x = event.pos().x() * self.current_frame_scale.x
        y = event.pos().y() * self.current_frame_scale.y

        crop_start = time.time()
        sucess, cropped_card, canny_image = self.card_separator.separate_card(self.current_frame, x, y)
        crop_end = time.time()
        canny_image = self.card_separator.canny_image
        
        canny_pixmap = self.numpy_grayscale_image_to_pixmap(canny_image, CARD_MAX)
        self.canny_image_label.setPixmap(canny_pixmap)

        if not sucess:
            return
        
        cropped_card_pixmap = self.numpy_color_image_to_pixmap(cropped_card, CARD_MAX)
        self.cropped_image_label.setPixmap(cropped_card_pixmap)


        match_start = time.time()
        identified_card = self.card_identificator.identify_card(cropped_card)
        match_end = time.time()

        identified_card_pixmap = self.numpy_color_image_to_pixmap(identified_card, CARD_MAX)
        self.reference_image_label.setPixmap(identified_card_pixmap)
        end = time.time()
        #self.add_new_reference_image(identified_card)
        self.crop_time_label.setText(f"Crop time: {(crop_end - crop_start)*1000}ms")
        self.match_time_label.setText(f"Match time: {(match_end - match_start)*1000}ms")
        self.total_time_label.setText(f"Total time: {(end - start)*1000}ms")
    
    def update(self) -> None:
        ret, frame = self.camera.read()
        
        camera_pixmap = self.numpy_color_image_to_pixmap(frame, VIEWPORT_MAX)
        self.current_frame = frame
        scale_x = frame.shape[1] / camera_pixmap.size().width()
        scale_y = frame.shape[0] / camera_pixmap.size().height()
        self.current_frame_scale = Vector2(scale_x, scale_y)

        self.camera_viewport.setPixmap(camera_pixmap)
    
    def run(self) -> None:
        sys.exit(self.app.exec())
