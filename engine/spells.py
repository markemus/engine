class Spell:
    name = "spell"
    rounds = None
    def __init__(self, caster, target):
        self.caster = caster
        self.target = target
        # Spell is created when it is cast
        self._cast()
        # TODO-DECIDE how should we track cast spells? game object?

    def _cast(self):
        """Spells should define a cast effect."""
        pass

    def expire(self):
        """Spells should define an expire effect if they need one."""
        pass
