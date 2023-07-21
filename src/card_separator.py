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
        pass

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

        all_contours, _ = cv2.findContours(dilatated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        filtered_contours: list = []
        return filtered_contours 

    def get_contour_around_point(self, contours, x: int, y: int):
        pass
        
    cap = cv2.VideoCapture(0)
    
    cv2.namedWindow("Parameters")
    cv2.resizeWindow("Parameters",640,240)
    cv2.createTrackbar("Threshold1","Parameters",23,255,empty)
    cv2.createTrackbar("Threshold2","Parameters",20,255,empty)
    cv2.createTrackbar("Area","Parameters",5000,30000,empty)
    
    object_captured = False
    object_coords = []
    
    def on_mouse_click(event, x, y, flags, param):
        global object_captured, object_coords
        if event == cv2.EVENT_LBUTTONDOWN:
            object_captured = True
            object_coords = (x, y)
    
    def show_cropped_image(img, x, y, w, h):
        object_crop = img[y:y+h, x:x+w]
    
        # Verifique se o objeto recortado é válido antes de exibi-lo
        if object_crop.size != 0:
            cv2.imshow("Objeto Recortado", object_crop)
        else:
            print("Nenhum objeto válido capturado.")
    
    
    def getContours(img,imgContour):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            areaMin = cv2.getTrackbarPos("Area", "Parameters")
            if area > areaMin:
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x , y , w, h = cv2.boundingRect(approx)
                cv2.rectangle(imgContour, (x , y ), (x + w , y + h ), (0, 255, 0), 5)
                
                
    cv2.namedWindow("Result")
    cv2.setMouseCallback("Result", on_mouse_click)
    
    while True:
        success, img = cap.read()
        imgContour = img.copy()
        imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
        imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
        threshold1 = 23
        threshold2 = 20
        imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
        kernel = np.ones((5, 5))
        imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
        #Mostra na janela, os contornos que estão sendo feitos em volta do objeto
        #getContours(imgDil, imgContour)
        contours, _ = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        cv2.imshow("Result", imgContour)
        
        cv2.setMouseCallback("Result", on_mouse_click)
    
        if object_captured:
            object_captured = False
            x, y = object_coords
    
            # Encontre o contorno correspondente ao objeto clicado
            for contour in contours:
                if cv2.pointPolygonTest(contour, (x, y), False) >= 0:
                    # Obtenha as coordenadas e dimensões do retângulo delimitador do objeto
                    x, y, w, h = cv2.boundingRect(contour)
                    show_cropped_image(img, x, y, w, h)
                    break
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    

    
