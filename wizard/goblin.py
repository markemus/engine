import engine.suits_and_collections as sc

import assets.dog
import assets.goblin
import assets.suits as asu

import wizard.owlbear
import wizard.suits as wsu

class ShallowGoblinChief(assets.goblin.ShallowGoblin):
    classname = "goblin chief"
    strong_will = True
    suits = [asu.plainsuit, (wsu.bronze_firesword, wsu.bronze_lightsword, wsu.bleedflail)]

class GreatGoblin(assets.goblin.DeepGoblin):
    classname = "Great Goblin"
    strong_will = True
    suits = [asu.plainsuit, asu.iron_armorsuit, asu.iron_weapons]

class GoblinPetDog(assets.dog.Dog):
    team = "goblinkin"

class GoblinPetOwlbear(wizard.owlbear.Owlbear):
    team = "goblinkin"

goblin_corpse_col = sc.limbs_to_collection(limbs=[assets.goblin.Torso], model=assets.goblin.ShallowGoblin)
