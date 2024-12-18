import engine.creature as cr

class Zombie(cr.creature):
    """A reanimated Limb."""
    classname = "zombie"
    namelist = ["zombie"]
    colors = [None]
    textures = [None]
    def __init__(self, limb, location):
        super().__init__(location=location)
        self.subelements = [limb]

    def _elementGen(self):
        """Zombies should not have limbs generated for them- we will manually set self.subelements."""
        pass
    def _clothe(self):
        """Zombies should not have clothes generated for them when they're created."""
        pass