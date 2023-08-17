import os
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from collections import Counter

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # Inicializa a captura de vídeo para acessar a webcam
        self.capture = cv2.VideoCapture(0)
        
        # Cria um QLabel para exibir a imagem
        self.image_label = QtWidgets.QLabel()
        self.setCentralWidget(self.image_label)
        
        # Configura um QTimer para atualizar o feed da webcam
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_image)
        self.timer.start(30)  # Atualiza a imagem a cada 30 ms

    def update_image(self):
        # Captura um frame da webcam
        ret, self.captured_frame = self.capture.read()
        
        # Converte o frame para o formato RGB
        frame = cv2.cvtColor(self.captured_frame, cv2.COLOR_BGR2RGB)
        
        # Converte o frame para QImage e exibe no QLabel
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        self.image_label.setPixmap(QtGui.QPixmap.fromImage(qImg))
    def mousePressEvent(self, event):
        num_captures = 5  # Número de imagens que serão capturadas em rápida sucessão
        matches = []  # Lista para armazenar a melhor correspondência identificada para cada imagem capturada
        
        for _ in range(num_captures):
            ret, captured_frame = self.capture.read()
            best_match = self.process_selected_region(captured_frame)
            if best_match is not None:
                matches.append(best_match)
        
        # Verifica se a lista de matches está vazia antes de prosseguir
        if matches:
            most_common, num_most_common = Counter(matches).most_common(1)[0]
            print(f'Melhor correspondência com base na votação: {most_common}')
        else:
            print('Nenhuma correspondência encontrada.')

    def process_selected_region(self, captured_frame):
        # Inicializa o detector SIFT
        sift = cv2.SIFT_create()

        # Encontra os pontos-chave e descritores da imagem capturada
        kp1, des1 = sift.detectAndCompute(captured_frame, None)

        # Verifica se des1 é válido
        if des1 is None:
            print("Não foi possível encontrar descritores na imagem recortada.")
            return None

        # Define o caminho para o banco de imagens
        script_dir = os.path.dirname(os.path.realpath(__file__))
        image_database_path = os.path.join(script_dir, 'BancoDeDados')

        # Inicializa a variável para armazenar a melhor correspondência
        best_match = None
        best_distance = float('inf')

        # Percorre todas as imagens do banco de dados
        for filename in os.listdir(image_database_path):
            # Lê a imagem do banco de dados
            image_path = os.path.join(image_database_path, filename)
            image = cv2.imread(image_path, 0)

            # Encontra os pontos-chave e descritores da imagem do banco de dados
            kp2, des2 = sift.detectAndCompute(image, None)

            # Verifica se des2 é válido
            if des2 is None:
                print(f"Não foi possível encontrar descritores na imagem {filename}.")
                continue

            # Cria um objeto BFMatcher
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)

            # Aplica o teste da razão para filtrar os bons matches
            good_matches = []
            for m, n in matches:
                if m.distance < 0.9 * n.distance:
                    good_matches.append(m)

            # Calcula a distância média entre os matches
            if good_matches:
                distance = sum(match.distance for match in good_matches) / len(good_matches)

                # Verifica se essa imagem é a melhor correspondência até agora
                if distance < best_distance:
                    best_distance = distance
                    best_match = filename

        return best_match

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
