"""See commonlimbs.py for more info on limb design.
class Human(cr.creature):
    classname = "man"
    # teams fight against other teams in the same room. Neutral is not a team and will not fight.
    team = "neutral"
    namelist = nm.names["human"]
    # baseElem is the root element of the limb tree. It will contain subelements in subelement_classes.
    baseElem = Torso
    # colors and textures are used during creature generation to color the limbs
    colors = ["black", "white", "brown", "tan"]
    textures = ["skinned"]
    # the creature will be clothed in their suits during generation. You can give them more than one suit, as long as
    # they don't overlap with each other. It won't crash if they do, but they will fail to overwrite each other where
    # they overlap and create some messages that the player can see.
    suits = [suits.plainsuit, suits.weaponsuit]
"""
import engine.creature as cr
import castle.commonlimbs as cl
import castle.namelists as nm
from castle import suits

class Head(cl.Head):
    # optional beard for humans
    subelement_classes = cl.Head.subelement_classes.copy() + [(cl.Beard, None)]

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, cl.RArm, cl.LArm, cl.Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 40
    size = 3

class PTorso(Torso):
    subelement_classes = [cl.PHead, cl.PRArm, cl.PLArm, cl.PLeg]


class Human(cr.creature):
    classname = "man"
    team = "neutral"
    namelist = nm.names["human"]
    baseElem = Torso
    colors = ["black", "white", "brown", "tan"]
    textures = ["skinned"]
    suits = [suits.plainsuit]

class PlayerHuman(Human):
    """A non-transmogrified Human, but a prisoner."""
    team = "prisoner"
    suits = [suits.prisonersuit]
    # suits = [suits.armorsuit]

class PrisonerHuman(Human):
    team = "prisoner"
    baseElem = PTorso
    suits = [suits.prisonersuit]

class GuardHuman(Human):
    team = "monster"
    suits = [suits.partial_armorsuit, suits.weapons]

class HumanKing(Human):
    classname = "king"
    team = "monster"
    suits = [suits.king_weapon, suits.jewelry, suits.armorsuit]
