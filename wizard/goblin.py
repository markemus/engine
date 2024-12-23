import assets.dog
import assets.goblin
import assets.suits as asu

import wizard.suits as wsu

class ShallowGoblinChief(assets.goblin.ShallowGoblin):
    classname = "goblin chief"
    suits = [asu.plainsuit, wsu.firesword]

class GoblinPetDog(assets.dog.Dog):
    team = "goblinkin"