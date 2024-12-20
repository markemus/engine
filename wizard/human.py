from assets import human
from assets import suits as asu


class PlayerHuman(human.Human):
    """Just an ordinary human."""
    team = "adventurer"
    suits = [asu.plainsuit, asu.backpack]

class SpecimenHuman(human.Human):
    team = "specimen"
    aggressive = False
