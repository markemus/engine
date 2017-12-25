import creature as cr 
"""
The Hydra is a dangerous and terrifying creature with a varying number of heads.
Beware its flailing tail and sharp teeth!
"""

#head
eye = cr.limb("eye")
eye.see = 1
eye.isSurface = True
eye.appendageRange = (2,3)

ear = cr.limb("ear")
ear.hear = 1
ear.isSurface = True
ear.appendageRange = (2,3)

teeth = cr.limb("teeth")
teeth.damage = 9
teeth.appendageRange = (1,2)

tongue = cr.limb("tongue")
tongue.appendageRange = (1,2)

snout = cr.limb("snout")
snout.subelements = [tongue, teeth]
snout.smell = 1
snout.isSurface = True
snout.appendageRange = (1,2)

head = cr.limb("head")
head.subelements = [snout, ear, eye]
head.isSurface = True
head.appendageRange = (3,6)

#legs
foot = cr.limb("foot")
foot.amble = 1/3
foot.isSurface = True
foot.appendageRange = (1,2)

leg = cr.limb("leg")
leg.subelements = [foot]
leg.isSurface = True
leg.appendageRange = (4,5)

#tail
tail = cr.limb("tail")
tail.isSurface = True
tail.grasp = 1
tail.f_grasp = 1
tail.t_grasp = 1
tail.damage = 7
tail.appendageRange = (1,2)

#body
body = cr.limb("body")
body.isSurface = True
body.subelements = [head, leg, tail]
body.appendageRange = (1,2)

#hydra
hydra = cr.creature("hydra")
hydra.subelements = [body]
hydra.colors = ["black", "gray", "red"]
hydra.textures = ["scaled"]

if __name__ == "__main__":
    hydra.desc()