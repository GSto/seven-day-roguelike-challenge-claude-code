"""
Accessory items like rings and amulets.
"""
import random
from constants import COLOR_WHITE
from .equipment import Equipment
from traits import Trait


class Accessory(Equipment):
    """Accessory equipment (rings, amulets, etc.)."""
    
    def __init__(self, x, y, name, char, attack_bonus=0, defense_bonus=0, 
                 description="", fov_bonus=0, health_aspect_bonus=0.0, attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 attack_traits=None, weaknesses=None, resistances=None,
                 xp_cost=5, is_cleanup=False):
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
            attack_traits=attack_traits,
            weaknesses=weaknesses,
            resistances=resistances,
            xp_cost=xp_cost,
            is_cleanup=is_cleanup
        )

# Base Classes
class Ring(Accessory):
    """Base class for rings."""
    
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0, fov_bonus=0, health_aspect_bonus=0, 
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 attack_traits=None, weaknesses=None, resistances=None,
                 xp_cost=5, description="A magical ring", is_cleanup=False):
        super().__init__(x, y, name, '=', attack_bonus, defense_bonus, description, fov_bonus, health_aspect_bonus,
                         attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus,
                         evade_bonus, crit_bonus, crit_multiplier_bonus, attack_traits, weaknesses, resistances, xp_cost, is_cleanup)

class Card(Accessory):
    """Base class for cards."""
    
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0, fov_bonus=0, health_aspect_bonus=0,
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 attack_traits=None, weaknesses=None, resistances=None,
                 xp_cost=5, description="An enchanted card", is_cleanup=False):
        super().__init__(x, y, name, '#', attack_bonus, defense_bonus, description, fov_bonus, health_aspect_bonus,
                         attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus,
                         evade_bonus, crit_bonus, crit_multiplier_bonus, attack_traits, weaknesses, resistances, xp_cost, is_cleanup)

class Artifact(Accessory):
    """Base class for artifacts"""
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0, fov_bonus=0, health_aspect_bonus=0,
              attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
              evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
              attack_traits=None, weaknesses=None, resistances=None,
              xp_cost=5, description="An enchanted card", is_cleanup=False):
      super().__init__(x, y, name, 'a', attack_bonus, defense_bonus, description, fov_bonus, health_aspect_bonus,
                      attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus,
                      evade_bonus, crit_bonus, crit_multiplier_bonus, attack_traits, weaknesses, resistances, xp_cost, is_cleanup)


class Necklace(Accessory):
    """Base class for necklaces."""
    
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0, fov_bonus=0, health_aspect_bonus=0,
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 attack_traits=None, weaknesses=None, resistances=None,
                 xp_cost=5, description="A magical necklace", is_cleanup=False):
        super().__init__(x, y, name, 'v', attack_bonus, defense_bonus, description, fov_bonus, health_aspect_bonus,
                         attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus,
                         evade_bonus, crit_bonus, crit_multiplier_bonus, attack_traits, weaknesses, resistances, xp_cost, is_cleanup)

class Hat(Accessory):
    """Base class for hats."""
    
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0, fov_bonus=0, health_aspect_bonus=0,
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 attack_traits=None, weaknesses=None, resistances=None,
                 xp_cost=5, description="A cool hat", is_cleanup=False):
        super().__init__(x, y, name, '^', attack_bonus, defense_bonus, description, fov_bonus, health_aspect_bonus,
                         attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus,
                         evade_bonus, crit_bonus, crit_multiplier_bonus, attack_traits, weaknesses, resistances, xp_cost, is_cleanup)


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
        
class StrikeBonus(Hat):
    """+6 ATK on Dark and Ice."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Strike Expertise", 
                        description="+6 ATK on strike attacks")
    
    def get_attack_bonus(self, player):
        pt = player.get_total_attack_traits()
        base_bonus = super().get_attack_bonus(player)
        if Trait.STRIKE in pt:
            return base_bonus + 6
        else:
            return base_bonus
        
class SlashBonus(Hat):
    """+6 ATK on Dark and Ice."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Blade Expertise", 
                        description="+6 ATK on slash attacks")
    
    def get_attack_bonus(self, player):
        pt = player.get_total_attack_traits()
        base_bonus = super().get_attack_bonus(player)
        if Trait.SLASH in pt:
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


class SturdyRock(Accessory):
    """Immunity to stun, immobilized, and off-guard."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Sturdy Rock", '=',
                        description="+1 DEF. Immunity to stun, immobilized, and off-guard",
                        defense_bonus=1)
    
    def blocks_status_effect(self, effect_name):
        """Check if this accessory blocks a specific status effect."""
        return effect_name in ['stun', 'immobilized', 'off_guard']


class PunishTheWeak(Accessory):
    """Deal 25% more damage to enemies with negative status effects."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Punish the Weak", '=',
                        description="-1 DEF. Deal 25% more damage to targets with negative status effects",
                        defense_bonus=-1)
    
    def get_damage_multiplier_vs_target(self, target):
        """Get damage multiplier when attacking a specific target."""
        if hasattr(target, 'status_effects') and target.status_effects.has_negative_effects():
            return 1.25  # 25% more damage
        return 1.0


# New Item Pack 2 Accessories

class ElementalMayhem(Accessory):
    """Grants a +3 attack bonus for every unique elemental trait among attack traits, and resistance traits"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Elemental Mayhem", '=',
                        description="Grants a +3 attack bonus for every unique elemental trait among attack traits and resistance traits")
    
    def get_attack_bonus(self, player):
        """Get attack bonus based on unique elemental traits."""
        base_bonus = super().get_attack_bonus(player)
        
        # Get all attack traits from player
        attack_traits = player.get_total_attack_traits()
        resistance_traits = player.get_total_resistances()
        
        # Combine and count unique elemental traits
        all_traits = set(attack_traits + resistance_traits)
        elemental_traits = {trait for trait in all_traits if trait.is_elemental}
        
        return base_bonus + (len(elemental_traits) * 3)


class GodsEye(Accessory):
    """FOV +20, Holy attack trait"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "God's Eye", '=',
                        description="FOV +20, Holy attack trait",
                        fov_bonus=20,
                        attack_traits=[Trait.HOLY])


class SavingThrow(Accessory):
    """If an attack would set your HP to 0 and your starting HP was not 1, your HP becomes 1"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Saving Throw", '=',
                        description="If an attack would set your HP to 0 and your starting HP was not 1, your HP becomes 1")
    
    def prevents_death(self, player, starting_hp):
        """Check if this accessory prevents death."""
        return starting_hp > 1


class Anaglyph(Accessory):
    """Balances stats. ATK = (ATK+DEF)/2, DEF = (DEF+ATK)/2"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Anaglyph", '=',
                        description="Balances stats. ATK = (ATK+DEF)/2, DEF = (DEF+ATK)/2",
                        is_cleanup=True)
    
    def apply_cleanup_effect(self, player, current_attack, current_defense):
        """Apply the stat balancing effect during cleanup phase."""
        balanced_value = (current_attack + current_defense) // 2
        return balanced_value, balanced_value  # new_attack, new_defense


class MallNinja(Accessory):
    """+1 ATK for every weapon in your inventory"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Mall Ninja", '=',
                        description="+1 ATK for every weapon in your inventory")
    
    def get_attack_bonus(self, player):
        """Get attack bonus based on number of weapons in inventory."""
        base_bonus = super().get_attack_bonus(player)
        weapon_count = sum(1 for item in player.inventory if hasattr(item, 'equipment_slot') and item.equipment_slot == 'weapon')
        return base_bonus + weapon_count


class RighteousFury(Accessory):
    """Holy attacks also apply 4 burn damage"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Righteous Fury", '=',
                        description="Holy attacks also apply 4 burn damage")
    
    def on_hit(self, player, target):
        """Apply burn damage when making holy attacks."""

        if hasattr(target, 'status_effects') and Trait.HOLY in player.attack_traits:
            if target.status_effects.apply_status('burn', 4, target):
                return f"{target.name if hasattr(target, 'name') else 'The target'} is burned by righteous fire!"
        return None


class SongOfIceAndFire(Accessory):
    """If on floor 5 or lower, +6 ATK for Ice or fire damage"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Song of Ice and Fire", '=',
                        description="If on floor 5 or lower, +6 ATK for Ice or fire damage")
    
    def get_attack_bonus(self, player):
        """Get attack bonus based on floor and elemental traits."""
        base_bonus = super().get_attack_bonus(player)
        
        # Check if player is on floor 5 or lower
        current_floor = getattr(player, 'current_floor', 1)
        if current_floor > 5:
            return base_bonus
        
        # Check if player has ice or fire attack traits
        attack_traits = player.get_total_attack_traits()
        if Trait.ICE in attack_traits or Trait.FIRE in attack_traits:
            return base_bonus + 6
        
        return base_bonus
        