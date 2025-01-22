import engine.item as it
import engine.effectsbook as eff
import autobattler.effectsbook as aeff


class SmokeMonacle(it.Item):
    name = "smoke monacle"
    canwear = it.Item.canwear.copy()
    covers = it.Item.covers.copy()
    canwear["eye"] = True
    level = 4
    descends = 0
    price = 10
    extra_vision = [eff.FireDOT, aeff.FireDOT]
    colors = ["black", "brown", "mirrored"]
    textures = ["glassy"]


equipment = [SmokeMonacle]
