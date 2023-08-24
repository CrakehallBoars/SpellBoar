# 24/08/2022
# Leonardo Di Credico         11202130507
# Anthony Hlebania            11202131843 
# Fernando Hiroaki Suzuki     11202130281 
# Fernando Astolfo Dos Santos 11201920813 
# Instruções de Execução: ./setup.sh

import PIL
import sys
import os
from colorama import Fore

cur_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{cur_path}/..")
from src.card_identificator import CardIdentificator

IMAGE_FOLDER = "tests/images"

class IdentificatorTests():
    def __init__(self):
        self.ci = CardIdentificator()
        unsleeved_rate = self.assert_folder(f"{IMAGE_FOLDER}/unsleeved")
        sleeved_rate   = self.assert_folder(f"{IMAGE_FOLDER}/sleeved")
        general_rate   = (unsleeved_rate + sleeved_rate) / 2

        print(f"Sleeved   sucess rate: {self.decimal_to_percent(sleeved_rate)}")
        print(f"Unsleeved sucess rate: {self.decimal_to_percent(unsleeved_rate)}")
        print(f"General   sucess rate: {self.decimal_to_percent(general_rate)}")
    
    def decimal_to_percent(self, decimal: float) -> str:
        return f"{round(decimal * 100, 2)}%"

    def _remove_extension(self, filename: str) -> str:
        return filename.split('.')[0]

    def _assert_card(self,folder: str, card_name: str) -> tuple[bool, str]:
        card = PIL.Image.open(f"{folder}/{card_name}.jpg")
        hash = self.ci.spellboar_hash(card)
        best_match = self._remove_extension(self.ci.get_best_match(hash))
        return best_match == card_name, best_match

    def assert_folder(self, folder: str) -> float:
        print(f"Testing all files on {folder}")

        total = len(os.listdir(folder))
        sucess_count = 0.0

        for filename in os.listdir(folder):
            filename = self._remove_extension(filename)

            sucess, best_match = self._assert_card(folder, filename)

            status = Fore.RED + "FAILURE:"
            if(sucess):
                status = Fore.GREEN + "SUCESS: "
                sucess_count += 1

            message = f"{status} Identified {filename} as {best_match}" + Fore.WHITE
            print(message)
            #self._assert_card(f"{IMAGE_FOLDER}/unsleeved", filename)
        
        sucess_rate = sucess_count / total
        return sucess_rate


if __name__ == '__main__':
    id_tests = IdentificatorTests()