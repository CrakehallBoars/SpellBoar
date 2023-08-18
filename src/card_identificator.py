# 04/08/2022
# Leonardo Di Credico         11202130507
# Anthony Hlebania            11202131843 
# Fernando Hiroaki Suzuki     11202130281 
# Fernando Astolfo Dos Santos 11201920813 
# Instruções de Execução: ./run.sh

import os
import numpy
from PIL import Image as PIL_Image

import cv2
import imagehash

IMAGE_FOLDER = "./card_references"

class CardIdentificator():
    def __init__(self) -> None:
        self.bf = cv2.BFMatcher()
        self.sift = cv2.SIFT_create()

        self.load_image_database()

    def load_image_database(self) -> None:
        """Load all images in IMAGE_FOLDER and storage their hashes and numpy image alongside their filename"""
        self.cv_image_database: dict[str, numpy.ndarray] = {}
        self.hash_database: dict[str, float] = {}
        self.des_database = {}

        for filename in os.listdir(IMAGE_FOLDER):
           path = os.path.join(IMAGE_FOLDER, filename)

           image = PIL_Image.open(path)
           image_hash = self.spellboar_hash(image)
           self.hash_database[filename] = image_hash

           cv_image = cv2.imread(path)
           _, self.des_database[filename] = self.sift.detectAndCompute(cv_image, None)
           self.cv_image_database[filename] = cv_image
    
    def sift_identify(self, unidentified_card: numpy.ndarray) -> numpy.ndarray:
        # Encontra os pontos-chave e descritores da imagem capturada
        kp, des = self.sift.detectAndCompute(unidentified_card, None)

        # Verifica se des1 é válido
        if des is None:
            print("Não foi possível encontrar descritores na imagem recortada.")
            return None

        # Inicializa a variável para armazenar a melhor correspondência
        best_match = None
        best_distance = float('inf')


        # Percorre todas as imagens do banco de dados
        for filename, reference_des in self.des_database.items():

            matches = self.bf.knnMatch(des, reference_des, k=2)

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


    def identify_card(self, unidentified_card: numpy.ndarray) -> numpy.ndarray:
        """Return best match between unidentified card and reference card images"""
        card_hash = self.get_card_hash(unidentified_card)
        match_filename = self.get_best_match(card_hash)
        match_card = self.cv_image_database[match_filename]
        return match_card

    def numpy_to_pil(self, raw_image: numpy.ndarray) -> PIL_Image.Image:
        image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB)
        image = PIL_Image.fromarray(raw_image)
        return image
    
    def spellboar_hash(self, image: PIL_Image) -> PIL_Image:
        return imagehash.dhash(image)
    
    def get_card_hash(self, card: numpy.ndarray) -> float:
        card_image = self.numpy_to_pil(card)
        hash = self.spellboar_hash(card_image)
        return hash
    
    def get_best_match(self, card_hash: float) -> str:
        best_match = ""
        best_distance = float('inf')

        for filename, reference_hash in self.hash_database.items():
            distance = card_hash - reference_hash

            # Update best match
            if distance < best_distance:
                best_distance = distance
                best_match = filename

        #print(f'Best match: {best_match}')
        return best_match

