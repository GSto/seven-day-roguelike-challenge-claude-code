"""
Player character implementation.
"""

from constants import COLOR_WHITE
from traits import Trait


class Player:
    """Represents the player character."""
    
    def __init__(self, x, y):
        """Initialize the player."""
        self.x = x
        self.y = y
        self.char = '@'
        self.color = COLOR_WHITE
        
        # Player stats
        self.max_hp = 50
        self.hp = self.max_hp
        self.attack = 7
        self.defense = 2
        self.level = 1
        self.xp = 0
        self.xp_to_next = 50
        self.fov = 10  # Field of view radius
        self.health_aspect = 0.3  # Health potion effectiveness multiplier
        
        # Combat stats
        self.evade = 0.05  # 5% base evade chance
        self.crit = 0.05  # 5% base crit chance
        self.crit_multiplier = 2.0  # 2x damage on critical hit
        
        # Multiplier stats for equipment/consumable bonuses
        self.attack_multiplier = 1.0
        self.defense_multiplier = 1.0
        self.xp_multiplier = 1.0
        
        # Equipment slots - start with basic equipment
        from items import WoodenStick, WhiteTShirt
        self.weapon = WoodenStick(0, 0)  # Starting weapon
        self.armor = WhiteTShirt(0, 0)   # Starting armor
        self.accessories = [None, None, None]  # List of equipped accessories
        self.accessory_slots = 3  # Number of accessory slots available
        
        # Inventory
        self.inventory = []
        self.inventory_size = 20

        # counts (used for item scaling)
        self.crit_count = 0
        self.heal_count = 0
        self.body_count = 0
        self.dodge_count = 0
        self.consumable_count = 0
        
        # Traits system
        self.attack_traits = []  # List of Aspect enums for attack
        self.weaknesses = []     # List of Aspect enums for weaknesses
        self.resistances = []    # List of Aspect enums for resistances
    
    def move(self, dx, dy):
        """Move the player by dx, dy."""
        self.x += dx
        self.y += dy
    
    def take_damage(self, damage):
        """Take damage, accounting for defense."""
        actual_damage = max(1, damage - self.get_total_defense())
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount):
        """Heal the player."""
        if(self.hp < self.max_hp):
            self.heal_count += 1
        self.hp = min(self.max_hp, self.hp + amount)
    
    def is_alive(self):
        """Check if the player is alive."""
        return self.hp > 0
    
    def gain_xp(self, amount):
        """Gain experience points with multiplier."""
        self.xp += int(amount * self.get_total_xp_multiplier())
        return False  # No automatic leveling
    
    def can_level_up(self):
        """Check if player has enough XP to level up."""
        return self.xp >= self.xp_to_next
    
    def attempt_level_up(self):
        """Try to level up manually. Returns True if successful."""
        if not self.can_level_up():
            return False
        
        self.level_up()
        return True
    
    def level_up(self):
        """Level up the player."""
        self.xp -= self.xp_to_next
        self.level += 1
        self.xp_to_next = int(self.xp_to_next * 1.4)
        
        # Increase stats
        old_max_hp = self.max_hp
        self.max_hp  = int(self.max_hp * 1.2)
        hp_gained = self.max_hp - old_max_hp
        self.hp = min(self.hp + hp_gained, self.max_hp)  # heal for HP gained without going over max
        
        if self.level % 3 == 0:
          self.defense += 1
        else:
          self.attack += 1
        
        # Return level up info for UI message
        return True
    
    def add_item(self, item):
        """Add an item to inventory if there's space."""
        if len(self.inventory) < self.inventory_size:
            self.inventory.append(item)
            return True
        return False
    
    def remove_item(self, item):
        """Remove an item from inventory."""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def get_attack_bonus(self): 
        total = 0
        if self.weapon:
            total += self.weapon.get_attack_bonus(self)
        if self.armor and hasattr(self.armor, 'attack_bonus'):
            total += self.armor.get_attack_bonus(self)
        for accessory in self.equipped_accessories():
            total += accessory.get_attack_bonus(self)
        return total
    
    def get_total_attack(self):
        """Get total attack power including equipment and multipliers."""
        total = self.attack + self.get_attack_bonus()
        return max(1, int(total * self.get_total_attack_multiplier())) # attack cannot fall below 1
    
    def get_total_defense(self):
        """Get total defense including equipment and multipliers."""
        total = self.defense
        if self.weapon:
            total += self.weapon.get_defense_bonus(self)
        if self.armor:
            total += self.armor.get_defense_bonus(self)
        for accessory in self.equipped_accessories():
            total += accessory.get_defense_bonus(self)
        return int(total * self.get_total_defense_multiplier())
    
    def get_total_fov(self):
        """Get total field of view including equipment bonuses."""
        total = self.fov
        if self.weapon and hasattr(self.weapon, 'fov_bonus'):
            total += self.weapon.fov_bonus
        if self.armor and hasattr(self.armor, 'fov_bonus'):
            total += self.armor.fov_bonus
        for accessory in self.equipped_accessories():
            if hasattr(accessory, 'fov_bonus'):
                total += accessory.fov_bonus
        return total
    
    def get_total_health_aspect(self):
        """Get total health aspect including equipment bonuses."""
        total = self.health_aspect
        if self.weapon and hasattr(self.weapon, 'health_aspect_bonus'):
            total += self.weapon.health_aspect_bonus
        if self.armor and hasattr(self.armor, 'health_aspect_bonus'):
            total += self.armor.health_aspect_bonus
        for accessory in self.equipped_accessories():
            if hasattr(accessory, 'health_aspect_bonus'):
                total += accessory.health_aspect_bonus
        return total
    
    def get_total_attack_multiplier(self):
        """Get total attack multiplier including equipment bonuses."""
        total = self.attack_multiplier
        if self.weapon and hasattr(self.weapon, 'attack_multiplier_bonus'):
            total *= self.weapon.get_attack_multiplier_bonus(self)
        if self.armor and hasattr(self.armor, 'attack_multiplier_bonus'):
            total *= self.armor.get_attack_multiplier_bonus(self)
        for accessory in self.equipped_accessories():
            if hasattr(accessory, 'attack_multiplier_bonus'):
                total *= accessory.get_attack_multiplier_bonus(self)
        return total
    
    def get_total_defense_multiplier(self):
        """Get total defense multiplier including equipment bonuses."""
        total = self.defense_multiplier
        if self.weapon and hasattr(self.weapon, 'defense_multiplier_bonus'):
            total *= self.weapon.get_defense_multiplier_bonus(self)
        if self.armor and hasattr(self.armor, 'defense_multiplier_bonus'):
            total *= self.armor.get_defense_multiplier_bonus(self)
        for accessory in self.equipped_accessories():
            if hasattr(accessory, 'defense_multiplier_bonus'):
                total *= accessory.get_defense_multiplier_bonus(self)
        return total
    
    def get_total_xp_multiplier(self):
        """Get total XP multiplier including equipment bonuses."""
        total = self.xp_multiplier
        if self.weapon and hasattr(self.weapon, 'xp_multiplier_bonus'):
            total *= self.weapon.get_xp_multiplier_bonus(self)
        if self.armor and hasattr(self.armor, 'xp_multiplier_bonus'):
            total *= self.armor.get_xp_multiplier_bonus(self)
        for accessory in self.equipped_accessories():
            if hasattr(accessory, 'xp_multiplier_bonus'):
                total *= accessory.get_xp_multiplier_bonus(self)
        return total
    
    def get_total_evade(self):
        """Get total evade chance including equipment bonuses."""
        total = self.evade
        if self.weapon and hasattr(self.weapon, 'evade_bonus'):
            total += self.weapon.evade_bonus
        if self.armor and hasattr(self.armor, 'evade_bonus'):
            total += self.armor.evade_bonus
        for accessory in self.equipped_accessories():
            if hasattr(accessory, 'evade_bonus'):
                total += accessory.evade_bonus
        return min(0.75, total)  # Cap at 75% evade
    
    def get_total_crit(self):
        """Get total crit chance including equipment bonuses."""
        total = self.crit
        if self.weapon and hasattr(self.weapon, 'crit_bonus'):
            total += self.weapon.crit_bonus
        if self.armor and hasattr(self.armor, 'crit_bonus'):
            total += self.armor.crit_bonus
        for accessory in self.equipped_accessories():
            if hasattr(accessory, 'crit_bonus'):
                total += accessory.crit_bonus
        return min(0.75, total)  # Cap at 75% crit
    
    def get_total_crit_multiplier(self):
        """Get total crit multiplier including equipment bonuses."""
        total = self.crit_multiplier
        if self.weapon and hasattr(self.weapon, 'crit_multiplier_bonus'):
            total += self.weapon.crit_multiplier_bonus
        if self.armor and hasattr(self.armor, 'crit_multiplier_bonus'):
            total += self.armor.crit_multiplier_bonus
        for accessory in self.equipped_accessories():
            if hasattr(accessory, 'crit_multiplier_bonus'):
                total += accessory.crit_multiplier_bonus
        return total
    
    def equipped_accessories(self):
        return [acc for acc in self.accessories if acc is not None]
    
    def get_total_attack_traits(self):
        """Get all attack traits including equipment bonuses."""
        total_traits = self.attack_traits.copy()
        if self.weapon:
            total_traits.extend(self.weapon.get_attack_traits())
        if self.armor:
            total_traits.extend(self.armor.get_attack_traits())
        for accessory in self.equipped_accessories():
            total_traits.extend(accessory.get_attack_traits())
        return total_traits
    
    def get_total_weaknesses(self):
        """Get all weaknesses including equipment effects."""
        total_weaknesses = self.weaknesses.copy()
        if self.weapon:
            total_weaknesses.extend(self.weapon.get_weaknesses())
        if self.armor:
            total_weaknesses.extend(self.armor.get_weaknesses())
        for accessory in self.equipped_accessories():
            total_weaknesses.extend(accessory.get_weaknesses())
        return total_weaknesses
    
    def get_total_resistances(self):
        """Get all resistances including equipment bonuses."""
        total_resistances = self.resistances.copy()
        if self.weapon:
            total_resistances.extend(self.weapon.get_resistances())
        if self.armor:
            total_resistances.extend(self.armor.get_resistances())
        for accessory in self.equipped_accessories():
            total_resistances.extend(accessory.get_resistances())
        return total_resistances
    
    def render(self, console, fov):
        """Render the player on the console."""
        # Player should always be visible (they're the center of vision)
        console.print(self.x, self.y, self.char, fg=self.color)