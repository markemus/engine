"""The minotaur wanders the labyrinth, seeking intruders and crushing them."""
import engine.creature as cr

import assets.commonlimbs as cl
import assets.namelists as nm
import assets.suits as asu

import monster.suits as msu


class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Horn, cl.Ear, cl.Eye, cl.Nose, cl.Jaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = "head"
    base_hp = 25
    size = 3
    strength = 1.5

# Torso
class Torso(cr.Limb):
    name = "body"
    subelement_classes = [Head, cl.LargeRArm, cl.LargeLArm, cl.LargeLeg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 60
    size = 3

# Minotaur
class Minotaur(cr.creature):
    classname = "minotaur"
    team = "monster"
    namelist = nm.names["greek"]
    baseElem = Torso
    colors = ["red", "brown", "green", "black", "gray"]
    textures = ["haired"]
    suits = [msu.club, asu.prisonersuit]
