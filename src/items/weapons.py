"""
Weapon items for combat.
"""

from constants import COLOR_YELLOW
from .base import Equipment
from .enchantments import Enchantment


class Weapon(Equipment):
    """Weapon equipment."""
    
    def __init__(self, x, y, name, char=')', attack_bonus=0, description="", 
                 fov_bonus=0, health_aspect_bonus=0.0, attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 xp_cost=5):
        self.enchantments = []
        self.base_name = name
        
        super().__init__(
            x=x, y=y,
            name=name,
            char=char,
            color=COLOR_YELLOW,
            description=description,
            attack_bonus=attack_bonus,
            equipment_slot="weapon",
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
    
    def add_enchantment(self, enchantment):
        """Add an enchantment to this weapon (max 2 enchantments)."""
        if len(self.enchantments) >= 2:
            return False
        
        # Check if enchantment type already exists
        for existing_enchantment in self.enchantments:
            if existing_enchantment.type == enchantment.type:
                return False
        
        self.enchantments.append(enchantment)
        self._update_stats_from_enchantments()
        self._update_display_name()
        return True
    
    def _update_stats_from_enchantments(self):
        """Update weapon stats based on current enchantments."""
        # Store base values if we haven't already
        if not hasattr(self, '_base_attack_bonus'):
            self._base_attack_bonus = self.attack_bonus
            self._base_defense_bonus = self.defense_bonus
            self._base_fov_bonus = self.fov_bonus
            self._base_health_aspect_bonus = self.health_aspect_bonus
            self._base_attack_multiplier_bonus = self.attack_multiplier_bonus
            self._base_xp_multiplier_bonus = self.xp_multiplier_bonus
            self._base_evade_bonus = self.evade_bonus
            self._base_crit_bonus = self.crit_bonus
            self._base_crit_multiplier_bonus = self.crit_multiplier_bonus
        
        # Start with base values
        total_attack = self._base_attack_bonus
        total_defense = self._base_defense_bonus
        total_fov = self._base_fov_bonus
        total_health_aspect = self._base_health_aspect_bonus
        total_attack_multiplier = self._base_attack_multiplier_bonus
        total_xp_multiplier = self._base_xp_multiplier_bonus
        total_crit = self._base_crit_bonus
        
        # Apply enchantment bonuses
        for enchantment in self.enchantments:
            total_attack += enchantment.get_attack_bonus()
            total_defense += enchantment.get_defense_bonus()
            total_fov += enchantment.get_fov_bonus()
            total_health_aspect += enchantment.get_health_aspect_bonus()
            total_attack_multiplier += enchantment.get_attack_multiplier_bonus()
            total_xp_multiplier += enchantment.get_xp_multiplier_bonus()
            if hasattr(enchantment, 'get_crit_bonus'):
                total_crit += enchantment.get_crit_bonus()
        
        # Update the actual stats
        self.attack_bonus = total_attack
        self.defense_bonus = total_defense
        self.fov_bonus = total_fov
        self.health_aspect_bonus = total_health_aspect
        self.attack_multiplier_bonus = total_attack_multiplier
        self.xp_multiplier_bonus = total_xp_multiplier
        self.crit_bonus = total_crit
    
    def _update_display_name(self):
        """Update the display name to include enchantments."""
        if not self.enchantments:
            self.name = self.base_name
        else:
            enchantment_names = [e.name for e in self.enchantments]
            self.name = f"{' '.join(enchantment_names)} {self.base_name}" 


# Specific weapon types


# Basic Weapons
class WoodenStick(Weapon):
    """Basic starting weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Wooden Stick", ')', 1, "A simple wooden stick", xp_cost=0)


## Short blade
# Tend to have a higher critical bonus. when you stab you STAB! 
class Dagger(Weapon):
    """Light, fast weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Dagger", ')', 3, "A sharp dagger. free to equip",xp_cost=0, crit_multiplier_bonus=0.5)

## Shields
## Trade an attack bonus for a defensive buff
class Shield(Weapon):
    """Defensive "weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Shield", ')', attack_bonus=0, defense_multiplier_bonus=1.25, description="A shield.")

class TowerShield(Weapon):
    """Defensive "weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Tower Shield", ')', attack_bonus=1, defense_multiplier_bonus=1.5, description="A large powerful shield")


## Long Blade
## Standard slashing weapons
class Sword(Weapon):
    """Balanced weapon for mid-game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Sword", ')', 5, "A well-balanced sword")

class Longsword(Weapon):
    """Powerful two-handed weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Longsword", ')', 8, "A two-handed longsword")


class WarScythe(Weapon):
    """Heavy weapon for maximum damage."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "War Scythe", ')', 12, "A long, brutal weapon")

## Blunt weapons
## Standard stiking weapons
class Axe(Weapon):
    """Balanced weapon for mid-game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Axe", ')', 6, "An axe")
class MorningStar(Weapon):
    """Powerful two-handed weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Morning Star", ')', 9, "A two-handed club")

class WarHammer(Weapon):
    """Heavy weapon for maximum damage."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "War Hammer", ')', 12, "A heavy war hammer")


## Katanas
## Critical Chance Based weapons
class Katana(Weapon):
    def __init__(self, x, y):
      super().__init__(x, y, "Katana", ')', 4, "A light, fast blade", crit_bonus=0.25)

class Uchigatana(Weapon):
    def __init__(self, x, y):
      super().__init__(x, y, "Uchigatana", ')', 7, "A samurai warrior's blade", crit_bonus=0.20)

class RiversOfBlood(Weapon):
    def __init__(self, x, y):
      super().__init__(x, y, "Rivers of Blood", ')', 11, "A samurai warrior's blade", crit_bonus=0.20, crit_multiplier_bonus=0.25)

## Staffs
## Tend to focus on non-combat stats, or have different 'magical' abilities
class ClericsStaff(Weapon):
    """Holy staff that enhances healing abilities."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Cleric's Staff", ')', 4, "A holy staff that enhances healing", health_aspect_bonus=0.2)

class MateriaStaff(Weapon):
        def __init__(self, x, y):
          super().__init__(x, y, "Materia Staff", ')', 2, "A staff that gets better when enchanted")

        def get_attack_bonus(self, player):
            base_attack = super().get_attack_bonus(player) 
            enchant_count = len(self.enchantments)
            if enchant_count == 0:
              return base_attack
            elif enchant_count == 1:
              return base_attack + 6
            else:
              return base_attack + 12
                


class Gauntlets(Weapon):
    """Gloves that enhance your natural strength."""

    def __init__(self, x, y):
        super().__init__(x, y, "Gauntlets", ')', 0, "Enhances natural strength", attack_multiplier_bonus=1.5)