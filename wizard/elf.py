import assets.elf
import assets.suits as asu
import wizard.suits as wsu

class DarkElf(assets.elf.Elf):
    classname = "dark elf"
    colors = ["black"]
    suits = [wsu.darkelfsuit]

class DarkElfScout(DarkElf):
    suits = [wsu.darkelfsuit, asu.partial_bronze_armorsuit, wsu.poisonsword]
