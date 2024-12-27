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


class DarkElfChampion(DarkElf):
    classname = "dark elf champion"
    suits = [wsu.darkelfsuit, asu.bronze_duelists_armorsuit, wsu.double_iron_poisonsword]
    # masters have a higher to-hit chance
    mastery = 2


class DarkElfGuard(DarkElf):
    classname = "dark elf guard"
    suits = [wsu.darkelfsuit, asu.bronze_armorsuit, wsu.iron_poisonsword]

dark_elf_corpse_col = sc.limbs_to_collection(limbs=[assets.elf.Torso], model=DarkElfScout)
