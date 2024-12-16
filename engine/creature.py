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
    subelement_classes = None
    wears = None
    base_hp = 10
    _armor = 1
    blocker = False
    printcolor = C.CYAN
    grasped = None
    # Size should be an int between 1 and 3. This affects to-hit chance.
    size = 2

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
        """Creates subelements from the subelement classes specified in the class definition."""
        for elemclass in self.subelement_classes:
            # Choose
            if type(elemclass) == tuple:
                elemclass = random.choice(elemclass)

            # Allows for optional limbs with (elemclass1, elemclass2, None)
            if elemclass is not None:
                # Count
                try:
                    potentialRange = elemclass.appendageRange
                except AttributeError:
                    raise AttributeError("'{0}' : {1} object has no attribute 'appendageRange'".format(elemclass.name, elemclass))

                countRange = random.randrange(potentialRange[0], potentialRange[1])

                # Create
                # TODO-DONE should this use same color? Good for fingers, maybe not for horns. Maybe add share_color tag?
                #  best way would be to use self.color if limb does not have limb.colors, otherwise use those.
                # If element has its own color definitions, use those (eg hair). Most elements should just inherit parent color.
                if hasattr(elemclass, "colors"):
                    color = random.choice(elemclass.colors)
                    texture = random.choice(elemclass.textures)
                else:
                    color = self.color
                    texture = self.texture

                for count in range(countRange):
                    elem = elemclass(color, texture)
                    self.subelements.append(elem)

    def desc(self, full=True, offset=0, stats=True):
        """Basic describe function is always called desc."""
        text = (" "*offset) + f"+ {C.YELLOW}{self.color} {self.texture} {self.name}{C.OFF}"
        if stats:
            text += f" {C.RED}({self.hp}/{self.base_hp}) {C.BLUE}({self.armor}){C.OFF}"
        if full:
            if hasattr(self, "grasped") and self.grasped:
                text += "\n" + self.grasped.desc(offset=offset+1)
            for item in self.covers:
                text += "\n" + item.desc(offset=offset+1, )
            for elem in self.subelements:
                text += "\n" + elem.desc(offset=offset+1, stats=stats)

        return text

    def limb_check(self, tag):
        """Returns a list of all limbs where tag is present (on the limb or on an inventory item).
        tag=name returns all limbs.
        Used for gathering limbs for a task, eg. tag=grasp to pick up an item."""
        limb_total = []

        # Allows for items with that tag to be used as if they were a limb themselves.
        if hasattr(self, tag) or sum([hasattr(x, tag) for x in self.equipment]):
            limb_total.append(self)
        
        for subLimb in self.subelements:
            limb_total += subLimb.limb_check(tag)

        return(limb_total)

    def limb_count(self, tag):
        """Counts total of tag value in subelements."""
        limbs = self.limb_check(tag)

        limb_total = 0
        for limb in limbs:
            if hasattr(limb, tag):
                limb_total += getattr(limb, tag)
            for x in limb.equipment:
                if hasattr(x, tag):
                    limb_total += getattr(x, tag)

        return limb_total

    def find_invs(self):
        """Find all inventories lower in the body hierarchy."""
        invs = []

        # if self.equipment:
        #     invs.append(self)

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
        # Losing a grasping limb should make the creature drop the associated weapon
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
                print(f"{C.RED}{who.name} cannot pick up the {self.name}.{C.OFF}")
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

    def get_neighbors(self, limb):
        neighbors = []
        if limb in self.subelements:
            neighbors = [self, *limb.subelements]
        else:
            for x in self.subelements:
                neighbors.extend(x.get_neighbors(limb))

        return neighbors

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
    dead = False
  
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
            elif suit["color_scheme"] == "same":
                c = random.choice(suit["color"])
                colors = {key: c for key in {**suit["wears"], **suit["grasps"]}}
            if suit["texture_scheme"] == "distinct":
                textures = {key: random.choice(suit["texture"]) for key in {**suit["wears"], **suit["grasps"]}}
            elif suit["texture_scheme"] == "same":
                t = random.choice(suit["texture"])
                textures = {key: t for key in {**suit["wears"], **suit["grasps"]}}

            # If suit is not supposed to be full, drop a random subset of limbs
            if not suit["full"]:
                random.shuffle(limbs)
                limbs = limbs[:random.randrange(0, len(limbs))]

            for limb in limbs:
                if "wears" in suit.keys() and limb.wears in suit["wears"].keys():
                    # Choose and construct articles
                    article = suit["wears"][limb.wears]
                    if type(article) == tuple:
                        # We want article choices to be coordinated, so we use the same seed for each tuple selection (eg pairs of shoes).
                        random.seed(seed)
                        articles = [random.choice(article)]
                        random.seed()
                    elif type(article) == list:
                        articles = article.copy()
                    else:
                        articles = [article]

                    for article in articles:
                        # Create article and equip
                        # For unique color scheme, each item gets its own color and texture
                        if suit["color_scheme"] == "unique":
                            color = random.choice(suit["color"])
                        else:
                            color = colors[limb.wears]
                        if suit["texture_scheme"] == "unique":
                            texture = random.choice(suit["texture"])
                        else:
                            texture = textures[limb.wears]
                        article = article(color=color, texture=texture)
                        limb.equip(article)

                if "grasps" in suit.keys() and limb.wears in suit["grasps"].keys():
                    # We don't need to coordinate weapon selections
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
                            if suit["color_scheme"] == "unique":
                                color = random.choice(suit["color"])
                            else:
                                color = colors[limb.wears]
                            if suit["texture_scheme"] == "unique":
                                texture = random.choice(suit["texture"])
                            else:
                                texture = textures[limb.wears]
                            weapon = weapon(color=color, texture=texture)
                            limb.grasped = weapon

        # Reset seed
        random.seed()

    def desc(self, full=True, offset=0, stats=True):
        """Basic describe function is always called desc."""
        text = (" " * offset) + f"> {self.printcolor}{self.name} ({self.classname}){C.OFF}"
        if full:
            for elem in self.subelements:
                text += "\n" + elem.desc(offset=offset + 1, stats=stats)

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
        """Counts total of tag value in subelements."""
        limbs = self.subelements[0].limb_check(tag)

        limb_total = 0
        for limb in limbs:
            if hasattr(limb, tag):
                limb_total += getattr(limb, tag)
            for x in limb.equipment:
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
            print(f"{C.RED}{self.name} does not have a free hand to pick up the {item.name}.{C.OFF}")

        return grasped

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

    def get_neighbors(self, limb):
        return self.subelements[0].get_neighbors(limb)

    def update_status(self):
        """Checks all limbs for necessary tags and updates status."""
        limbs = self.subelements[0].limb_check("name")
        for limb in limbs:
            if hasattr(limb, "grasp"):
                if not (limb.limb_count("f_grasp") >= 1) or not (limb.limb_count("t_grasp") >= 1):
                    if limb.grasped:
                        self.location.drop_item(limb.grasped)
                        limb.grasped = None


    def remove_limb(self, limb):
        if limb in self.subelements:
            # Limb is the core limb. Just die and don't try checking statuses since we're removing the whole limb tree.
            self.subelements.remove(limb)
            self.die()
            return
        else:
            for subLimb in self.subelements:
                subLimb.remove_limb(limb)

        # Losing a vital limb kills the creature
        limb_vitals = limb.limb_check("vital")
        # We'll see if others of this class are still attached
        limb_vitals = set([x.__class__ for x in limb_vitals])
        if len(limb_vitals):
            other_vitals = set([x.__class__ for x in self.subelements[0].limb_check("vital")])
            # We confirm that all vitals that were removed still exist in our subelements. Otherwise, die.
            if len(limb_vitals.intersection(other_vitals)) < len(limb_vitals):
                self.die()

        self.update_status()

    def die(self):
        print(f"{self.name} dies.")
        room = self.location

        # Drop all held items
        for grasper in self.subelements[0].limb_check("grasp"):
            if grasper.grasped:
                x = grasper.grasped
                grasper.grasped = None
                room.drop_item(x)

        # Then die
        room.removeCreature(self)
        self.dead = True
        # and fall down
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
