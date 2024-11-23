from enum import Enum


class CardType(Enum):
    ACTIVE = (1, "odyssey", "Brick")
    PASSIVE = (2, "viva", "Brick")

    def __init__(self, num, deck_name, note_type):
        self._value_ = num
        self.deck_name = deck_name
        self.note_type = note_type