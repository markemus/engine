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