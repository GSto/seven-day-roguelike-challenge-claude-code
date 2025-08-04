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
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack = 10
        self.defense = 2
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        
        # Equipment slots
        self.weapon = None
        self.armor = None
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
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount):
        """Heal the player."""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def is_alive(self):
        """Check if the player is alive."""
        return self.hp > 0
    
    def gain_xp(self, amount):
        """Gain experience points."""
        self.xp += amount
        
        # Check for level up
        leveled_up = False
        while self.xp >= self.xp_to_next:
            self.level_up()
            leveled_up = True
        
        return leveled_up
    
    def level_up(self):
        """Level up the player."""
        self.xp -= self.xp_to_next
        self.level += 1
        self.xp_to_next = int(self.xp_to_next * 1.5)
        
        # Increase stats
        old_max_hp = self.max_hp
        self.max_hp += 20
        self.hp += (self.max_hp - old_max_hp)  # Heal to full on level up
        self.attack += 3
        self.defense += 1
        
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
        """Get total attack power including equipment."""
        total = self.attack
        if self.weapon:
            total += self.weapon.attack_bonus
        return total
    
    def get_total_defense(self):
        """Get total defense including equipment."""
        total = self.defense
        if self.armor:
            total += self.armor.defense_bonus
        if self.accessory:
            total += self.accessory.defense_bonus
        return total
    
    def render(self, console, fov):
        """Render the player on the console."""
        # Player should always be visible (they're the center of vision)
        console.print(self.x, self.y, self.char, fg=self.color)