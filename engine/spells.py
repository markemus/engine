class Spell:
    name = "spell"
    rounds = None
    def __init__(self, caster, target):
        self.caster = caster
        self.target = target
        # Spell is created when it is cast

    def cast(self):
        """Spells should define a cast effect. It should return True if cast is successful and False otherwise."""
        pass

    def update(self):
        """Spells should define an update effect. This is called during every combat round."""
        pass

    def expire(self):
        """Spells should define an expire effect if they need one."""
        pass
