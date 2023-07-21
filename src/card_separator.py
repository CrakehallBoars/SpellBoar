import numpy

class CardSeparator():
    def __init__(self):
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
    
    def stackImages(scale,imgArray):
        rows = len(imgArray)
        cols = len(imgArray[0])
        rowsAvailable = isinstance(imgArray[0], list)
        width = imgArray[0][0].shape[1]
        height = imgArray[0][0].shape[0]
        if rowsAvailable:
            for x in range ( 0, rows):
                for y in range(0, cols):
                    if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                    else:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                    if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
            imageBlank = np.zeros((height, width, 3), np.uint8)
            hor = [imageBlank]*rows
            hor_con = [imageBlank]*rows
            for x in range(0, rows):
                hor[x] = np.hstack(imgArray[x])
            ver = np.vstack(hor)
        else:
            for x in range(0, rows):
                if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                    imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
                else:
                    imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
                if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
            hor= np.hstack(imgArray)
            ver = hor
        return ver
    
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
    
    def separate_card(self, frame: numpy.ndarray, mouse_x: int, mouse_y: int) -> numpy.ndarray:
        pass

    
