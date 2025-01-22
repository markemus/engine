from colorist import BrightColor as BC, Color as C


class Spell:
    name = "spell"
    rounds = None
    mana_cost = None
    expired = False

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
                self.cont.game.active_spells.append(self)
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
        if hasattr(self, "_expire"):
            self._expire()
        self.cont.game.active_spells.remove(self)
        self.expired = True


class Effect:
    # Effects may define a "desc" attribute that will be added to limb.desc()
    desc = None
    rounds = None
    expire_on_removal = False
    cast_on_removal = True
    allow_duplicates = True
    expired = False

    def __init__(self, casting_limb, limb, controller):
        self.casting_limb = casting_limb
        self.limb = limb
        self.cont = controller

    def cast(self):
        """Effects can implement a _cast() method. This will be called when the effect is first applied, similar to
        a spell."""
        if not self.allow_duplicates:
            if sum([isinstance(x, self.__class__) for x in self.limb.active_effects]):
                return False

        if not self.cast_on_removal:
            if self.limb not in self.limb.creature.limb_check("name"):
                return False

        if self._cast():
            self.limb.active_effects.append(self)
            self.cont.game.active_spells.append(self)
            return True

    def _cast(self):
        return True

    def update(self):
        """This works the same way as in Spell()."""
        pass

    def expire(self):
        """Effects may implement an _expire() method. It is optional."""
        if hasattr(self, "_expire"):
            self._expire()
        self.limb.active_effects.remove(self)
        self.cont.game.active_spells.remove(self)
        self.expired = True


class DelayedEffect(Effect):
    """Works the same as Effect, but subclasses should implement _update() instead of update(). They should also set delay.
    rounds should be long enough to include the delay."""
    delay = 0
    counter = 1
    on_message = None

    def update(self):
        if self.counter == self.delay and self.on_message:
            print(self.on_message)
        if self.counter >= self.delay:
            self._update()
        self.counter += 1

    def _update(self):
        """Subclasses should implement _update()."""
        pass
