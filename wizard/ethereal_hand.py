import engine.creature as cr

import assets.commonlimbs as cl

import wizard.suits as su

class EFinger(cl.Finger):
    base_hp = 15

class EThumb(cl.Thumb):
    base_hp = 15

class FlyingHand(cl.RHand):
    subelement_classes = [EFinger, EThumb]
    flight = 1
    see = 1
    base_hp = 30
    strength = 1

class EtherealHand(cr.creature):
    """A flying ethereal hand, gripping a glowing sword."""
    classname = "ethereal hand"
    namelist = ["ethereal hand"]
    baseElem = FlyingHand
    colors = ["glowing"]
    textures = ["ethereal"]
    suits = [su.bronze_lightsword, su.lightsuit]
