"""
Accessory items like rings and amulets.
"""
import random
from constants import COLOR_WHITE
from .base import Equipment
from traits import Trait


class Accessory(Equipment):
    """Accessory equipment (rings, amulets, etc.)."""
    
    def __init__(self, x, y, name, char, attack_bonus=0, defense_bonus=0, 
                 description="", fov_bonus=0, health_aspect_bonus=0.0, attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 xp_cost=5):
        super().__init__(
            x=x, y=y,
            name=name,
            char=char,
            color=COLOR_WHITE,
            description=description,
            attack_bonus=attack_bonus,
            defense_bonus=defense_bonus,
            equipment_slot="accessory",
            fov_bonus=fov_bonus,
            health_aspect_bonus=health_aspect_bonus,
            attack_multiplier_bonus=attack_multiplier_bonus,
            defense_multiplier_bonus=defense_multiplier_bonus,
            xp_multiplier_bonus=xp_multiplier_bonus,
            evade_bonus=evade_bonus,
            crit_bonus=crit_bonus,
            crit_multiplier_bonus=crit_multiplier_bonus,
            xp_cost=xp_cost
        )

# Base Classes
class Ring(Accessory):
    """Base class for rings."""
    
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0, fov_bonus=0, health_aspect_bonus=0, 
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 xp_cost=5, description="A magical ring"):
        super().__init__(x, y, name, '=', attack_bonus, defense_bonus, description, fov_bonus, health_aspect_bonus,
                         attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus,
                         evade_bonus, crit_bonus, crit_multiplier_bonus, xp_cost)

class Card(Accessory):
    """Base class for cards."""
    
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0, fov_bonus=0, health_aspect_bonus=0,
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 xp_cost=5, description="An enchanted card"):
        super().__init__(x, y, name, '#', attack_bonus, defense_bonus, description, fov_bonus, health_aspect_bonus,
                         attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus,
                         evade_bonus, crit_bonus, crit_multiplier_bonus, xp_cost)

class Artifact(Accessory):
    """Base class for artifacts"""
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0, fov_bonus=0, health_aspect_bonus=0,
              attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
              evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
              xp_cost=5, description="An enchanted card"):
      super().__init__(x, y, name, 'a', attack_bonus, defense_bonus, description, fov_bonus, health_aspect_bonus,
                      attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus,
                      evade_bonus, crit_bonus, crit_multiplier_bonus, xp_cost)


class Necklace(Accessory):
    """Base class for necklaces."""
    
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0, fov_bonus=0, health_aspect_bonus=0,
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 xp_cost=5, description="A magical necklace"):
        super().__init__(x, y, name, 'v', attack_bonus, defense_bonus, description, fov_bonus, health_aspect_bonus,
                         attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus,
                         evade_bonus, crit_bonus, crit_multiplier_bonus, xp_cost)

class Hat(Accessory):
    """Base class for hats."""
    
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0, fov_bonus=0, health_aspect_bonus=0,
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 xp_cost=5, description="A cool hat"):
        super().__init__(x, y, name, '^', attack_bonus, defense_bonus, description, fov_bonus, health_aspect_bonus,
                         attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus,
                         evade_bonus, crit_bonus, crit_multiplier_bonus, xp_cost)


class PowerRing(Ring):
    """Ring that boosts attack."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ring of Power", attack_bonus=3, defense_bonus=0)


class ProtectionRing(Ring):
    """Ring that provides strong defense."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ring of Protection", defense_bonus=2)

class Rosary(Necklace):
    """Necklace that increases health aspect."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Rosary", defense_bonus=1, health_aspect_bonus=0.1, description="A healer's necklace")
        self.weaknesses = [Trait.HOLY]
        self.resistances = [Trait.DARK]

class HeadLamp(Hat):
    """Hat that increases FOV"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "HeadLamp", attack_bonus=0, defense_bonus=1, fov_bonus=5, description="lamp on your head")

class BaronsCrown(Hat):
    """Hat with attack multiplier."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Baron's Crown", attack_multiplier_bonus=1.25, description="Crown of a Jester King")

class JewelersCap(Hat):
    """Hat with XP multiplier."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Jeweler's Cap", xp_multiplier_bonus=1.1, description="A greedy man's gift")

# Later Game Accessories

class GreaterPowerRing(Ring):
    """Ring that greatly boosts attack."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Greater Ring of Power", attack_bonus=6, defense_bonus=0)


class GreaterProtectionRing(Ring):
    """Ring that greatly boosts attack."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Greater Ring of Protection", attack_bonus=0, defense_bonus=4)


class AceOfSpades(Card):
    """Double Attack, Zero Defense"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ace of Spades", attack_multiplier_bonus=2.0, defense_multiplier_bonus=0.1, description="Are you a gambling man? doubles attack, decimates defense")

class AceOfDiamonds(Card):
    
    def __init__(self, x, y):
        super().__init__(x,y, "Ace of Hearts", description="2x XP if 20% HP or less")

    def get_xp_multiplier_bonus(self, player):
        if(player.hp <= (player.max_hp / 5)):
            return 2
        else:
            return 0
        
class AceOfClubs(Card):
        def __init__(self, x, y):
          super().__init__(x, y, "Ace of Clubs", description="+5 Def if 20% HP or less")

        def get_defense_bonus(self, player):
          if(player.hp <= (player.max_hp / 5)):
              return 5
          else:
              return 0
          
class AceOfHearts(Card):
        def __init__(self, x, y):
          super().__init__(x, y, "Ace of Hearts", description="2x attack if at full health")

        def get_attack_multiplier_bonus(self, player):
            if(player.hp == player.max_hp): 
                return 2
            else: 
                return 1
            
class Joker(Card):
        def __init__(self, x, y):
          super().__init__(x, y, "Joker", description="Double or nothing on Everything")

        def get_attack_multiplier_bonus(self, player):
            rand = random.random()
            if rand <= 0.5:
              return 2
            else:
              return 0.5
            
        def get_defense_multiplier_bonus(self, player):
            rand = random.random()
            if rand <= 0.5:
              return 2
            else:
              return 0.5
            
        def get_xp_multiplier_bonus(self, player):
            rand = random.random()
            if rand <= 0.5:
              return 2
            else:
              return 0.5


# Example accessories using new evade/crit bonuses
class ShadowRing(Ring):
    """Ring that enhances evasion."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Shadow Ring", evade_bonus=0.10, description="A ring that bends light around you")


class RingOfPrecision(Ring):
    """Ring that enhances critical strikes."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ring of Precision", crit_bonus=0.12, description="A ring that guides your strikes")


class BrutalityAmulet(Necklace):
    """Necklace that enhances critical damage."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Amulet of Brutality", crit_multiplier_bonus=0.5, description="An amulet that amplifies your fury")


class AssassinsMask(Hat):
    """Mask combining stealth and lethality."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Assassin's Mask", evade_bonus=0.08, crit_bonus=0.08, 
                        description="A mask that shrouds you in shadow and sharpens your focus")
        
class PsychicsTurban(Hat):
    """+1 ATK for every consumable used."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Psychic's Turban", 
                        description="+1 ATK for each consumable used")
    
    def get_attack_bonus(self, player):
        return super().get_attack_bonus(player) + player.consumable_count
    

class GravePact(Hat):
    """+6 ATK on Dark and Ice."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Grave Pact", 
                        description="+6 ATK for cold and dark attack")
    
    def get_attack_bonus(self, player):
        pt = player.get_total_attack_traits()
        base_bonus = super().get_attack_bonus(player)
        if Trait.DARK in pt or Trait.ICE in pt:
            return base_bonus + 6
        else:
            return base_bonus
        
class TurtleShell(Hat):
    """+6 DEF -6 ATK."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Turtle Shell", 
                        description="+6 DEF, -6 ATK")
    
    def get_attack_bonus(self, player):
        return super().get_attack_bonus(player) - 6
    
    def get_defense_bonus(self, player):
        return super().get_defense_bonus(player)
        
        