import engine.effectsbook as eff
import engine.spells as sp


from colorist import BrightColor as BC, Color as C


class SecurityAnnouncement(sp.Effect):
    rounds = 1
    def _cast(self):
        print(f'{BC.RED}"Conflict detected. Security system is now online. Please desist immediately."{BC.OFF}')
        return True


class BrightLight(sp.DelayedEffect):
    """Bright light for the security system's spotlight."""
    rounds = "forever"
    on_message = f'{BC.RED}"This is your last warning. Cease hostilities immediately."\n{BC.MAGENTA}The spotlight turns on.{BC.OFF}'
    delay = 5
    expire_on_removal = True

    def _cast(self):
        self.effects = []
        return True

    def _update(self):
        enemies = [c for c in self.creature.location.creatures if c.team == "adventurer"]
        for enemy in enemies:
            enemy_illuminated = False
            for limb in enemy.limb_check("isSurface"):
                light = eff.Light(creature=enemy, limb=limb, controller=self.cont)
                if light.cast():
                    enemy_illuminated = True
                    self.effects.append(light)

            if enemy_illuminated:
                print(f"{BC.MAGENTA}{enemy.name} is illuminated in the harsh glare!{BC.OFF}")

    def _expire(self):
        for effect in self.effects:
            if not effect.expired:
                effect.expire()
        print(f"{BC.MAGENTA}The harsh light illuminating the room goes out.{BC.OFF}")


class StunGrenades(sp.DelayedEffect):
    rounds = 11
    on_message = f'{BC.RED}"Hostilities still detected. Deploying stun grenades."{BC.OFF}'
    delay = 10

    def _update(self):
        if self.counter == self.delay:
            enemies = [c for c in self.creature.location.creatures if c.team == "adventurer"]
            for enemy in enemies:
                e = eff.StunForSure(creature=enemy, limb=enemy.subelements[0], controller=self.cont)
                e.cast()


class EntangleFeet(sp.DelayedEffect):
    rounds = "forever"
    on_message = f'{BC.RED}"Warnings ignored. You are being temporarily detained for the protection of yourself and others."{BC.OFF}'
    # Subclass and set entangling_limb
    entangling_limb = None
    delay = 20

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class Entangled(eff.Entangled):
            rounds = "forever"
            entangling_limb = self.entangling_limb

        self.Entangled = Entangled

    def _update(self):
        enemies = [c for c in self.creature.location.creatures if c.team == "adventurer"]
        for enemy in enemies:
            feet = enemy.limb_check("amble")
            can_fly = enemy.limb_count("flight")
            if not can_fly:
                for foot in feet:
                    e = self.Entangled(creature=enemy, limb=foot, controller=self.cont)
                    e.cast()


class TurnOffAllSecurityEffects(sp.Effect):
    """Expire all of self.creature's effects."""
    rounds = "forever"
    def update(self):
        combatants = [c for c in self.creature.location.creatures if c.team not in ["adventurer", "neutral"]]
        if not combatants:
            print(f'{BC.RED}"No more hostilities detected. Commencing shutdown. Thank you for your cooperation."{BC.OFF}')
            # Expire all security effects, including self
            creature_effects = [e for e in self.cont.game.active_spells if e.creature == self.creature]
            for e in creature_effects:
                e.expire()
