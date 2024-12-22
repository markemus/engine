from colorist import BrightColor as BC, Color as C


class Spell:
    name = "spell"
    rounds = None
    def __init__(self, caster, target, controller):
        self.caster = caster
        self.target = target
        self.cont = controller

    def cast(self):
        """Spells should define a _cast() method. It should return True if cast is successful and False otherwise."""
        enough_mana = self.caster.check_siphon_tag("mana", self.mana_cost)
        if enough_mana:
            worked = self._cast()
            if worked:
                siphoned = self.caster.siphon_tag("mana", self.mana_cost)
                # TODO-DECIDE once we're convinced this never fails, remove this exception?
                if not siphoned:
                    raise ValueError("Not enough mana to siphon!")
            return worked
        else:
            print(f"{BC.MAGENTA}Not enough mana! The spell fizzles.{BC.OFF}")
            return False


    def update(self):
        """Spells may define an update() method. This is called during every combat round."""
        pass

    def expire(self):
        """Spells may define an expire() method if they need one."""
        pass


class Effect:
    # Effects may define a "desc" attribute that will be added to limb.desc()
    desc = None
    rounds = None
    def __init__(self, creature, limb):
        self.creature = creature
        self.limb = limb

    def cast(self):
        """Effects should implement a cast() method. This will be called when the effect is first applied, similar to
        a spell"""
        pass

    def update(self):
        """This works the same way as in Spell()."""
        pass

    def expire(self):
        """Effects may implement an _expire() method. It is optional."""
        if hasattr(self, "_expire"):
            self._expire()
        self.limb.active_effects.remove(self)
