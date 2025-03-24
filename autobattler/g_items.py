from engine import item as it
from engine import utils
from colorist import BrightColor as BC, Color as C


class Paintbrush(it.Item):
    name = "paintbrush"
    colors = ["white", "gray", "brown"]
    textures = ["wood"]
    store_description = "Tool used to paint your golem."
    price = 1

    def use(self, char, controller):
        if not hasattr(char, "golem"):
            print(f"{C.RED}{char.name} has no golem deployed!{C.OFF}")
        golem = char.golem

        colors = utils.listtodict(golem.colors, add_x=True)
        utils.dictprint(colors)
        print(f"{BC.CYAN}You being painting your golem.{BC.OFF}")
        i = input(f"{BC.GREEN}Select a color: {BC.OFF}")

        if i in colors and i != "x":
            color = colors[i]
            textures = utils.listtodict(golem.textures, add_x=True)
            utils.dictprint(textures)
            j = input(f"{BC.GREEN}Select a texture: {BC.OFF}")

            if j in textures and j != "x":
                texture = textures[j]
                limbs = [l for l in golem.limb_check("name") if not hasattr(l, "colors")]
                for limb in limbs:
                    limb.color = color
                    limb.texture = texture
                print(f"{BC.MAGENTA}You paint your golem with {color} {texture}.{BC.OFF}")

            else:
                print(f"{C.RED}You decide not to paint your golem.{C.OFF}")
        else:
            print(f"{C.RED}You decide not to paint your golem.{C.OFF}")


item_list = [Paintbrush]
