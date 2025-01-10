from assets import human
from assets import suits as asu


class PlayerHuman(human.Human):
    """Just an ordinary human."""
    team = "adventurer"
    suits = [asu.plainsuit, asu.backpack, asu.basic_weapons]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for limb in self.limb_check("name"):
    #         limb.base_hp = int(limb.base_hp * 1.5)
    #         limb.hp = int(limb.hp * 1.5)
