# 24/08/2022
# Leonardo Di Credico         11202130507
# Anthony Hlebania            11202131843 
# Fernando Hiroaki Suzuki     11202130281 
# Fernando Astolfo Dos Santos 11201920813 
# Instruções de Execução: ./setup.sh

import sys
import os
from colorama import Fore
import cv2

cur_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{cur_path}/../src")
from card_identificator import CardIdentificator
from card_separator import CardSeparator
from interface_manager import Vector2

IMAGE_FOLDER = "tests/images"

class FullTester():
    def __init__(self) -> None:
        self.ci = CardIdentificator()
        self.cs = CardSeparator()

        self.card_matches: dict[str, dict[Vector2, str]] = {
            "A.png": {
                Vector2(447.0 , 345.0): "PainfulLesson",
                Vector2(775.5 , 354.0): "Withercrown",
                Vector2(1033.5, 352.5): "Jaya_sGreeting",
                Vector2(1335.0, 387.0): "SpellgorgerWeird", 
                Vector2(489.0 , 778.5): "ChainwhipCyclops", 
                Vector2(772.5 , 795.0): "BrokenWings", 
                Vector2(1071.0, 801.0): "WormholeSerpent", 
                Vector2(1491.0, 777.0): "RelentlessAdvance."
            },
            "B.png": {
                Vector2(459.0 , 291.0): "PainfulLesson" , 
                Vector2(747.0 , 309.0): "Withercrown", 
                Vector2(976.5 , 327.0): "Jaya_sGreeting", 
                Vector2(1300.5, 358.5): "SpellgorgerWeird", 
                Vector2(1534.5, 384.0): "Demolish", 
                Vector2(454.5 , 678.0): "ChainwhipCyclops", 
                Vector2(763.5 , 690.0): "JasperaSentinel", 
                Vector2(1093.5, 720.0): "PhantomMonster", 
                Vector2(1371.0, 735.0): "FillwithFright", 
            },
            "C.png":
            {
                Vector2(433.5 , 367.5): "Withercrown",
                Vector2(756.0 , 361.5): "PainfulLesson",
                Vector2(1050.0, 366.0): "Jaya_sGreeting", 
                Vector2(1354.5, 375.0): "FillwithFright", 
                Vector2(1617.0, 382.5): "JasperaSentinel", 
                Vector2(408.0 , 688.5): "PhantomMonster", 
                Vector2(645.0 , 688.5): "ChainwhipCyclops", 
                Vector2(921.0 , 688.5): "Demolish", 
                Vector2(1515.0, 718.5): "SpellgorgerWeird"
            },
            "D.png":
            {
                Vector2(475.5, 373.5): "Withercrown",
                Vector2(748.5, 382.5): "PainfulLesson", 
                Vector2(1057.5, 379.5): "Jaya_sGreeting", 
                Vector2(1339.5, 372.0): "FillwithFright", 
                Vector2(1606.5, 393.0): "JasperaSentinel", 
                Vector2(405.0, 706.5): "PhantomMonster", 
                Vector2(639.0, 711.0): "ChainwhipCyclops",
                Vector2(949.5, 738.0): "Demolish", 
                Vector2(1246.5, 729.0): "RelentlessAdvance", 
                Vector2(1585.5, 729.0): "WormholeSerpent"
            },
            "E.png":
            {
                Vector2(249.0, 343.5): "ChainwhipCyclops", 
                Vector2(435.0, 328.5): "Withercrown", 
                Vector2(675.0, 325.5): "FillwithFright", 
                Vector2(1014.0, 288.0): "Jaya_sGreeting", 
                Vector2(1306.5, 309.0): "PainfulLesson", 
                Vector2(1644.0, 357.0): "JasperaSentinel", 
                Vector2(1819.5, 364.5): "BrokenWings", 
                Vector2(351.0, 720.0): "PhantomMonster", 
                Vector2(613.5, 733.5): "RelentlessAdvance", 
                Vector2(934.5, 730.5): "Demolish", 
                Vector2(1546.5, 724.5): "WormholeSerpent"
            }
        }

        average_sum = 0
        results: list[str] = []
        for image, card_positions in self.card_matches.items():
            sucess = self._assert_image_cards(image, card_positions)
            sucess_rate = self.decimal_to_percent(sucess)
            average_sum += sucess
            results.append(f"{image}  sucess rate: {sucess_rate}")
        for result in results:
            print(result)
        print(f"Average sucess rate: {self.decimal_to_percent(average_sum/len(results))}")

    def decimal_to_percent(self, decimal: float) -> str:
        return f"{round(decimal * 100, 2)}%"
    
    def _assert_image_cards(self, filename: str, card_positions: dict[Vector2, str]) -> float:
        print(f"Testing cards on image {filename}")

        image = cv2.imread(f"{IMAGE_FOLDER}/full_scene/{filename}")

        sucess_count = 0.0

        total = len(card_positions.items())

        for pos, card_name in card_positions.items():
            _, cropped_image, _ = self.cs.separate_card(image, pos.x, pos.y)
            card_hash = self.ci.get_card_hash(cropped_image)
            match_filename = self.ci.sift_identify(cropped_image).replace('.jpg', '')

            sucess = match_filename == card_name

            status = Fore.RED + "FAILURE:"
            if(sucess):
                status = Fore.GREEN + "SUCESS: "
                sucess_count += 1

            message = f"{status} Identified {card_name} as {match_filename}" + Fore.WHITE
            print(message)
        
        sucess_rate = sucess_count / total
        return sucess_rate

if __name__ == '__main__':
    id_tests = FullTester()
