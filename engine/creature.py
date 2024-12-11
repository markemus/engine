import random
import time

from colorist import Color as C
from colorist import BrightColor as BC
from engine import ai

# End of Loading Zone

# TODO currently severed limbs cannot be transferred since they have no transfer function. Turn them into items? Inheritance?
#  needs a severed tag. Can inherit from item, why not? Just don't let people move it if it's not severed.
class limb:
    """Body parts for Creatures. Store in a list in Creature object.

    Limbs are procedurally generated from the class template; limbs of the same class may still be
    very different objects."""
    name = "NO_NAME_LIMB"
    wears = "generic"
    base_hp = 10
    _armor = 1
    blocker = False

    def __init__(self, color="d_color", texture="d_texture"):
        self.color = color
        self.texture = texture
        self.subelements = []
        self._elementGen()
        self.inventory = []
        # self.invis_inv = []
        self.hp = self.base_hp

    def _elementGen(self):
        for elemclass in self.subelement_classes:
            # Choose
            if type(elemclass) == tuple:
                elemclass = random.choice(elemclass)

            # Count
            try:
                potentialRange = elemclass.appendageRange
            except AttributeError:
                raise AttributeError("'{0}' : {1} object has no attribute 'appendageRange'".format(elemclass.name, elemclass))
            
            countRange = random.randrange(potentialRange[0], potentialRange[1])

            # Create
            # TODO-DECIDE should this use same color? Good for fingers, maybe not for horns.
            for count in range(countRange):
                elem = elemclass(self.color, self.texture)
                self.subelements.append(elem)

    def desc(self, full=True, offset=0):
        """Basic describe function is always called desc."""
        text = (" "*offset) + f"+ {C.YELLOW}{self.color} {self.texture} {self.name}{C.OFF}"
        if full:
            for item in self.inventory:
                text += "\n" + item.desc(offset = offset+1)
            for elem in self.subelements:
                text += "\n" + elem.desc(offset = offset+1)

        return text

    def limb_check(self, tag):
        """Returns a list of all limbs where tag is present (on the limb or on an inventory item).
        tag=name returns all limbs.
        Used for gathering limbs for a task, eg. tag=grasp to pick up an item."""
        limb_total = []

        # TODO don't allow this for items in eg backpack
        # Allows for items with that tag to be used as if they were a limb themselves.
        if hasattr(self, tag) or sum([hasattr(x, tag) for x in self.inventory]):
            limb_total.append(self)
        
        for subLimb in self.subelements:
            limb_total += subLimb.limb_check(tag)

        return(limb_total)

    def remove_limb(self, limb):
        if limb in self.subelements:
            self.subelements.remove(limb)
        else:
            for subLimb in self.subelements:
                subLimb.remove_limb(limb)

    def transfer(self, who, wherefrom, whereto):
        """A creature moves a removed limb from one inventory to another."""
        if self in wherefrom:
            # Determines that 'who' is able to grasp the item.
            if who.grasp(self):
                whereto.append(self)
                wherefrom.remove(self)
                who.ungrasp(self)
            else:
                print(f"The {who.name} cannot pick up the {self.name}.")
        else:
            print(f"The {self.name} is not there.")

    @property
    def armor(self):
        armor = self._armor

        for item in self.inventory:
            if hasattr(item, "armor"):
                armor += item.armor

        return armor


class weapon(limb):
    """A limb that can deal damage."""
    name = "NO_NAME_WEAPON"
    _damage = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def damage(self):
        """This will return the amount of damage and the item that is causing it.
        This is important for the UI and possibly for other calculations.

        When checking damage, just use limb.damage[0] to reference damage alone."""
        damage = self._damage
        item = self

        for _item in self.inventory:
            if hasattr(_item, "damage"):
                # TODO-DECIDE what about adding damage? eg spikes on tails. Or swords on strong arms.
                if _item.damage > damage:
                    damage = _item.damage
                    item = _item
        
        return damage, item

# TODO-DONE check for eyes before seeing the room. Allow blindfolds!
# TODO-DONE taking items from containers and storing them in inventory
class creature:
    """Creatures are procedurally generated from the class template; creatures of the same class may still be very
    different objects."""
    classname = "NO_NAME_CREATURE"
    team = None
    printcolor = BC.CYAN
    # cantransfer = False      # can carry items
    # subelements = []         # elements of creature
    location = "loader"   # name of Place where creature is- object
    aggressive = True
  
    def __init__(self, location):
        self.name = random.choice(self.namelist)
        self.color = random.choice(self.colors)
        self.texture = random.choice(self.textures)
        self.inventory = []
        self._elementGen()
        self._clothe()

        self.location = location
        self.ai = ai.CombatAI(self)

    def _elementGen(self):
        baseElem = self.baseElem(self.color, self.texture)
        self.subelements = [baseElem]

    def _clothe(self):
        """Equips a creature when it is first created. Multiple suits can be applied in sequence, so weapons
        can be added after armor etc."""
        seed = int(time.time())
        for suit in self.suits:
            if (type(suit) == tuple):
                suit = random.choice(suit)
            # brings back all limbs? I think so. Good trick.
            limbs = self.subelements[0].limb_check("name")

            # Color and texture are either set once for the full suit, or uniquely per "wears" (so socks will always match)
            if suit["color_scheme"] == "distinct":
                colors = {key: random.choice(suit["color"]) for key in suit["wears"]}
            else:
                color = random.choice(suit["color"])
                colors = {key: color for key in suit["wears"]}
            if suit["texture_scheme"] == "distinct":
                textures = {key: random.choice(suit["texture"]) for key in suit["wears"]}
            else:
                texture = random.choice(suit["texture"])
                textures = {key: texture for key in suit["wears"]}

            # If suit is not supposed to be full, drop a random subset of limbs
            if not suit["full"]:
                random.shuffle(limbs)
                limbs = limbs[:random.randrange(0, len(limbs))]

            for limb in limbs:
                if limb.wears in suit["wears"].keys():
                    random.seed(seed)
                    # Choose and construct
                    article = suit["wears"][limb.wears]
                    if type(article) == tuple:
                        article = random.choice(article)
                        # print(article)

                    # Create article
                    article = article(color=colors[limb.wears], texture=textures[limb.wears])
                    limb.inventory.append(article)
        # Reset seed
        random.seed()

    def desc(self, full=True, offset=0):
        """Basic describe function is always called desc."""
        text = (" " * offset) + f"> {self.printcolor}{self.name} ({self.classname}){C.OFF}"
        if full:
            for elem in self.subelements:
                text += "\n" + elem.desc(offset=offset + 1)

        return text

    # Can only move between bordered Places with this function. Should have a failure option.
    def leave(self, direction):
        """Move to a new Place. Accepts a str input."""
        left = False
        currentRoom = self.location
        nextRoom = self.location.borders[direction]

        if nextRoom is not None:
            # TODO-DECIDE Currently each foot has 1/2 amble. Instead require two limbs for walking?
            if len(self.subelements[0].limb_check("amble")) >= 1:
                currentRoom.removeCreature(self)
                self.location = currentRoom.borders[direction]
                nextRoom.addCreature(self)
                left = True
                print(f"You leave {C.RED}{currentRoom.name}{C.OFF} and enter {C.RED}{nextRoom.name}{C.OFF}.")
        else:
            print("There is no way out in that direction.")

        return left

    def viewInv(self):
        """Examine Creature inventory and held Item inventories. Recursive."""
        for carriedItem in self.inventory:
            print(carriedItem.name)
            
            if len(carriedItem.vis_inv) >= 1:
                carriedItem.viewInv()

    def limb_count(self, tag):
        """When you only need to know if a tag is present, it's easy."""
        limbs = self.subelements[0].limb_check(tag)

        limb_total = 0
        for limb in limbs:
            if hasattr(limb, tag):
                limb_total += getattr(limb, tag)
            for x in limb.inventory:
                if hasattr(x, tag):
                    limb_total += getattr(x, tag)

        return limb_total

    def grasp_check(self):
        """Grasps an item with the first available appendage."""
        graspHand = None
        hands = self.subelements[0].limb_check("grasp")
        
        if len(hands) >= 1:
            for hand in hands:
                if hand.grasp >= 1:
                    f_grasp = 0
                    t_grasp = 0

                    for finger in hand.limb_check("f_grasp"):
                        f_grasp += finger.f_grasp
                    for thumb in hand.limb_check("t_grasp"):
                        t_grasp += thumb.t_grasp

                    # TODO check that hand is empty. But can have a glove...
                    if f_grasp >= 1 and t_grasp >= 1:
                        graspHand = hand
                        break

        return graspHand

    def grasp(self, item):
        """Pick up an item with an appendage."""
        grasped = False
        graspHand = self.grasp_check()
                        
        if graspHand is not None:
            graspHand.inventory.append(item)
            print(f"{self.name} picks up the {item.name} with their {graspHand.name}.")
            grasped = True
        else:
            print(f"{self.name} cannot pick up the {item.name}.")

        return grasped

    def ungrasp(self, item):
        ungrasped = False
        hands = self.subelements[0].limb_check("grasp")

        for hand in hands:
            if item in hand.inventory:
                del hand.inventory[hand.inventory.index(item)]
                ungrasped = True

        return ungrasped

    def remove_limb(self, limb):
        if limb in self.subelements:
            self.subelements.remove(limb)
        else:
            for subLimb in self.subelements:
                subLimb.remove_limb(limb)
        # TODO vital should be returned by remove_limb. We should also check if other copies of the vital organ remain (if so, do not die)
        # Losing a vital limb kills the creature
        if hasattr(limb, "vital"):
            if limb.vital:
                self.die()

    def speak(self, words, listener):
        room = self.location.get_creatures()

        if listener in room:
            listener.listen(words, self)
        else:
            print("Who are you talking to?")

    def listen(self, words, speaker):
        print(f"{speaker.printcolor}{speaker.name}{C.OFF} says: \"{words}\".")
        print(f"{self.printcolor}{self.name}{C.OFF} listens carefully.")

    # TODO add looting for severed limbs (inventory management in general needs work)
    def die(self):
        print(f"{self.name} dies.")
        room = self.location
        room.removeCreature(self)
        landings = room.elem_check("canCatch")
        if len(landings) > 0:
            lands_at = random.choice(landings)
            lands_at.add_vis_item(self.subelements[0])
            print(f"{BC.CYAN}{self.name}'s corpse falls onto the {lands_at.name}.{BC.OFF}")
        else:
            print(f"{BC.CYAN}{self.name} falls and disappears out of sight.{BC.OFF}")

    def get_location(self):
        return self.location

    def get_team(self):
        return self.team
