"""
Weapon items for combat.
"""

from constants import COLOR_YELLOW
from .equipment import Equipment
from enchantments import Enchantment
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
            total += self.get_enchantment_bonus(enchantment, "attack", player)
        return total
    
    def get_defense_bonus(self, player):
        """Get defense bonus including enchantments."""
        total = super().get_defense_bonus(player)
        for enchantment in self.enchantments:
            total += self.get_enchantment_bonus(enchantment, "defense", player)
        return total
    
    def get_fov_bonus(self, player):
        """Get FOV bonus including enchantments."""
        total = super().get_fov_bonus(player)
        for enchantment in self.enchantments:
            total += self.get_enchantment_bonus(enchantment, "fov", player)
        return total
    
    def get_health_aspect_bonus(self, player):
        """Get health aspect bonus including enchantments."""
        total = super().get_health_aspect_bonus(player)
        for enchantment in self.enchantments:
            total += self.get_enchantment_bonus(enchantment, "health_aspect", player)
        return total
    
    def get_attack_multiplier_bonus(self, player):
        """Get attack multiplier bonus including enchantments."""
        total = super().get_attack_multiplier_bonus(player)
        for enchantment in self.enchantments:
            total += self.get_enchantment_bonus(enchantment, "attack_multiplier", player)
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
            total += self.get_enchantment_bonus(enchantment, "xp_multiplier", player)
        return total
    
    def get_enchantment_bonus(self, enchantment, bonus_type, player):
        """
        Override method to customize enchantment effects for specific weapons.
        
        Args:
            enchantment: The enchantment to get bonus from
            bonus_type: Type of bonus ("attack", "defense", "fov", etc.)
            player: Player instance for context
            
        Returns:
            The bonus value for this enchantment and bonus type
        """
        # Default behavior - call the appropriate method on the enchantment
        weapon_method_name = f"get_weapon_{bonus_type}_bonus"
        shared_method_name = f"get_{bonus_type}_bonus"
        
        if hasattr(enchantment, weapon_method_name):
            return getattr(enchantment, weapon_method_name)()
        elif hasattr(enchantment, shared_method_name):
            return getattr(enchantment, shared_method_name)()
        return 0.0
    
    def get_evade_bonus(self, player):
        """Get evade bonus including enchantments."""
        total = super().get_evade_bonus(player)
        # No evade enchantments currently exist
        return total
    
    def get_crit_bonus(self, player):
        """Get crit bonus including enchantments."""
        total = super().get_crit_bonus(player)
        for enchantment in self.enchantments:
            total += self.get_enchantment_bonus(enchantment, "crit", player)
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
        super().__init__(x, y, "Wooden Stick", ')', 1, "A simple wooden stick", xp_cost=0, attack_traits=[Trait.STRIKE])


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
        super().__init__(x, y, "Shield", ')', 1, defense_multiplier_bonus=1.25, description="A shield.", attack_traits=[Trait.STRIKE])

class TowerShield(Weapon):
    """Defensive "weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Tower Shield", ')', 1, defense_multiplier_bonus=1.5, description="A large powerful shield", attack_traits=[Trait.STRIKE])
        self.defense_bonus = 4

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
      super().__init__(x, y, "Katana", ')', 4, "A light, fast blade", crit_bonus=0.15, attack_traits=[Trait.SLASH])

class Uchigatana(Weapon):
    def __init__(self, x, y):
      super().__init__(x, y, "Uchigatana", ')', 7, "A samurai warrior's blade", crit_bonus=0.15, attack_traits=[Trait.SLASH])

class RiversOfBlood(Weapon):
    def __init__(self, x, y):
      super().__init__(x, y, "Rivers of Blood", ')', 11, "A samurai warrior's blade", crit_bonus=0.20, crit_multiplier_bonus=0.25, attack_traits=[Trait.SLASH])

## Staffs
## Tend to focus on non-combat stats, or have different 'magical' abilities
class ClericsStaff(Weapon):
    """Holy staff that enhances healing abilities."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Cleric's Staff", ')', 4, "A holy staff that enhances healing", health_aspect_bonus=0.2, attack_traits=[Trait.HOLY, Trait.MYSTIC])
    
    def get_enchantment_bonus(self, enchantment, bonus_type, player):
        """Override to give special bonuses for BLESSED and HOLY enchantments."""
        from enchantments import EnchantmentType
        
        # Get base bonus
        base_bonus = super().get_enchantment_bonus(enchantment, bonus_type, player)
        
        # Special bonuses for BLESSED and HOLY enchantments on Cleric's Staff
        if enchantment.type in [EnchantmentType.BLESSED, EnchantmentType.HOLY]:
            if bonus_type == "attack":
                base_bonus += 4  # Additional +4 ATK bonus
            elif bonus_type == "health_aspect":
                base_bonus += 0.10  # Additional +10% health aspect bonus
        
        return base_bonus

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
        super().__init__(x, y, "Pickaxe", ')', 6, "Favorite of Miners, scales with light", attack_traits=[Trait.STRIKE])

        def get_attack_multiplier_bonus(self, player):
            return min(1, 1 + (player.get_total_fov() / 100)) # return 1 so we don't accidently scale down

class Gauntlets(Weapon):
    """Gloves that enhance your natural strength."""

    def __init__(self, x, y):
        super().__init__(x, y, "Gauntlets", ')', 0, "Enhances natural strength", attack_multiplier_bonus=2, attack_traits=[Trait.STRIKE])


class DemonSlayer(Weapon):
    """Legendary weapon designed to slay demons."""

    def __init__(self, x, y):
        super().__init__(x, y, "Demon Slayer", ')', 15, "A legendary blade forged to slay demons", 
                         attack_traits=[Trait.DEMONSLAYER, Trait.SLASH], xp_cost=100)


class SnakesFang(Weapon):
    """Venomous blade that applies poison on hit."""

    def __init__(self, x, y):
        super().__init__(x, y, "Snake's Fang", ')', 4, "Deals slash & poison damage. Applies additional poison on hit", 
                         attack_traits=[Trait.SLASH, Trait.POISON])
    
    def on_hit(self, player, target):
        """Apply additional poison when hitting a target."""
        if hasattr(target, 'status_effects'):
            if target.status_effects.apply_status('poison', 5, target):
                return f"The venom seeps into {target.name if hasattr(target, 'name') else 'the target'}!"
        return None


class Rapier(Weapon):
    """Elegant blade that leaves enemies off-guard."""

    def __init__(self, x, y):
        super().__init__(x, y, "Rapier", ')', 6, "Mid-game weapon that applies off-guard on attack", 
                         attack_traits=[Trait.SLASH])
    
    def on_hit(self, attacker, target):
        """Apply off-guard status when hitting a target."""
        if hasattr(target, 'status_effects'):
            if target.status_effects.apply_status('off_guard', 1, target):
                return f"{target.name if hasattr(target, 'name') else 'The target'} is caught off-guard!"
        return None


# New Item Pack 2 Weapons

class AcidDagger(Weapon):
    """Mid game weapon. 6 dmg. Apply 4 burn and 4 poison on every hit. Slash, Fire, Poison damage."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Acid Dagger", ')', 6, 
                        "Mid game weapon. 6 dmg. Apply 4 burn and 4 poison on every hit. Slash, Fire, Poison damage.",
                        attack_traits=[Trait.SLASH, Trait.FIRE, Trait.POISON])
    
    def on_hit(self, attacker, target):
        """Apply burn and poison when hitting a target."""
        messages = []
        if hasattr(target, 'status_effects'):
            if target.status_effects.apply_status('burn', 4, target):
                messages.append(f"{target.name if hasattr(target, 'name') else 'The target'} is burned by acid!")
            if target.status_effects.apply_status('poison', 4, target):
                messages.append(f"{target.name if hasattr(target, 'name') else 'The target'} is poisoned!")
        return " ".join(messages) if messages else None


class ClairObscur(Weapon):
    """Late game weapon. 10 dmg. Deals light, dark, and mystic damage"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Clair Obscur", ')', 10, 
                        "Late game weapon. 10 dmg. Deals light, dark, and mystic damage",
                        attack_traits=[Trait.HOLY, Trait.DARK, Trait.MYSTIC])


class FeuGlace(Weapon):
    """Late game weapon. 10 dmg. Deals fire, ice, and mystic damage"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Feu-Glace", ')', 10, 
                        "Late game weapon. 10 dmg. Deals fire, ice, and mystic damage",
                        attack_traits=[Trait.FIRE, Trait.ICE, Trait.MYSTIC])


class BigStick(Weapon):
    """Mid-game weapons. strike. 50% chance to apply stun. 50% chance to apply immobilized."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Big Stick", ')', 5, 
                        "Mid-game weapons. strike. 50% chance to apply stun. 50% chance to apply immobilized.",
                        attack_traits=[Trait.STRIKE])
    
    def on_hit(self, attacker, target):
        """Apply random status effects when hitting a target."""
        import random
        messages = []
        if hasattr(target, 'status_effects'):
            if random.random() < 0.5:  # 50% chance for stun
                if target.status_effects.apply_status('stun', 1, target):
                    messages.append(f"{target.name if hasattr(target, 'name') else 'The target'} is stunned!")
            if random.random() < 0.5:  # 50% chance for immobilized
                if target.status_effects.apply_status('immobilized', 1, target):
                    messages.append(f"{target.name if hasattr(target, 'name') else 'The target'} is immobilized!")
        return " ".join(messages) if messages else None