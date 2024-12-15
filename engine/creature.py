import random
import time

from colorist import Color as C
from colorist import BrightColor as BC
from engine import ai

# End of Loading Zone
class Limb:
    """Body parts for Creatures. Store in a list in Creature object.

    Limbs are procedurally generated from the class template; limbs of the same class may still be
    very different objects."""
    name = "NO_NAME_LIMB"
    wears = None
    base_hp = 10
    _armor = 1
    blocker = False
    printcolor = C.CYAN
    grasped = None

    def __init__(self, color="d_color", texture="d_texture"):
        self.color = color
        self.texture = texture
        self.subelements = []
        self._elementGen()
        self.equipment = []
        self.covers = []
        # self.vis_inv = []
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
            # TODO-DECIDE should this use same color? Good for fingers, maybe not for horns. Maybe add share_color tag?
            for count in range(countRange):
                elem = elemclass(self.color, self.texture)
                self.subelements.append(elem)

    def desc(self, full=True, offset=0):
        """Basic describe function is always called desc."""
        text = (" "*offset) + f"+ {C.YELLOW}{self.color} {self.texture} {self.name}{C.OFF}"
        if full:
            for item in self.equipment:
                text += "\n" + item.desc(offset = offset+1)
            for elem in self.subelements:
                text += "\n" + elem.desc(offset = offset+1)

        return text

    def limb_check(self, tag):
        """Returns a list of all limbs where tag is present (on the limb or on an inventory item).
        tag=name returns all limbs.
        Used for gathering limbs for a task, eg. tag=grasp to pick up an item."""
        limb_total = []

        # TODO-DONE don't allow this for items in eg backpack
        # Allows for items with that tag to be used as if they were a limb themselves.
        if hasattr(self, tag) or sum([hasattr(x, tag) for x in self.equipment]):
            limb_total.append(self)
        
        for subLimb in self.subelements:
            limb_total += subLimb.limb_check(tag)

        return(limb_total)

    def find_invs(self):
        """Find all inventories lower in the body hierarchy."""
        invs = []

        # Equipped items
        for item in self.equipment:
            if hasattr(item, "vis_inv"):
                invs.append(item)

        # Held item
        if hasattr(self, "grasped"):
            if hasattr(self.grasped, "vis_inv"):
                invs.append(self.grasped)

        for subLimb in self.subelements:
            invs += subLimb.find_invs()

        return invs

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
                print(f"{BC.CYAN}{who.name} puts away the {self.name}.{BC.OFF}")
            else:
                print(f"{C.RED}The {who.name} cannot pick up the {self.name}.{C.OFF}")
        else:
            print(f"{C.RED}The {self.name} is not there.{C.OFF}")

    def equip(self, article):
        """Put an Item (article) onto the Limb.
        article.requires can specify a required tag as ("tag", amount).
        article.level specifies the level it will be equipped at. Each Limb can only equip one Item at each level."""
        equipped = False
        if article.canwear[self.wears]:
            if not article.requires or (hasattr(self, article.requires[0]) and (getattr(self, article.requires[0]) >= article.requires[1])):
                # Check level if empty
                already_equipped = [x for x in self.equipment if x.level == article.level]
                if not already_equipped:
                    # Insert equipment at proper level
                    i = 0
                    levels = [x.level for x in self.equipment]
                    for i, level in enumerate(levels):
                        if level > article.level:
                            break
                    self.equipment.insert(i, article)
                    # Equipment should cover limb (and lower limbs if applicable).
                    # Items that cover should always have a 'descend' tag.
                    if hasattr(article, "descends"):
                        potentially_cover = self.return_from_depth(article.descends)
                        for subelement in potentially_cover:
                            if article.covers[subelement.wears]:
                                # Insert equipment at proper level
                                i = 0
                                levels = [x.level for x in subelement.covers]
                                for i, level in enumerate(levels):
                                    if level > article.level:
                                        break
                                subelement.covers.insert(i, article)
                    equipped = True
                else:
                    print(f"{C.RED}{self.name} already has a {already_equipped[0].name} equipped!{C.OFF}")
            else:
                print(f"{C.RED}{self.name} lacks the {article.requires[0]} ability!{C.OFF}")
        else:
            print(f"{C.RED}{self.name} cannot wear a {article.name}!{C.OFF}")

        return equipped

    def return_from_depth(self, depth):
        """Returns a list of all subelements down to 'depth' in the subelement tree."""
        depth_elements = [self]
        if depth:
            for subelement in self.subelements:
                depth_elements += subelement.return_from_depth(depth-1)
        return depth_elements

    @property
    def armor(self):
        armor = self._armor

        for item in self.equipment:
            if hasattr(item, "armor"):
                armor += item.armor

        return armor


class Weapon(Limb):
    """A limb that can deal damage."""
    name = "NO_NAME_WEAPON"
    _damage = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def damage(self):
        """This will return the amount of damage and the item that is causing it.
        This is important for the UI and possibly for other calculations.

        When checking damage, use limb.damage[0] to reference damage alone."""
        damage = self._damage
        item = self

        # EG gauntlets, spiked gloves, fake fangs. self.grasped is eg swords
        for _item in self.equipment + [self.grasped]:
            if hasattr(_item, "damage"):
                if _item.damage > damage:
                    damage = _item.damage
                    item = _item

        # eg swords
        # if self.grasped self.grasped.damage > damage:
        #     damage = self.grasped.damage
        #     item = self.grasped

        return damage, item

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
        self._elementGen()
        self._clothe()

        self.location = location
        self.ai = ai.CombatAI(self)

    def _elementGen(self):
        baseElem = self.baseElem(self.color, self.texture)
        self.subelements = [baseElem]

    def _clothe(self):
        """Equips a creature when it is first created. Multiple suits can be applied in sequence, so weapons
        can be added after armor etc. Note that color schemes will be shared across weapons and armor, so it
        might make sense to split them into separate suits."""
        # Seed is to coordinate item selection across limbs of the same type, we don't get eg shoe+slipper
        seed = int(time.time())
        for suit in self.suits:
            # print(suit)
            if (type(suit) == tuple):
                suit = random.choice(suit)
            # Returns all limbs
            limbs = self.subelements[0].limb_check("name")

            # Color and texture are either set once for the full suit, or uniquely per "wears" (so socks will always match)
            if suit["color_scheme"] == "distinct":
                colors = {key: random.choice(suit["color"]) for key in {**suit["wears"], **suit["grasps"]}}
            else:
                color = random.choice(suit["color"])
                colors = {key: color for key in {**suit["wears"], **suit["grasps"]}}
            if suit["texture_scheme"] == "distinct":
                textures = {key: random.choice(suit["texture"]) for key in {**suit["wears"], **suit["grasps"]}}
            else:
                texture = random.choice(suit["texture"])
                textures = {key: texture for key in {**suit["wears"], **suit["grasps"]}}

            # If suit is not supposed to be full, drop a random subset of limbs
            if not suit["full"]:
                random.shuffle(limbs)
                limbs = limbs[:random.randrange(0, len(limbs))]

            for limb in limbs:
                if "wears" in suit.keys() and limb.wears in suit["wears"].keys():
                    random.seed(seed)
                    # Choose and construct articles
                    article = suit["wears"][limb.wears]
                    if type(article) == tuple:
                        articles = [random.choice(article)]
                    elif type(article) == list:
                        articles = article.copy()
                    else:
                        articles = [article]

                    for article in articles:
                        # Create article and equip
                        article = article(color=colors[limb.wears], texture=textures[limb.wears])
                        limb.equip(article)

                if "grasps" in suit.keys() and limb.wears in suit["grasps"].keys():
                    # We don't need to coordinate weapon selections
                    random.seed()
                    # Choose and construct articles
                    weapon = suit["grasps"][limb.wears]
                    if type(weapon) == tuple:
                        weapons = [random.choice(weapon)]
                    elif type(weapon) == list:
                        weapons = weapon.copy()
                    else:
                        weapons = [weapon]

                    for weapon in weapons:
                        if not limb.grasped:
                            # Create weapon and grasp
                            weapon = weapon(color=colors[limb.wears], texture=textures[limb.wears])
                            limb.grasped = weapon

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
            if len(self.subelements[0].limb_check("amble")) >= 1:
                currentRoom.removeCreature(self)
                self.location = currentRoom.borders[direction]
                nextRoom.addCreature(self)
                left = True
                print(f"You leave {C.RED}{currentRoom.name}{C.OFF} and enter {C.RED}{nextRoom.name}{C.OFF}.")
        else:
            print("There is no way out in that direction.")

        return left

    def limb_count(self, tag):
        limbs = self.subelements[0].limb_check(tag)

        limb_total = 0
        for limb in limbs:
            if hasattr(limb, tag):
                limb_total += getattr(limb, tag)
            for x in limb.equipment:
                if hasattr(x, tag):
                    limb_total += getattr(x, tag)

        return limb_total

    # TODO this is the way tag checks should work in general, and we should have a general function to check them.
    #  use properties to set tag = 0 if subtags aren't there? We need hasattr to be supported... it's a bit messy.
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

                    # check that hand is empty.
                    if f_grasp >= 1 and t_grasp >= 1:
                        if not hand.grasped:
                            graspHand = hand
                            break

        return graspHand

    def grasp(self, item):
        """Pick up an item with an appendage."""
        grasped = False
        graspHand = self.grasp_check()
                        
        if graspHand is not None and not graspHand.grasped:
            graspHand.grasped = item
            print(f"{BC.CYAN}{self.name} picks up the {item.name} with their {graspHand.name}.{BC.OFF}")
            grasped = True
        else:
            print(f"{C.RED}{self.name} cannot pick up the {item.name}.{C.OFF}")

        return grasped

    # TODO-DECIDE refactor ungrasp and transfer? None of this feels necessary. How would we even know to call ungrasp without knowing what hand is holding the item?
    #  on the other hand it does play well with transfer()?
    def ungrasp(self, item):
        """Ungrasp an item from an appendage. The calling function will need to determine where to put it next."""
        ungrasped = False
        hands = self.subelements[0].limb_check("grasp")

        for hand in hands:
            # if item in hand.equipment:
            #     hand.equipment.remove(item)
            if hand.grasped == item:
                hand.grasped = None
                ungrasped = True
                break

        return ungrasped

    def remove_limb(self, limb):
        if limb in self.subelements:
            self.subelements.remove(limb)
        else:
            for subLimb in self.subelements:
                subLimb.remove_limb(limb)
        # TODO-DONE vital should be returned by remove_limb. We should also check if other copies of the vital organ remain (if so, do not die)
        # Losing a vital limb kills the creature
        if hasattr(limb, "vital") and limb.vital:
            vitals = self.subelements[0].limb_check("vital")
            # We check if other vital limbs share this exact class (eg two heads, two hearts).
            if not sum([vital.__class__ == limb.__class__ for vital in vitals]):
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
            lands_at.vis_inv.append(self.subelements[0])
            print(f"{BC.CYAN}{self.name}'s corpse falls onto the {lands_at.name}.{BC.OFF}")
        else:
            print(f"{BC.CYAN}{self.name} falls and disappears out of sight.{BC.OFF}")

    def get_location(self):
        return self.location

    def get_team(self):
        return self.team
