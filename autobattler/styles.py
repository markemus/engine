import autobattler.places as apc

from engine.styles import LevelStyle, GameStyle

from colorist import BrightColor as BC, Color as C
# TODO golem fights (owners are present but neutral)
# TODO shop
# TODO save golems from previous runs to spawn to fight against (level matched)
# TODO crowd effect (more cheering = more gold)
#  more cash for a close fight (so you can rebuild your golem)
#  extra cash for every enemy limb removed
#  more cash for longer fight
# TODO announcer- damage summary every round.
# TODO classes- affect items in shop and AI.
#  torturer- targets small limbs, disables opponent, and extends the fight for more crowd favor.
#  tank- draws aggro, uses heavy armor
#  mage- uses illusions, reduced aggro, no armor
#  rogue- small limbs, light armor
#  tech- devotion causes % chances for magic to malfunction or backfire (in interesting ways?). Same in reverse.
#  petmaster- has pets that deal damage for it.
# TODO different combat ais per class (limb targeting strategies and weapon choice)
# TODO devotion- weapons that deal damage based on how much equipment of certain type golem has.
# TODO synergies.
#  TODO-DONE Suck blood from entangled limbs.
# TODO Heal from fire on self (spread it everywhere).
#  Weapons that attack limb on fire catch fire themselves.
#  Fire shield (takes damage and breaks, but heals from fire).
#  Oil slick that trips enemies that can be lit on fire (anything with oil takes dot).
#  Acid- like fire, but different synergies. Should blind.
#  Ice- freeze limbs, like webbing. But maybe makes them "brittle" so they take more damage. Fire removes ice but not webbing.
#  Slime- puts out fire, digestion damage over time (or heal over time).
#  Buff damage from damage type
#  TODO-DONE Slime- coat a limb and reduce damage from it. Acidic. Puts out fire.
# TODO-DONE Digestive slime- heal yourself for every enemy limb coated in slime. Does a little damage.
# TODO Revive cut off limbs to fight for you (and buzzsaw).
#  Pulp limbs so they can't revive.
#  Buff your little allies.
#  Energy shield that covers allies as well.
#  Orbital- orb that blocks
#  Illusions- allies that don't do damage but draw aggro (somewhat countered by pest ai)
#  Allies that draw aggro and tank an attack or two.
#  AOE attacks (multiple enemies), counters adds.
#  Hook (pull enemies out of the sky)
#  Ranged weapons countered by armor. (use ammo?)
#  Melee weapons countered by blockers.
#  Reactive armor- light weapon on fire, spray it with acid
#  TODO-DONE Armor breach- reduce limb armor
# TODO-DONE Weaken enemy limb to reduce damage. Allow this to stack so you can build a debuffing build that grows over time
# TODO Double tap- next attack happens twice.
#  Effects that only occur after N rounds.
#  Dispel- remove N of creature's effects. Counters effect builds.
#  A weapon/effect that buffs, heals, damages based on how many of same damage type weapons you have
#  Limb that draws attacks to it
#  Consumable limbs/equipment that leave permanent buffs behind
#  Temporary buffs with longer term negative effects (so good early fight but becomes worse in long fights)
#  TODO-DONE Static- electricity zap on attack. Messes with mechanical and doesn't affect magical.
# TODO Magic level (lowered by technology). Devotion to damage type (amount of damage dealt, or number of limbs currently affected).
#  Blood rituals- drain blood, give some effect
#  Shrink- make limbs smaller, would synergize with effects that give small limbs increased evasion
#  TODO-DONE Eyes that give better vision (counters shadow), mastery, smoke goggles- light effect on limbs that are on fire.
#  TODO laser beams



class Arena:
    level_text = f"""{BC.BLUE}You've scrimped and saved your whole life for this opportunity. Build a golem and fight your opponents' golems to earn money to build your golem even stronger. Work your way up through the ranks and become a master of the arena.{BC.OFF}"""
    room_classes = [apc.ChangingRooms]
    start_room = apc.GolemStore
    end_room = apc.Arena
    creature_classes = []


LevelStyle.register(Arena)

class Golem:
    # levels will spawn in this order
    levelorder = [Arena]
    # Doors will be added linking these levels together- level 0 to level 1, level 1 to level 2, etc.
    links = []
    start_splash = f"""
    ------------------------
    |      {C.RED}Golemancy{C.OFF}      |
    
    |                      |
    |  {C.BLUE}an {BC.CYAN}EverRogue{BC.OFF} {C.BLUE}game{C.OFF}   |
    |     by Markemus      |
    ------------------------
        """
    # This will display on game over
    death_splash = f"""
    ------------------------
    |       {C.RED}YOU DIED{C.OFF}       |
    ------------------------
        """


GameStyle.register(Golem)
