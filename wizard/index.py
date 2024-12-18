from assets import human, cat, giant_spider
from assets import places
from assets import suits

from engine.styles import LevelStyle, GameStyle
from engine import creature as cr
from engine import game
from engine import interface
from engine import utils

from colorist import BrightColor as BC, Color as C


class PlayerHuman(human.Human):
    """Just an ordinary human."""
    team = "prisoner"
    suits = [suits.plainsuit]

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

class Home:
    level_text = f"""{BC.BLUE}You are in your home, preparing to set off on your adventure.{BC.OFF}"""
    room_classes = [places.Bathroom, places.Bedroom, places.Parlor, places.Kitchen]
    start_room = places.Den
    end_room = places.DiningRoom
    creature_classes = []

LevelStyle.register(Home)

class Wizard:
    # levels will spawn in this order
    levelorder = [Home]
    # Doors will be added linking these levels together- level 0 to level 1, level 1 to level 2, etc.
    links = []
    start_splash = f"""Wizard Game"""
    death_splash = f"""YOU DIED"""

GameStyle.register(Wizard)


# This should go into engine
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

class Light(Spell):
    name = "Light"
    description = "A luminous glow that surrounds a creature, making it easier to hit."
    rounds = 10
    targets = "enemy"
    # TODO-DECIDE mana costs for spells?
    def _cast(self):
        self.original_colors = {}
        limbs = self.target.subelements[0].limb_check("isSurface")
        for limb in limbs:
            self.original_colors[limb] = limb.color
            limb.color = f"luminous {limb.color}"
            limb.size += 1
        print(f"{BC.MAGENTA}A luminous glow surrounds {C.RED}{self.target.name}{BC.MAGENTA}.{BC.OFF}")

    def expire(self):
        limbs = self.target.subelements[0].limb_check("isSurface")
        for limb in limbs:
            if limb in self.original_colors.keys():
                limb.color = self.original_colors[limb]
                limb.size -= 1
        print(f"{BC.MAGENTA}The glow surrounding {C.RED}{self.target.name}{BC.MAGENTA} fades away.{BC.OFF}")

class SummonSpider(Spell):
    name = "Summon Spider"
    description = "Summon an enemy spider."
    rounds = 1
    targets = "caster"

    def _cast(self):
        """This is useful if you want to test combat magic on an opponent."""
        spider = giant_spider.GiantSpider(location=self.target.location)
        self.target.location.creatures.append(spider)
        print(f"{BC.MAGENTA}A {C.RED}giant spider{BC.MAGENTA} pops into existence!{BC.OFF}")

class ReanimateLimb(Spell):
    name = "Reanimate Limb"
    description = "Reanimate a zombie."
    rounds = 1
    targets = "caster"

    def _cast(self):
        """Bring a limb in the room back to life."""
        if self.caster.humanity <= 1:
            invs = self.caster.location.find_invs()
            # Drop equipment
            invs = utils.listtodict(invs, add_x=True)
            utils.dictprint(invs)
            i = input(f"\n{BC.GREEN}Which inventory would you like to resurrect from?{BC.OFF} ")

            if i in invs.keys() and i != "x":
                limbs = utils.listtodict([item for item in invs[i].vis_inv if isinstance(item, cr.Limb)], add_x=True)
                utils.dictprint(limbs)
                j = input(f"\n{BC.GREEN}Select a limb to resurrect:{BC.OFF} ")

                if j in limbs.keys() and j != "x":
                    limb = limbs[j]
                    zombie = Zombie(limb=limb, location=self.caster.location)
                    zombie.team = self.caster.team
                    self.caster.location.addCreature(zombie)
                    self.caster.companions.append(zombie)
                    print(f"{C.RED}{zombie.name}{BC.MAGENTA} rises from the dead with a moan!{BC.OFF}")



# Main
# Generate a game using the Wizard template.
t_game = game.Game("The Path to Wizardry", Wizard)
thisLevel = t_game.level_list[0]

player = PlayerHuman(location=thisLevel.start)
player.name = input(f"{BC.CYAN}Enter your name: {BC.OFF}")
familiar = cat.Cat(location=thisLevel.start)
familiar.name = input(f"{BC.CYAN}Enter the name of your familiar: {BC.OFF}")
player.companions.append(familiar)
thisLevel.start.creatures.append(player)
thisLevel.start.creatures.append(familiar)
t_game.set_char(player)

# Character setup
player.spellbook.append(Light)
player.spellbook.append(SummonSpider)
player.spellbook.append(ReanimateLimb)
# Player humanity affects which spells they can cast
player.humanity = 1

thisLevel.start.find_invs()[0].vis_inv.append(human.Head(color="gray", texture="rotting"))

i = interface.Interface(t_game)
# Game loop- if you use CTRL-C to cheat, just run this to get back into the game when you're ready.
while True:
    i.command()

# TODO-DONE spell tracking
# TODO-DONE spell casting from interface
# TODO-DONE player party
# TODO-DECIDE exchange equipment with party?
