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
import assets.commonlimbs as cl
import assets.namelists as nm
from assets import suits

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


class Human(cr.creature):
    classname = "man"
    team = "neutral"
    namelist = nm.names["human"]
    baseElem = Torso
    colors = ["black", "white", "brown", "tan"]
    textures = ["skinned"]
    suits = [suits.plainsuit]
