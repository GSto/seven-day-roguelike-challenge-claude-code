"""
Status effects system for the roguelike game.
"""


class StatusEffects:
    """Manages status effect counters for players and monsters."""
    
    def __init__(self):
        """Initialize all status effects to 0."""
        # Negative status effects
        self.burn = 0          # Takes N fire damage per turn, removes 1
        self.poison = 0        # Takes N poison damage per turn, removes 1
        self.stun = 0          # 50% chance to skip turn, removes 1
        self.frightened = 0    # -2 ATK when attacking, removes 1
        self.blinded = 0       # +N% miss chance, no crits
        self.immobilized = 0   # Can't evade when attacked, removes 1
        self.off_guard = 0     # 0 defense when attacked, removes 1
        
        # Positive status effects
        self.shields = 0       # Blocks 1 attack, removes 1
    
    def has_negative_effects(self):
        """Check if entity has any negative status effects."""
        return (self.burn > 0 or self.poison > 0 or self.stun > 0 or 
                self.frightened > 0 or self.blinded > 0 or 
                self.immobilized > 0 or self.off_guard > 0)
    
    def clear_negative_effects(self):
        """Remove all negative status effects."""
        self.burn = 0
        self.poison = 0
        self.stun = 0
        self.frightened = 0
        self.blinded = 0
        self.immobilized = 0
        self.off_guard = 0
    
    def apply_status(self, effect_name, amount, entity=None):
        """Apply a status effect with the given amount, checking for immunities."""
        # Check for immunity from accessories
        if entity and hasattr(entity, 'equipped_accessories'):
            for accessory in entity.equipped_accessories():
                if hasattr(accessory, 'blocks_status_effect') and accessory.blocks_status_effect(effect_name):
                    return False  # Blocked by accessory
        
        if hasattr(self, effect_name):
            current_value = getattr(self, effect_name)
            setattr(self, effect_name, current_value + amount)
            return True
        return False
    
    def remove_status(self, effect_name, amount=1):
        """Remove amount from a status effect (minimum 0)."""
        if hasattr(self, effect_name):
            current_value = getattr(self, effect_name)
            setattr(self, effect_name, max(0, current_value - amount))
            return True
        return False
    
    def get_status(self, effect_name):
        """Get the current value of a status effect."""
        if hasattr(self, effect_name):
            return getattr(self, effect_name)
        return 0
    
    def process_turn_start_effects(self, entity):
        """Process status effects that trigger at turn start."""
        damage_taken = 0
        messages = []
        
        # Burn damage
        if self.burn > 0:
            from traits import Trait
            damage = entity.take_damage_with_traits(self.burn, [Trait.FIRE])
            damage_taken += damage
            messages.append(f"{entity.name if hasattr(entity, 'name') else 'Player'} takes {damage} burn damage!")
            self.remove_status('burn', 1)
        
        # Poison damage
        if self.poison > 0:
            from traits import Trait
            damage = entity.take_damage_with_traits(self.poison, [Trait.POISON])
            damage_taken += damage
            messages.append(f"{entity.name if hasattr(entity, 'name') else 'Player'} takes {damage} poison damage!")
            self.remove_status('poison', 1)
        
        return damage_taken, messages
    
    def check_stun_skip_turn(self):
        """Check if entity should skip turn due to stun. Returns True if turn should be skipped."""
        if self.stun > 0:
            import random
            if random.random() < 0.5:  # 50% chance
                self.remove_status('stun', 1)
                return True
        return False
    
    def get_attack_modifier(self):
        """Get attack modifier from status effects."""
        modifier = 0
        if self.frightened > 0:
            modifier -= 2
            self.remove_status('frightened', 1)
        return modifier
    
    def get_miss_chance_increase(self):
        """Get additional miss chance from blinded status."""
        return self.blinded  # N% additional miss chance
    
    def can_crit(self):
        """Check if entity can perform critical hits."""
        return self.blinded == 0
    
    def get_effective_evade(self, base_evade):
        """Get effective evade chance considering immobilized status."""
        if self.immobilized > 0:
            self.remove_status('immobilized', 1)
            return 0.0  # Can't evade when immobilized
        return base_evade
    
    def get_effective_defense(self, base_defense):
        """Get effective defense considering off_guard status."""
        if self.off_guard > 0:
            self.remove_status('off_guard', 1)
            return 0  # No defense when off-guard
        return base_defense
    
    def absorb_attack(self):
        """Check if shields absorb an attack. Returns True if attack was absorbed."""
        if self.shields > 0:
            self.remove_status('shields', 1)
            return True
        return False
    
    def __str__(self):
        """String representation of active status effects."""
        active_effects = []
        
        if self.burn > 0:
            active_effects.append(f"Burn: {self.burn}")
        if self.poison > 0:
            active_effects.append(f"Poison: {self.poison}")
        if self.stun > 0:
            active_effects.append(f"Stun: {self.stun}")
        if self.frightened > 0:
            active_effects.append(f"Frightened: {self.frightened}")
        if self.blinded > 0:
            active_effects.append(f"Blinded: {self.blinded}")
        if self.immobilized > 0:
            active_effects.append(f"Immobilized: {self.immobilized}")
        if self.off_guard > 0:
            active_effects.append(f"Off-Guard: {self.off_guard}")
        if self.shields > 0:
            active_effects.append(f"Shields: {self.shields}")
        
        return ", ".join(active_effects) if active_effects else "None"