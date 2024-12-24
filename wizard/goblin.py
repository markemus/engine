import engine.suits_and_collections as sc

import assets.dog
import assets.goblin
import assets.suits as asu

import wizard.suits as wsu

class ShallowGoblinChief(assets.goblin.ShallowGoblin):
    classname = "goblin chief"
    suits = [asu.plainsuit, wsu.firesword]

class GoblinPetDog(assets.dog.Dog):
    team = "goblinkin"

goblin_corpse_col = sc.limbs_to_collection(limbs=[assets.goblin.Torso], model=assets.goblin.ShallowGoblin)
