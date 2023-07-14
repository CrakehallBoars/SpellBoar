from card_identificator import CardIdentificator
from card_separator import CardSeparator

class MainWindow():
    def __init__(self) -> None:
        self.card_separator = CardSeparator()
        self.card_identificator = CardIdentificator()

    def on_card_click(self, pos_x: int, pos_y: int) -> None:
        separated_card = self.card_separator.separate_card(self.frame, pos_x, pos_y)

        identified_card = self.card_identificator.identify_card(separated_card)
    
    def run(self) -> None:
        while(True):
            pass