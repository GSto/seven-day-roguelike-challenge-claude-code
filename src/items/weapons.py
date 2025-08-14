"""
Weapon items for combat.
"""

from constants import COLOR_YELLOW
from .base import Equipment
from .enchantments import Enchantment
from traits import Trait


class Weapon(Equipment):
    """Weapon equipment."""
    
    def __init__(self, x, y, name, char=')', attack_bonus=0, description="", 
                 fov_bonus=0, health_aspect_bonus=0.0, attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 attack_traits=None, weaknesses=None, resistances=None,
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
            attack_traits=attack_traits,
            weaknesses=weaknesses,
            resistances=resistances,
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
        self._update_display_name()
        return True
    
    def get_attack_bonus(self, player):
        """Get attack bonus including enchantments."""
        total = super().get_attack_bonus(player)
        for enchantment in self.enchantments:
            total += enchantment.get_attack_bonus()
        return total
    
    def get_defense_bonus(self, player):
        """Get defense bonus including enchantments."""
        total = super().get_defense_bonus(player)
        for enchantment in self.enchantments:
            total += enchantment.get_defense_bonus()
        return total
    
    def get_fov_bonus(self, player):
        """Get FOV bonus including enchantments."""
        total = super().get_fov_bonus(player)
        for enchantment in self.enchantments:
            total += enchantment.get_fov_bonus()
        return total
    
    def get_health_aspect_bonus(self, player):
        """Get health aspect bonus including enchantments."""
        total = super().get_health_aspect_bonus(player)
        for enchantment in self.enchantments:
            total += enchantment.get_health_aspect_bonus()
        return total
    
    def get_attack_multiplier_bonus(self, player):
        """Get attack multiplier bonus including enchantments."""
        total = super().get_attack_multiplier_bonus(player)
        for enchantment in self.enchantments:
            total += enchantment.get_attack_multiplier_bonus()
        return total
    
    def get_defense_multiplier_bonus(self, player):
        """Get defense multiplier bonus including enchantments."""
        total = super().get_defense_multiplier_bonus(player)
        for enchantment in self.enchantments:
            # Defense multiplier enchantments would be additive here if they existed
            pass
        return total
    
    def get_xp_multiplier_bonus(self, player):
        """Get XP multiplier bonus including enchantments."""
        total = super().get_xp_multiplier_bonus(player)
        for enchantment in self.enchantments:
            total += enchantment.get_xp_multiplier_bonus()
        return total
    
    def get_evade_bonus(self, player):
        """Get evade bonus including enchantments."""
        total = super().get_evade_bonus(player)
        # No evade enchantments currently exist
        return total
    
    def get_crit_bonus(self, player):
        """Get crit bonus including enchantments."""
        total = super().get_crit_bonus(player)
        for enchantment in self.enchantments:
            if hasattr(enchantment, 'get_crit_bonus'):
                total += enchantment.get_crit_bonus()
        return total
    
    def get_crit_multiplier_bonus(self, player):
        """Get crit multiplier bonus including enchantments."""
        total = super().get_crit_multiplier_bonus(player)
        # No crit multiplier enchantments currently exist
        return total
    
    def get_total_attack_traits(self):
        """Get all attack traits including enchantments."""
        return self.get_attack_traits()
    
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
        super().__init__(x, y, "Dagger", ')', 3, "A sharp dagger. free to equip",xp_cost=0, crit_multiplier_bonus=0.5, attack_traits=[Trait.SLASH])

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
        super().__init__(x, y, "Sword", ')', 5, "A well-balanced sword", attack_traits=[Trait.SLASH])

class Longsword(Weapon):
    """Powerful two-handed weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Longsword", ')', 8, "A two-handed longsword", attack_traits=[Trait.SLASH])


class WarScythe(Weapon):
    """Heavy weapon for maximum damage."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "War Scythe", ')', 12, "A long, brutal weapon", attack_traits=[Trait.SLASH])

## Blunt weapons
## Standard stiking weapons
class Axe(Weapon):
    """Balanced weapon for mid-game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Axe", ')', 6, "An axe", attack_traits=[Trait.STRIKE])
class MorningStar(Weapon):
    """Powerful two-handed weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Morning Star", ')', 9, "A two-handed club", attack_traits=[Trait.STRIKE])

class WarHammer(Weapon):
    """Heavy weapon for maximum damage."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "War Hammer", ')', 12, "A heavy war hammer", attack_traits=[Trait.STRIKE])


## Katanas
## Critical Chance Based weapons
class Katana(Weapon):
    def __init__(self, x, y):
      super().__init__(x, y, "Katana", ')', 4, "A light, fast blade", crit_bonus=0.25, attack_traits=[Trait.SLASH])

class Uchigatana(Weapon):
    def __init__(self, x, y):
      super().__init__(x, y, "Uchigatana", ')', 7, "A samurai warrior's blade", crit_bonus=0.20, attack_traits=[Trait.SLASH])

class RiversOfBlood(Weapon):
    def __init__(self, x, y):
      super().__init__(x, y, "Rivers of Blood", ')', 11, "A samurai warrior's blade", crit_bonus=0.20, crit_multiplier_bonus=0.25, attack_traits=[Trait.SLASH])

## Staffs
## Tend to focus on non-combat stats, or have different 'magical' abilities
class ClericsStaff(Weapon):
    """Holy staff that enhances healing abilities."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Cleric's Staff", ')', 4, "A holy staff that enhances healing", health_aspect_bonus=0.2, attack_traits=[Trait.HOLY, Trait.MYSTIC])

class MateriaStaff(Weapon):
        def __init__(self, x, y):
          super().__init__(x, y, "Materia Staff", ')', 2, "A staff that gets better with enchantments", attack_traits=[Trait.MYSTIC])
          self.no_initial_enchantments = True

        def get_attack_bonus(self, player):
            base_attack = super().get_attack_bonus(player) 
            enchant_count = len(self.enchantments)
            if(player.armor is not None): 
                enchant_count += len(player.armor.enchantments)
            if enchant_count == 0:
              return base_attack
            elif enchant_count == 1:
              return base_attack + 3
            elif enchant_count == 2: 
              return base_attack + 6
            elif enchant_count == 3:
              return base_attack + 9 
            else:
              return base_attack + 12
                

# Special Weapons
class Pickaxe(Weapon):
    """Gloves that enhance your natural strength."""

    def __init__(self, x, y):
        super().__init__(x, y, "Pickaxe", ')', 6, "Favorite of Miners, scales with light")

        def get_attack_multiplier_bonus(self, player):
            return max(1, player.fov)

class Gauntlets(Weapon):
    """Gloves that enhance your natural strength."""

    def __init__(self, x, y):
        super().__init__(x, y, "Gauntlets", ')', 0, "Enhances natural strength", attack_multiplier_bonus=2)


class DemonSlayer(Weapon):
    """Legendary weapon designed to slay demons."""

    def __init__(self, x, y):
        super().__init__(x, y, "Demon Slayer", ')', 15, "A legendary blade forged to slay demons", 
                         attack_traits=[Trait.DEMONSLAYER, Trait.SLASH], xp_cost=100)