from assets import human
from assets import suits as asu


class PlayerHuman(human.Human):
    """Just an ordinary human."""
    team = "adventurer"
    suits = [asu.plainsuit, asu.backpack, asu.basic_weapons]
