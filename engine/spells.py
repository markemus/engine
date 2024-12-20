from colorist import BrightColor as BC, Color as C


class Spell:
    name = "spell"
    rounds = None
    def __init__(self, caster, target):
        self.caster = caster
        self.target = target

    def cast(self):
        """Spells should define a _cast() method. It should return True if cast is successful and False otherwise."""
        enough_mana = self.caster.check_siphon_tag("mana", self.mana_cost)
        if enough_mana:
            worked = self._cast()
            if worked:
                siphoned = self.caster.siphon_tag("mana", self.mana_cost)
                # TODO once we're convinced this never fails, remove this exception
                if not siphoned:
                    raise ValueError("Not enough mana to siphon!")
            return worked
        else:
            print(f"{BC.MAGENTA}Not enough mana! The spell fizzles.{BC.OFF}")
            return False


    def update(self):
        """Spells should define an update() method. This is called during every combat round."""
        pass

    def expire(self):
        """Spells should define an expire() method if they need one."""
        pass
