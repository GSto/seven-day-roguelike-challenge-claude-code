"""
Player character implementation.
"""

from constants import COLOR_WHITE


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
        
        # Multiplier stats for equipment/consumable bonuses
        self.attack_multiplier = 1.0
        self.defense_multiplier = 1.0
        self.xp_multiplier = 1.0
        
        # Equipment slots - start with basic equipment
        from items import WoodenStick, WhiteTShirt
        self.weapon = WoodenStick(0, 0)  # Starting weapon
        self.armor = WhiteTShirt(0, 0)   # Starting armor
        self.accessory = None
        
        # Inventory
        self.inventory = []
        self.inventory_size = 20
    
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
    
    def get_total_attack(self):
        """Get total attack power including equipment and multipliers."""
        total = self.attack
        if self.weapon:
            total += self.weapon.attack_bonus
        if self.armor and hasattr(self.armor, 'attack_bonus'):
            total += self.armor.attack_bonus
        if self.accessory:
            total += self.accessory.attack_bonus
        return int(total * self.get_total_attack_multiplier())
    
    def get_total_defense(self):
        """Get total defense including equipment and multipliers."""
        total = self.defense
        if self.armor:
            total += self.armor.defense_bonus
        if self.accessory:
            total += self.accessory.defense_bonus
        return int(total * self.get_total_defense_multiplier())
    
    def get_total_fov(self):
        """Get total field of view including equipment bonuses."""
        total = self.fov
        if self.weapon and hasattr(self.weapon, 'fov_bonus'):
            total += self.weapon.fov_bonus
        if self.armor and hasattr(self.armor, 'fov_bonus'):
            total += self.armor.fov_bonus
        if self.accessory and hasattr(self.accessory, 'fov_bonus'):
            total += self.accessory.fov_bonus
        return total
    
    def get_total_health_aspect(self):
        """Get total health aspect including equipment bonuses."""
        total = self.health_aspect
        if self.weapon and hasattr(self.weapon, 'health_aspect_bonus'):
            total += self.weapon.health_aspect_bonus
        if self.armor and hasattr(self.armor, 'health_aspect_bonus'):
            total += self.armor.health_aspect_bonus
        if self.accessory and hasattr(self.accessory, 'health_aspect_bonus'):
            total += self.accessory.health_aspect_bonus
        return total
    
    def get_total_attack_multiplier(self):
        """Get total attack multiplier including equipment bonuses."""
        total = self.attack_multiplier
        if self.weapon and hasattr(self.weapon, 'attack_multiplier_bonus'):
            total += self.weapon.attack_multiplier_bonus
        if self.armor and hasattr(self.armor, 'attack_multiplier_bonus'):
            total += self.armor.attack_multiplier_bonus
        if self.accessory and hasattr(self.accessory, 'attack_multiplier_bonus'):
            total += self.accessory.attack_multiplier_bonus
        return total
    
    def get_total_defense_multiplier(self):
        """Get total defense multiplier including equipment bonuses."""
        total = self.defense_multiplier
        if self.weapon and hasattr(self.weapon, 'defense_multiplier_bonus'):
            total += self.weapon.defense_multiplier_bonus
        if self.armor and hasattr(self.armor, 'defense_multiplier_bonus'):
            total += self.armor.defense_multiplier_bonus
        if self.accessory and hasattr(self.accessory, 'defense_multiplier_bonus'):
            total += self.accessory.defense_multiplier_bonus
        return total
    
    def get_total_xp_multiplier(self):
        """Get total XP multiplier including equipment bonuses."""
        total = self.xp_multiplier
        if self.weapon and hasattr(self.weapon, 'xp_multiplier_bonus'):
            total += self.weapon.xp_multiplier_bonus
        if self.armor and hasattr(self.armor, 'xp_multiplier_bonus'):
            total += self.armor.xp_multiplier_bonus
        if self.accessory and hasattr(self.accessory, 'xp_multiplier_bonus'):
            total += self.accessory.xp_multiplier_bonus
        return total
    
    def render(self, console, fov):
        """Render the player on the console."""
        # Player should always be visible (they're the center of vision)
        console.print(self.x, self.y, self.char, fg=self.color)