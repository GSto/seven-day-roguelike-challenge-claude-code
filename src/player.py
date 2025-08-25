"""
Player character implementation.
"""

from constants import COLOR_WHITE
from traits import Trait
from status_effects import StatusEffects
from entity import Entity
from stats import Stats, StatType
from event_emitter import EventEmitter
from event_type import EventType
from event_context import HealContext, ConsumeContext, LevelUpContext


class Player(Entity):
    """Represents the player character."""
    
    def __init__(self, x, y):
        """Initialize the player."""
        # Create stats for the player
        player_stats = Stats(
            max_hp=50,
            hp=50,
            attack=4,
            defense=1,
            evade=0.05,
            crit=0.05,
            crit_multiplier=2.0,
            attack_multiplier=1.0,
            defense_multiplier=1.0,
            xp_multiplier=1.0,
            xp=0,
            health_aspect=0.3
        )
        
        # Initialize base Entity attributes
        super().__init__(
            x=x,
            y=y,
            character='@',
            color=COLOR_WHITE,
            stats=player_stats
        )
        
        # Player-specific stats not in Stats class
        self.level = 1
        self.xp_to_next = 50
        self.fov = 10  # Field of view radius
        
        # Equipment slots - start with basic equipment
        from items.weapons import WoodenStick
        from items.armor import WhiteTShirt
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
        
        # Catalyst tax system - HP cost for using catalysts
        self.catalyst_tax = 0.1  # Starts at 10%
    
    def take_damage(self, damage):
        """Override to use total defense instead of base defense."""
        actual_damage = max(1, damage - self.get_total_defense())
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def take_damage_with_traits(self, damage, attack_traits=None):
        """Override to use total resistances/weaknesses and total defense."""
        if attack_traits is None:
            attack_traits = []
        
        # Check for trait interactions
        final_damage = damage
        player_resistances = self.get_total_resistances()
        player_weaknesses = self.get_total_weaknesses()
        
        for trait in attack_traits:
            if trait in player_resistances:
                final_damage = int(final_damage * 0.5)  # 50% damage if resistant
            elif trait in player_weaknesses:
                final_damage = int(final_damage * 2.0)  # 200% damage if weak
        
        # Apply normal damage calculation
        actual_damage = max(1, final_damage - self.get_total_defense())
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount):
        """Heal the player."""
        old_hp = self.hp
        if(self.hp < self.max_hp):
            self.heal_count += 1
        self.hp = min(self.max_hp, self.hp + amount)
        
        actual_heal = self.hp - old_hp
        if actual_heal > 0:
            event_emitter = EventEmitter()
            context = HealContext(player=self, amount_healed=actual_heal)
            event_emitter.emit(EventType.PLAYER_HEAL, context)
    
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
        old_level = self.level
        self.level += 1
        self.xp_to_next = int(self.xp_to_next * 1.4)
        
        # Increase stats
        old_max_hp = self.max_hp
        self.max_hp  = int(self.max_hp * 1.2)
        hp_gained = self.max_hp - old_max_hp
        self.hp = min(self.hp + hp_gained, self.max_hp)  # heal for HP gained without going over max
        
        stat_increases = {}
        if self.level % 3 == 0:
          self.defense += 1
          stat_increases['defense'] = 1
        else:
          self.attack += 1
          stat_increases['attack'] = 1
        
        stat_increases['max_hp'] = hp_gained
        
        # Emit level up event
        event_emitter = EventEmitter()
        context = LevelUpContext(player=self, new_level=self.level, stat_increases=stat_increases)
        event_emitter.emit(EventType.LEVEL_UP, context)
        
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
        # Calculate base attack with all bonuses except cleanup
        attack = self._get_total_attack_without_cleanup()
        defense = self._get_total_defense_without_cleanup()
        
        # Apply cleanup effects (like Anaglyph) after all other calculations
        for accessory in self.equipped_accessories():
            if hasattr(accessory, 'is_cleanup') and accessory.is_cleanup:
                if hasattr(accessory, 'apply_cleanup_effect'):
                    attack, defense = accessory.apply_cleanup_effect(self, attack, defense)
        
        return attack
    
    def get_total_defense(self):
        """Get total defense including equipment and multipliers."""
        # Calculate base defense with all bonuses except cleanup
        attack = self._get_total_attack_without_cleanup()
        defense = self._get_total_defense_without_cleanup()
        
        # Apply cleanup effects (like Anaglyph) after all other calculations
        for accessory in self.equipped_accessories():
            if hasattr(accessory, 'is_cleanup') and accessory.is_cleanup:
                if hasattr(accessory, 'apply_cleanup_effect'):
                    attack, defense = accessory.apply_cleanup_effect(self, attack, defense)
        
        return defense
    
    def _get_total_attack_without_cleanup(self):
        """Get total attack without cleanup effects (internal use)."""
        total = self.attack + self.get_attack_bonus()
        return max(1, int(total * self.get_total_attack_multiplier()))
    
    def _get_total_defense_without_cleanup(self):
        """Get total defense without cleanup effects (internal use)."""
        total = self.defense
        if self.weapon:
            total += self.weapon.get_defense_bonus(self)
        if self.armor:
            total += self.armor.get_defense_bonus(self)
        for accessory in self.equipped_accessories():
            # Don't include cleanup accessories' defense bonus here
            if not (hasattr(accessory, 'is_cleanup') and accessory.is_cleanup):
                total += accessory.get_defense_bonus(self)
        return int(total * self.get_total_defense_multiplier())
    
    def get_total_fov(self):
        """Get total field of view including equipment bonuses."""
        total = self.fov
        if self.weapon and hasattr(self.weapon, 'fov_bonus'):
            total += self.weapon.get_fov_bonus(self)
        if self.armor and hasattr(self.armor, 'fov_bonus'):
            total += self.armor.get_fov_bonus(self)
        for accessory in self.equipped_accessories():
            if hasattr(accessory, 'fov_bonus'):
                total += accessory.get_fov_bonus(self)
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
        if self.weapon and hasattr(self.weapon, 'get_evade_bonus'):
            total += self.weapon.get_evade_bonus(self)
        if self.armor and hasattr(self.armor, 'get_evade_bonus'):
            total += self.armor.get_evade_bonus(self)
        for accessory in self.equipped_accessories():
            if hasattr(accessory, 'get_evade_bonus'):
                total += accessory.get_evade_bonus(self)
        return min(0.75, total)  # Cap at 75% evade
    
    def get_total_crit(self):
        """Get total crit chance including equipment bonuses."""
        total = self.crit
        if self.weapon and hasattr(self.weapon, 'get_crit_bonus'):
            total += self.weapon.get_crit_bonus(self)
        if self.armor and hasattr(self.armor, 'get_crit_bonus'):
            total += self.armor.get_crit_bonus(self)
        for accessory in self.equipped_accessories():
            if hasattr(accessory, 'get_crit_bonus'):
                total += accessory.get_crit_bonus(self)
        return min(0.75, total)  # Cap at 75% crit
    
    def get_total_crit_multiplier(self):
        """Get total crit multiplier including equipment bonuses."""
        total = self.crit_multiplier
        if self.weapon and hasattr(self.weapon, 'get_crit_multiplier_bonus'):
            total += self.weapon.get_crit_multiplier_bonus(self)
        if self.armor and hasattr(self.armor, 'get_crit_multiplier_bonus'):
            total += self.armor.get_crit_multiplier_bonus(self)
        for accessory in self.equipped_accessories():
            if hasattr(accessory, 'get_crit_multiplier_bonus'):
                total += accessory.get_crit_multiplier_bonus(self)
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
        """Get all weaknesses including equipment effects, after cancellation with resistances."""
        total_weaknesses = self.weaknesses.copy()
        if self.weapon:
            total_weaknesses.extend(self.weapon.get_weaknesses())
        if self.armor:
            total_weaknesses.extend(self.armor.get_weaknesses())
        for accessory in self.equipped_accessories():
            total_weaknesses.extend(accessory.get_weaknesses())
        
        # Get all resistances for cancellation
        all_resistances = self._get_all_resistances()
        
        # Remove weaknesses that are cancelled by resistances
        final_weaknesses = []
        for weakness in total_weaknesses:
            if weakness not in all_resistances:
                final_weaknesses.append(weakness)
        
        return final_weaknesses
    
    def get_total_resistances(self):
        """Get all resistances including equipment bonuses, after cancellation with weaknesses."""
        all_resistances = self._get_all_resistances()
        
        # Get all weaknesses for cancellation
        all_weaknesses = self._get_all_weaknesses()
        
        # Remove resistances that are cancelled by weaknesses
        final_resistances = []
        for resistance in all_resistances:
            if resistance not in all_weaknesses:
                final_resistances.append(resistance)
        
        return final_resistances
    
    def _get_all_resistances(self):
        """Get all resistances before cancellation."""
        total_resistances = self.resistances.copy()
        if self.weapon:
            total_resistances.extend(self.weapon.get_resistances())
        if self.armor:
            total_resistances.extend(self.armor.get_resistances())
        for accessory in self.equipped_accessories():
            total_resistances.extend(accessory.get_resistances())
        return total_resistances
    
    def _get_all_weaknesses(self):
        """Get all weaknesses before cancellation."""
        total_weaknesses = self.weaknesses.copy()
        if self.weapon:
            total_weaknesses.extend(self.weapon.get_weaknesses())
        if self.armor:
            total_weaknesses.extend(self.armor.get_weaknesses())
        for accessory in self.equipped_accessories():
            total_weaknesses.extend(accessory.get_weaknesses())
        return total_weaknesses
    
    def render(self, console, fov):
        """Render the player on the console."""
        # Player should always be visible (they're the center of vision)
        console.print(self.x, self.y, self.character, fg=self.color)
    
    @property
    def xp(self):
        return self.stats.get_stat(StatType.XP)
    
    @xp.setter
    def xp(self, value):
        self.stats.set_stat(StatType.XP, value)
    
    @property
    def xp_multiplier(self):
        return self.stats.get_stat(StatType.XP_MULTIPLIER)
    
    @xp_multiplier.setter
    def xp_multiplier(self, value):
        self.stats.set_stat(StatType.XP_MULTIPLIER, value)
    
    @property
    def health_aspect(self):
        return self.stats.get_stat(StatType.HEALTH_ASPECT)
    
    @health_aspect.setter
    def health_aspect(self, value):
        self.stats.set_stat(StatType.HEALTH_ASPECT, value)