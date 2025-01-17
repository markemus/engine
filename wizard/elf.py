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
    classname = "dark elf scout"
    suits = [wsu.darkelfsuit, asu.partial_bronze_armorsuit, wsu.bronze_poisonsword]


class DarkElfChampion(DarkElf):
    classname = "dark elf champion"
    suits = [wsu.darkelfsuit, asu.bronze_duelists_armorsuit, wsu.double_iron_poisonsword]
    # masters have a higher to-hit chance
    mastery = 2
    strong_will = True


class DarkElfGuard(DarkElf):
    classname = "dark elf guard"
    suits = [wsu.darkelfsuit, asu.partial_bronze_armorsuit, wsu.iron_poisonsword]


class DarkElfSmith(DarkElf):
    classname = "dark elf smith"
    suits = [wsu.darkelfsuit, wsu.leather_apron, wsu.iron_hammer]
    mastery = 1


dark_elf_corpse_col = sc.limbs_to_collection(limbs=[assets.elf.Torso], model=DarkElfScout)
