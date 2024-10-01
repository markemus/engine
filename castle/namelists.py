# TODO-DONE why aren't we using namelists?

names = {"goblin": ["Reshgar", "Shamrath", "Imptor", "Zagroth", "Marosh", "Eilim", "Hanand", "Sharog"],
         "orc": ["Murgur", "Amroth", "Kailin", "Meex", "Ralosh", "Loth"],
         "human": ["Emen", "Rami", "Sagden", "Merind", "Hom", "Shriv"],
         "hobbit": ["Mumpto", "Hamlin", "Gooby", "Grint", "Smit", "Rag"],
         "elf": ["Erilir", "Rea", "Dolinir", "Astroth", "Reanor", "Ashaab"],
         "dwarf": ["Gargrin", "Erith", "Margor", "Kharoth", "Shirv", "Emmon"],
         "troll": ["Arggh", "Grargh", "Erff", "Smurr", "Urd"],
}



class Dark:
    verbs = ["crying", "killing", "fleeing", "poisoning", "sobbing"]
    adverbs = ["angry", "fearful", "fearsome", "ferocious", "agonizing"]

class Light:
    verbs = ["singing", "laughing", "smiling", "rejoicing"]
    adverbs = ["happily", "joyously", "miraculously"]

class Pattern:
    sentence = [Dark.adverbs, Dark.verbs]

class SentenceBuilder:
    def __init__(self):
        pass