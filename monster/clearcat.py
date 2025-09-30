"""A clear serene creature with visible internal organs."""
import engine.creature as cr

import assets.commonlimbs as cl
import assets.namelists as nm

class Fang(cr.Weapon):
    name = "fang"
    subelement_classes = []
    _damage = 15
    appendageRange = (2, 3)
    wears = "fang"
    base_hp = 7
    size = 1
    colors = ["yellow"]
    textures = ["enameled"]

class Snout(cr.Limb):
    name = "snout"
    subelement_classes = [cl.Nose, Fang, cl.Tongue]
    isSurface = True
    appendageRange = (1, 2)
    wears = "snout"
    base_hp = 8
    size = 2
    eats = 1
    strength = 1

class Brain(cr.Limb):
    name = "brain"
    subelement_classes = []
    isSurface = False
    appendageRange = (1, 2)
    vital = "brain"
    base_hp = 5
    size = 1
    colors = ["gray"]
    textures = ["wrinkly"]

class Skull(cr.Limb):
    name = "skull"
    subelement_classes = [Brain]
    isSurface = False
    appendageRange = (1, 2)
    size = 2
    base_hp = 10
    colors = ["white"]
    textures = ["ivory"]

class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Ear, Skull, cl.Eye, Snout]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_head"
    vital = "head"
    base_hp = 15
    size = 2

class Claw(cr.Limb):
    name = "claw"
    subelement_classes = []
    isSurface = True
    appendageRange = (5, 6)
    wears = "claw"
    base_hp = 3
    size = 1

class PawBones(cr.Limb):
    name = "bone"
    subelement_classes = []
    isSurface = False
    appendageRange = (5, 6)
    base_hp = 5
    size = 1
    colors = ["white"]
    textures = ["ivory"]

class Paw(cr.Limb):
    name = "paw"
    subelement_classes = [PawBones, Claw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "paw"
    base_hp = 5
    size = 1
    amble = 1/3

class LegBones(cr.Limb):
    name = "bone"
    subelement_classes = []
    isSurface = False
    appendageRange = (2, 3)
    colors = ["white"]
    textures = ["ivory"]
    base_hp = 5
    size = 1

class Leg(cr.Limb):
    name = "leg"
    subelement_classes = [LegBones, Paw]
    isSurface = True
    appendageRange = (4, 5)
    wears = "animal_leg"
    base_hp = 10
    size = 2
    strength = 1

class TailBones(cr.Limb):
    name = "bone"
    subelement_classes = []
    isSurface = False
    appendageRange = (5, 6)
    colors = ["white"]
    textures = ["ivory"]
    base_hp = 5
    size = 1

class Tail(cr.Limb):
    name = "tail"
    subelement_classes = [TailBones]
    isSurface = True
    appendageRange = (1, 2)
    base_hp = 5
    size = 2

class Spine(cr.Limb):
    name = "spine"
    subelement_classes = []
    isSurface = False
    appendageRange = (1, 2)
    size = 2
    base_hp = 15
    colors = ["white"]
    textures = ["ivory"]

class Lung(cr.Limb):
    name = "lung"
    subelement_classes = []
    isSurface = False
    appendageRange = (2, 3)
    colors = ["gray"]
    textures = ["smooth"]
    base_hp = 3
    size = 1

class Heart(cr.Limb):
    name = "heart"
    subelement_classes = []
    isSurface = False
    appendageRange = (1, 2)
    colors = ["red"]
    textures = ["muscly"]
    base_hp = 3
    size = 1
    vital = "heart"

class Liver(cr.Limb):
    name = "liver"
    subelement_classes = []
    isSurface = False
    appendageRange = (1, 2)
    base_hp = 3
    size = 1
    colors = ["brown"]
    textures = ["meaty"]

class Stomach(cr.Limb):
    name = "stomach"
    subelement_classes = []
    isSurface = False
    appendageRange = (2, 3)
    base_hp = 3
    size = 1
    colors = ["red"]
    textures = ["smooth"]

class Kidney(cr.Limb):
    name = "kidney"
    subelement_classes = []
    isSurface = False
    appendageRange = (2, 3)
    base_hp = 3
    size = 1
    colors = ["brown"]
    textures = ["smooth"]

class LargeIntestine(cr.Limb):
    name = "large intestine"
    subelement_classes = []
    isSurface = False
    appendageRange = (2, 3)
    base_hp = 3
    size = 1
    colors = ["white"]
    textures = ["wrinkly"]

class SmallIntestine(cr.Limb):
    name = "small intestine"
    subelement_classes = []
    isSurface = False
    appendageRange = (2, 3)
    base_hp = 3
    size = 1
    colors = ["white"]
    textures = ["wrinkly"]

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, Spine, Lung, Heart, Liver, Stomach, Kidney, LargeIntestine, SmallIntestine, Leg, Tail]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_body"
    base_hp = 15
    size = 2

class ClearCat(cr.creature):
    classname = "clearcat"
    aggressive = False
    team = "escapee"
    namelist = nm.names["cat"]
    baseElem = Torso
    colors = ["clear"]
    textures = ["glassy"]
    suits = []
