import numpy
import cv2

# TODO: Parametrize in a config menu
THRESHOLD1 = 23
THRESOLD2 = 20

AREA_THRESOLD = 5000

class CardSeparator():
    def __init__(self) -> None:
        pass

    def separate_card(self, frame: numpy.ndarray, mouse_x: int, mouse_y: int) -> numpy.ndarray:
        preprocessed_image = self.preprocess_image(frame)
        all_contours = self.get_image_contours(preprocessed_image)
        card_contour = self.get_image_contours(all_contours)
        separated_card = self.crop_image(frame, card_contour)
        return separated_card

    def preprocess_image(image: numpy.ndarray) -> numpy.ndarray:
        """Apply 7x7 gaussian blur on image, then return it on gray scale"""
        blurred_image = cv2.GaussianBlur(image, (7, 7), 1)
        gray_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2GRAY)

    
    def get_image_contours(self, preprocessed_image: numpy.ndarray):
        """Return the contours of all objects with area > AREA_THRESOLD """
        threshold1 = 23
        threshold2 = 20
        
        # Find edges around of image on pos
        canny_image = cv2.Canny(preprocessed_image, threshold1, threshold2)

        kernel = numpy.ones((5, 5))
        dilatated_image = cv2.dilate(canny_image, kernel, iterations=1)

        # Get the coordinates from the edges on canny_image
        all_contours, _ = cv2.findContours(dilatated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        filtered_contours: list = []
        for contour in all_contours:
            area = cv2.contourArea(contour)
            if area > AREA_THRESOLD:
                filtered_contours.append(contour)

        return filtered_contours 

    def get_contour_around_point(self, all_contours, x: int, y: int):
        """Return the contour of the card at x,y"""
        for contour in all_contours:
            if cv2.pointPolygonTest(contour, (x, y), False) >= 0:

                # Obtenha as coordenadas e dimensões do retângulo delimitador do objeto
                return cv2.boundingRect(contour)
    
    def crop_image(self,raw_image: numpy.ndarray, contour):
        """Crops the image around the given contour"""
        x, y, w, h = contour
        cropped_image = raw_image[y:y+h, x:x+w]
        return cropped_image
        
