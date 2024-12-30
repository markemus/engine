import engine.creature as cr

# TODO-DECIDE store original creature somewhere on limb when it gets removed? Then we could name zombies with class
class Zombie(cr.creature):
    """A reanimated Limb."""
    classname = "zombie"
    namelist = ["zombie"]
    colors = [None]
    textures = [None]
    can_rest = False
    can_breathe = False
    can_stun = False

    def __init__(self, limb, location):
        super().__init__(location=location)
        self.subelements = [limb]
        # Heal the limb a bit, since it will have negative hp otherwise
        limb.hp = int(limb.base_hp / 2)
        self.name = f"zombie {limb.name}"

    def _elementGen(self):
        """Zombies should not have limbs generated for them- we will manually set self.subelements."""
        pass
    def _clothe(self):
        """Zombies should not have clothes generated for them when they're created."""
        pass