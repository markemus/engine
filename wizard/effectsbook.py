import engine.effectsbook as eff
import engine.spells as sp


from colorist import BrightColor as BC, Color as C


class SecurityAnnouncement(sp.DelayedEffect):
    rounds = "forever"
    delay = 0

    def _cast(self):
        print(f'{BC.RED}"Conflict detected. Security system is now online. Please desist immediately."{BC.OFF}')
        return True

    def _update(self):
        if self.counter == 5:
            print(f'{BC.RED}"This is your last warning. Cease hostilities or system will be forced to intervene."{BC.OFF}')
        if self.counter == 10:
            print(f'{BC.RED}"Hostilities ongoing despite warnings. Deploying stun grenades."{BC.OFF}')
        if self.counter == 20:
            print(f'{BC.RED}"Warnings ignored. You are being temporarily detained for the protection of yourself and others."{BC.OFF}')
        if self.counter == 30:
            print(f'{BC.RED}"Hostilities ongoing despite interventions. Sealing room for sterilization procedure.{BC.OFF}"')

    def _expire(self):
        print(f'{BC.RED}"No more hostilities detected. Commencing shutdown. Thank you for your cooperation."{BC.OFF}')


class BrightLight(sp.DelayedEffect):
    """Bright light for the security system's spotlight."""
    rounds = "forever"
    on_message = f'{BC.MAGENTA}The spotlight turns on.{BC.OFF}'
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
    on_message = f'{BC.MAGENTA}Grenades fall from holes in the ceiling.{BC.OFF}'
    delay = 10

    def _update(self):
        if self.counter == self.delay:
            enemies = [c for c in self.creature.location.creatures if c.team == "adventurer"]
            for enemy in enemies:
                e = eff.StunForSure(creature=enemy, limb=enemy.subelements[0], controller=self.cont)
                e.cast()


class EntangleFeet(sp.DelayedEffect):
    rounds = "forever"
    on_message = f"{BC.MAGENTA}A long cable snakes out of the floor and begins wrapping itself around your party's feet.{BC.OFF}"
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


class GasAttack(sp.DelayedEffect):
    rounds = "forever"
    on_message = f"\n{BC.MAGENTA}A green cloud blows in through vents in the ceiling.{BC.OFF}"
    delay = 30

    def _update(self):
        for enemy in [c for c in self.creature.location.creatures if c.team == "adventurer" and c.can_breathe]:
            print(f"{BC.MAGENTA}{enemy.name} chokes on the poison gas!{BC.OFF}")
            gas_attack = eff.Poison(creature=enemy, limb=enemy.subelements[0], controller=self.cont)
            gas_attack.cast()


class BrokenSecurityComponent(sp.DelayedEffect):
    rounds = "forever"
    # Subclass and set delay
    delay = 0

    def _update(self):
        if self.counter == self.delay:
            print(f"{BC.MAGENTA}Grinding sounds issue from the {self.limb.name} as it fails to operate.{BC.OFF}")


class BrokenSecurityAnnouncement(sp.DelayedEffect):
    rounds = "forever"
    delay = 0

    def _cast(self):
        print(f'{BC.MAGENTA}Squealing sounds issue from the speaker.{BC.OFF}')
        return True

    def _update(self):
        if self.counter == 5:
            print(f'{BC.MAGENTA}Squealing sounds issue from the speaker.{BC.OFF}')
        if self.counter == 10:
            print(f'{BC.MAGENTA}Squealing sounds issue from the speaker.{BC.OFF}')
        if self.counter == 20:
            print(f'{BC.MAGENTA}Squealing sounds issue from the speaker.{BC.OFF}')
        if self.counter == 30:
            print(f'{BC.MAGENTA}Squealing sounds issue from the speaker.{BC.OFF}')

    def _expire(self):
        print(f'{BC.MAGENTA}Squealing sounds issue from the speaker.{BC.OFF}')


class TurnOffAllSecurityEffects(sp.Effect):
    """Expire all of self.creature's effects."""
    rounds = "forever"

    def update(self):
        combatants = [c for c in self.creature.location.creatures if c.team not in ["adventurer", "neutral"]]
        if not combatants:
            # Expire all security effects, including self
            creature_effects = [e for e in self.cont.game.active_spells if e.creature == self.creature]
            for e in creature_effects:
                e.expire()
