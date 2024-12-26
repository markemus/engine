import engine.suits_and_collections as sc

import assets.elf
import assets.suits as asu
import wizard.suits as wsu

class DarkElf(assets.elf.Elf):
    classname = "dark elf"
    team = "dark elf"
    colors = ["black"]
    suits = [wsu.darkelfsuit]

class DarkElfScout(DarkElf):
    suits = [wsu.darkelfsuit, asu.partial_bronze_armorsuit, wsu.bronze_poisonsword]

# TODO give him a sword that summons tiny spiders on hit (that can't be targeted and can't leave room).
class DarkElfChampion(DarkElf):
    suits = [wsu.darkelfsuit, asu.bronze_duelists_armorsuit, wsu.double_iron_poisonsword]

dark_elf_corpse_col = sc.limbs_to_collection(limbs=[assets.elf.Torso], model=DarkElfScout)
