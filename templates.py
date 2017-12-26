"""
DEPRECATED. Templates are now defined within standard creature and element classes. Creatures are then generated
from them in their class constructors.

This module converts normal objects into template objects for test purposes.
"""
import creature

class creatureTemplate(creature.creature):
    #templates are basic creatures used for creature generation.
    #They contain a definition of the possible variations for the creature class.
    #Default values will simply recreate the template creature. 

    def __init__(self, name, baseCreature, appendageRange = (1,2), colors=None, textures=None):
        super(creatureTemplate, self).__init__(name)
        self.subelements = copy.deepcopy(baseCreature.subelements)
        core = self.subelements[0]
        self.colors = colors
        self.textures = textures
        self.set_default_variables(core, appendageRange)
        
        #core must always be unique.
        core.appendageRange = (1,2)

    def set_default_variables(self, element, appendageRange):
        
        if (type(element) == tuple):
            for option in element:
                self.set_default_variables(option, appendageRange)
        else:
            element.appendageRange = appendageRange

            for subelement in element.subelements:
                self.set_default_variables(subelement, appendageRange)