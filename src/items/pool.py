"""
Item pool system for managing item spawning with rarity-based drop rates and uniqueness constraints.
"""

import random
from dataclasses import dataclass, field
from typing import Type, List, Dict, Set, Optional, Tuple
        # Import all item classes
from .consumables import (
    HealthPotion, Beef, Chicken, SalmonOfKnowledge, D6, MagicMushroom, Carrot,
    Antidote, ShellPotion, MezzoForte, Elixir,
    SwordsToPlowshares, Transmutation,
    PowerCatalyst, DefenseCatalyst, JewelerCatalyst, ReapersCatalyst, 
    ShadowsCatalyst, BaronCatalyst, WardenCatalyst, FireResistanceCatalyst,
    IceResistanceCatalyst, HolyResistanceCatalyst, DarkResistanceCatalyst,
    BaronsBoon, JewelersBoon, MinersBoon, ClericsBoon, JokersBoon, ReapersBoon,
    FireBoon, IceBoon, HolyBoon, DarkBoon, MayhemsBoon
)
from .pickups import Snackie
from .weapons import (
    Dagger, Sword, Shield, Katana, Axe, MorningStar, ClericsStaff, Gauntlets,
    MateriaStaff, Uchigatana, Pickaxe, SnakesFang, Rapier, AcidDagger, BigStick,
    Longsword, WarHammer, WarScythe, TowerShield, ClairObscur, FeuGlace,
    RiversOfBlood, DemonSlayer, BackhandBlade, HolyAvenger
)
from .armor import (
    LeatherArmor, SafetyVest, Cloak, SpikedArmor, GamblersVest, MinimalSuit,
    ChainMail, NightCloak, CoatedPlate, AntiAngelTechnology, SpikedCuirass,
    UtilityBelt, SOSArmor, PlateArmor, ShadowCloak, DragonScale, StoneArmor, TurtleShell, AntiDevilTechnology
)
from .accessories import (
    PowerRing, ProtectionRing, GreaterPowerRing, GreaterProtectionRing,
    BaronsCrown, JewelersCap, Rosary, HeadLamp, ShadowRing, RingOfPrecision,
    BrutalityAmulet, AssassinsMask, GravePact, PunishTheWeak,
    StrikeBonus, SlashBonus, ElementalMayhem, GodsEye, SavingThrow, Anaglyph,
    MallNinja, RighteousFury, SongOfIceAndFire, AceOfHearts, AceOfClubs,
    AceOfDiamonds, AceOfSpades, Joker, HealingDodge, ProtectiveLevel,
    PsychicsTurban, VampiresPendant, WardensTome
)


# Rarity weight constants
RARITY_COMMON = 1.0
RARITY_UNCOMMON = 0.6
RARITY_RARE = 0.3

@dataclass
class ItemSpec:
    """Specification for an item type including spawn rules."""
    item_class: Type           # The item class to instantiate
    item_type: str             # 'weapon', 'armor', 'accessory', 'consumable'
    min_level: int            # Earliest level this item can appear
    max_level: Optional[int]  # Latest level (None = no limit)
    rarity: float            # Base spawn weight (higher = more common)
    unique_per_floor: bool   # True for weapons/armor
    unique_per_game: bool    # True for accessories
    tags: List[str] = field(default_factory=list)  # Optional tags for special handling


class ItemPool:
    """Manages item spawning with rarity-based drop rates and uniqueness tracking."""
    
    def __init__(self):
        self.weapon_specs: List[ItemSpec] = []
        self.armor_specs: List[ItemSpec] = []
        self.accessory_specs: List[ItemSpec] = []
        self.consumable_specs: List[ItemSpec] = []
        self.pickup_specs: List[ItemSpec] = []  # Separate category for pickups
        
        # Tracking for uniqueness constraints
        self.floor_spawned_weapons: Dict[int, Set[Type]] = {}  # Per-floor tracking
        self.floor_spawned_armor: Dict[int, Set[Type]] = {}    # Per-floor tracking
        self.game_spawned_accessories: Set[Type] = set()       # Global tracking
        
        # Cache for performance
        self._level_pools: Dict[str, List[Tuple[ItemSpec, float]]] = {}
        
        # Initialize item specifications
        self._initialize_item_specs()
    
    def _initialize_item_specs(self):
        """Initialize all item specifications with difficulty ratings and spawn rules."""
        
        # WEAPONS
        self.weapon_specs = [
            # Early game weapons (levels 1-4)
            ItemSpec(Dagger, 'weapon', 1, 4, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(Sword, 'weapon', 1, 5, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(Shield, 'weapon', 1, 6, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(Katana, 'weapon', 1, 5, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            
            # Mid game weapons (levels 3-7)
            ItemSpec(Axe, 'weapon', 3, 7, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(MorningStar, 'weapon', 3, 8, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(ClericsStaff, 'weapon', 2, 7, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(Gauntlets, 'weapon', 3, 8, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(MateriaStaff, 'weapon', 3, 8, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(Uchigatana, 'weapon', 4, 8, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(Pickaxe, 'weapon', 2, 7, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(SnakesFang, 'weapon', 3, 7, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(Rapier, 'weapon', 3, 8, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(AcidDagger, 'weapon', 3, 7, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(BigStick, 'weapon', 2, 6, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            
            # Late game weapons (levels 6-9)
            ItemSpec(Longsword, 'weapon', 6, 9, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(TowerShield, 'weapon', 6, None, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(WarHammer, 'weapon', 7, None, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(WarScythe, 'weapon', 7, None, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(HolyAvenger, 'weapon', 7, None, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(BackhandBlade, 'weapon', 7, None, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(ClairObscur, 'weapon', 8, None, RARITY_RARE, unique_per_floor=True, unique_per_game=False),
            ItemSpec(FeuGlace, 'weapon', 8, None, RARITY_RARE, unique_per_floor=True, unique_per_game=False),
            ItemSpec(RiversOfBlood, 'weapon', 7, None, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            
            # End game weapons (levels 9-10)
            ItemSpec(DemonSlayer, 'weapon', 10, 10, RARITY_COMMON, unique_per_floor=True, unique_per_game=False, tags=['boss_weapon']),
        ]
        
        # ARMOR
        self.armor_specs = [
            # Early game armor (levels 1-4)
            ItemSpec(LeatherArmor, 'armor', 1, 4, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(SafetyVest, 'armor', 1, 5, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(Cloak, 'armor', 1, 5, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            
            # Default armor (all levels)
            ItemSpec(SpikedArmor, 'armor', 1, None, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(GamblersVest, 'armor', 1, None, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(MinimalSuit, 'armor', 1, None, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            
            # Mid game armor (levels 3-7)
            ItemSpec(ChainMail, 'armor', 3, 7, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(NightCloak, 'armor', 3, 8, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(CoatedPlate, 'armor', 4, 8, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(AntiAngelTechnology, 'armor', 4, 8, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(AntiDevilTechnology, 'armor', 4, 8, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(TurtleShell, 'armor', 4, 8, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(StoneArmor, 'armor', 4, 8, RARITY_COMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(SpikedCuirass, 'armor', 3, 8, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(UtilityBelt, 'armor', 3, None, RARITY_RARE, unique_per_floor=True, unique_per_game=False),
            ItemSpec(SOSArmor, 'armor', 4, 8, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            
            # Late game armor (levels 6-10)
            ItemSpec(PlateArmor, 'armor', 6, None, RARITY_UNCOMMON, unique_per_floor=True, unique_per_game=False),
            ItemSpec(ShadowCloak, 'armor', 6, None, RARITY_RARE, unique_per_floor=True, unique_per_game=False),
            ItemSpec(DragonScale, 'armor', 9, None, RARITY_RARE, unique_per_floor=True, unique_per_game=False),
        ]
        
        # ACCESSORIES (unique per game)
        self.accessory_specs = [
            # Basic rings
            ItemSpec(PowerRing, 'accessory', 1, 7, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(ProtectionRing, 'accessory', 1, 7, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(GreaterPowerRing, 'accessory', 4, None, RARITY_RARE, unique_per_floor=False, unique_per_game=True),
            ItemSpec(GreaterProtectionRing, 'accessory', 4, None, RARITY_RARE, unique_per_floor=False, unique_per_game=True),
            
            # Special accessories (available from mid-game)
            ItemSpec(BaronsCrown, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(JewelersCap, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(Rosary, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(HeadLamp, 'accessory', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(ShadowRing, 'accessory', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(RingOfPrecision, 'accessory', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(BrutalityAmulet, 'accessory', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(AssassinsMask, 'accessory', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(GravePact, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(PunishTheWeak, 'accessory', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(StrikeBonus, 'accessory', 3, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(SlashBonus, 'accessory', 3, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(ElementalMayhem, 'accessory', 1, None, RARITY_RARE, unique_per_floor=False, unique_per_game=True),
            ItemSpec(GodsEye, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True, tags=['legendary']),
            ItemSpec(SavingThrow, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(Anaglyph, 'accessory', 1, None, RARITY_RARE, unique_per_floor=False, unique_per_game=True),
            ItemSpec(MallNinja, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(RighteousFury, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(SongOfIceAndFire, 'accessory', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=True),
            
            # Cards (mid to late game)
            ItemSpec(AceOfHearts, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True, tags=['card']),
            ItemSpec(AceOfClubs, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True, tags=['card']),
            ItemSpec(AceOfDiamonds, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True, tags=['card']),
            ItemSpec(AceOfSpades, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True, tags=['card']),
            ItemSpec(Joker, 'accessory', 1, None, RARITY_RARE, unique_per_floor=False, unique_per_game=True, tags=['card']),
            
            # Additional accessories
            ItemSpec(HealingDodge, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(ProtectiveLevel, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(PsychicsTurban, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True),
            ItemSpec(VampiresPendant, 'accessory', 1, None, RARITY_RARE, unique_per_floor=False, unique_per_game=True),
            ItemSpec(WardensTome, 'accessory', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=True),
        ]
        
        # PICKUPS (instant effect items)
        self.pickup_specs = [
            ItemSpec(Snackie, 'pickup', 1, None, RARITY_COMMON * 2.0, unique_per_floor=False, unique_per_game=False),
        ]
        
        # CONSUMABLES (no uniqueness constraints)
        self.consumable_specs = [
            # Basic consumables (all levels)
            ItemSpec(HealthPotion, 'consumable', 1, None, RARITY_COMMON * 2.5, unique_per_floor=False, unique_per_game=False),
            ItemSpec(Beef, 'consumable', 1, None, RARITY_RARE, unique_per_floor=False, unique_per_game=False),
            ItemSpec(Chicken, 'consumable', 1, None, RARITY_RARE, unique_per_floor=False, unique_per_game=False),
            ItemSpec(SalmonOfKnowledge, 'consumable', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=False),
            ItemSpec(D6, 'consumable', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=False),
            ItemSpec(MagicMushroom, 'consumable', 1, None, RARITY_RARE, unique_per_floor=False, unique_per_game=False),
            ItemSpec(Carrot, 'consumable', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=False),
            
            # Status consumables
            ItemSpec(Antidote, 'consumable', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=False),
            ItemSpec(ShellPotion, 'consumable', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=False),
            ItemSpec(MezzoForte, 'consumable', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=False),
            
            # Special consumables
            ItemSpec(SwordsToPlowshares, 'consumable', 3, None, RARITY_RARE, unique_per_floor=False, unique_per_game=False),
            ItemSpec(Transmutation, 'consumable', 3, None, RARITY_RARE, unique_per_floor=False, unique_per_game=False),
            
            # Catalysts (mid-game+)
            ItemSpec(PowerCatalyst, 'consumable', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=False, tags=['catalyst']),
            ItemSpec(DefenseCatalyst, 'consumable', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=False, tags=['catalyst']),
            ItemSpec(JewelerCatalyst, 'consumable', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=False, tags=['catalyst']),
            ItemSpec(ReapersCatalyst, 'consumable', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=False, tags=['catalyst']),
            ItemSpec(ShadowsCatalyst, 'consumable', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=False, tags=['catalyst']),
            ItemSpec(BaronCatalyst, 'consumable', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=False, tags=['catalyst']),
            ItemSpec(WardenCatalyst, 'consumable', 1, None, RARITY_UNCOMMON, unique_per_floor=False, unique_per_game=False, tags=['catalyst']),
            ItemSpec(FireResistanceCatalyst, 'consumable', 1, None, RARITY_RARE, unique_per_floor=False, unique_per_game=False, tags=['catalyst', 'elemental']),
            ItemSpec(IceResistanceCatalyst, 'consumable', 1, None, RARITY_RARE, unique_per_floor=False, unique_per_game=False, tags=['catalyst', 'elemental']),
            ItemSpec(HolyResistanceCatalyst, 'consumable', 1, None, RARITY_RARE, unique_per_floor=False, unique_per_game=False, tags=['catalyst', 'elemental']),
            ItemSpec(DarkResistanceCatalyst, 'consumable', 1, None, RARITY_RARE, unique_per_floor=False, unique_per_game=False, tags=['catalyst', 'elemental']),
            
            # Boons 
            ItemSpec(BaronsBoon, 'consumable', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=False, tags=['boon']),
            ItemSpec(JewelersBoon, 'consumable', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=False, tags=['boon']),
            ItemSpec(MinersBoon, 'consumable', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=False, tags=['boon']),
            ItemSpec(ClericsBoon, 'consumable', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=False, tags=['boon']),
            ItemSpec(JokersBoon, 'consumable', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=False, tags=['boon']),
            ItemSpec(ReapersBoon, 'consumable', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=False, tags=['boon']),
            ItemSpec(FireBoon, 'consumable', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=False, tags=['boon', 'elemental']),
            ItemSpec(IceBoon, 'consumable', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=False, tags=['boon', 'elemental']),
            ItemSpec(HolyBoon, 'consumable', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=False, tags=['boon', 'elemental']),
            ItemSpec(DarkBoon, 'consumable', 1, None, RARITY_COMMON, unique_per_floor=False, unique_per_game=False, tags=['boon', 'elemental']),
            ItemSpec(MayhemsBoon, 'consumable', 2, None, RARITY_RARE, unique_per_floor=False, unique_per_game=False, tags=['boon']),
            
            # End game consumable
            ItemSpec(Elixir, 'consumable', 8, None, RARITY_RARE, unique_per_floor=False, unique_per_game=False),
        ]
    
    def start_new_floor(self, level: int):
        """Reset per-floor tracking for weapons and armor."""
        self.floor_spawned_weapons[level] = set()
        self.floor_spawned_armor[level] = set()
    
    def is_item_available(self, item_spec: ItemSpec, level: int) -> bool:
        """
        Check if an item can spawn based on uniqueness constraints.
        
        - Weapons/Armor: Check if already spawned on current floor
        - Accessories: Check if already spawned in the game
        - Consumables: Always available
        """
        if item_spec.unique_per_game:
            # Check global uniqueness for accessories
            return item_spec.item_class not in self.game_spawned_accessories
        elif item_spec.unique_per_floor:
            # Check per-floor uniqueness for weapons/armor
            if item_spec.item_type == 'weapon':
                floor_weapons = self.floor_spawned_weapons.get(level, set())
                return item_spec.item_class not in floor_weapons
            elif item_spec.item_type == 'armor':
                floor_armor = self.floor_spawned_armor.get(level, set())
                return item_spec.item_class not in floor_armor
        
        # No uniqueness constraint (consumables)
        return True
    
    def calculate_spawn_weight(self, item_spec: ItemSpec, level: int) -> float:
        """
        Calculate spawn weight considering:
        - Base rarity
        - Level range constraints
        - Level transition smoothing (phase in/out gradually)
        - Uniqueness availability
        """
        # Check if item is available
        if not self.is_item_available(item_spec, level):
            return 0.0
        
        # Check level range
        if level < item_spec.min_level:
            return 0.0
        if item_spec.max_level is not None and level > item_spec.max_level:
            return 0.0
        
        # Special case: Level 10 boss items
        if level == 10 and 'boss_weapon' in item_spec.tags:
            return 100.0  # Extremely high weight for DemonSlayer on level 10
        
        # Base weight from rarity only
        weight = item_spec.rarity
        
        # Level transition smoothing
        # Phase in: gradually increase weight as we get further from min_level
        if item_spec.min_level > 1:
            levels_since_min = level - item_spec.min_level
            phase_in_factor = min(1.0, levels_since_min / 2.0)  # Full weight after 2 levels
            weight *= phase_in_factor
        
        # Phase out: gradually decrease weight as we approach max_level
        if item_spec.max_level is not None:
            levels_until_max = item_spec.max_level - level
            phase_out_factor = min(1.0, (levels_until_max + 1) / 2.0)  # Start phasing out 2 levels before max
            weight *= phase_out_factor
        
        return weight
    
    
    def get_item_type_weights(self, level: int) -> Dict[str, float]:
        """
        Return weights for item type selection based on level.
        Pickups are 5-10% of the pool at all levels.
        """
        if level <= 2:
            # Early game: more pickups (10%) for survivability
            return {'pickup': 0.10, 'consumable': 0.20, 'weapon': 0.28, 'armor': 0.23, 'accessory': 0.19}
        elif level <= 5:
            # Mid game: standard pickup rate (7%)
            return {'pickup': 0.07, 'consumable': 0.31, 'weapon': 0.24, 'armor': 0.14, 'accessory': 0.24}
        elif level <= 8:
            # Late game: slightly fewer pickups (6%)
            return {'pickup': 0.06, 'consumable': 0.32, 'weapon': 0.24, 'armor': 0.14, 'accessory': 0.24}
        else:
            # End game: minimum pickups (5%)
            return {'pickup': 0.05, 'consumable': 0.33, 'weapon': 0.24, 'armor': 0.14, 'accessory': 0.24}
    
    def _get_weighted_pool(self, specs: List[ItemSpec], level: int) -> List[Tuple[ItemSpec, float]]:
        """Get a list of (ItemSpec, weight) tuples for weighted random selection."""
        # Don't cache pools since uniqueness state changes during gameplay
        weighted_pool = []
        for spec in specs:
            weight = self.calculate_spawn_weight(spec, level)
            if weight > 0:
                weighted_pool.append((spec, weight))
        
        return weighted_pool
    
    def _select_item_from_pool(self, weighted_pool: List[Tuple[ItemSpec, float]]) -> Optional[ItemSpec]:
        """Select an item from a weighted pool using weighted random selection."""
        if not weighted_pool:
            return None
        
        total_weight = sum(weight for _, weight in weighted_pool)
        if total_weight <= 0:
            return None
        
        r = random.random() * total_weight
        cumulative = 0
        
        for spec, weight in weighted_pool:
            cumulative += weight
            if r <= cumulative:
                return spec
        
        # Fallback (should not reach here)
        return weighted_pool[-1][0]
    
    def create_item_for_level(self, level: int, x: int, y: int, 
                            item_type: Optional[str] = None,
                            force_type: bool = False):
        """
        Create an appropriate item for the given level.
        
        Args:
            level: Current dungeon level
            x, y: Position for the item
            item_type: Optional specific type ('weapon', 'armor', 'accessory', 'consumable')
            force_type: If True, must spawn the specified type (no fallback)
        
        Returns:
            An item instance appropriate for the level
        """
        # If no specific type requested, choose based on level weights
        if item_type is None:
            type_weights = self.get_item_type_weights(level)
            item_types = list(type_weights.keys())
            weights = list(type_weights.values())
            item_type = random.choices(item_types, weights=weights)[0]
        
        # Get the appropriate spec list
        if item_type == 'weapon':
            specs = self.weapon_specs
        elif item_type == 'armor':
            specs = self.armor_specs
        elif item_type == 'accessory':
            specs = self.accessory_specs
        elif item_type == 'consumable':
            specs = self.consumable_specs
        elif item_type == 'pickup':
            specs = self.pickup_specs
        else:
            # Invalid type
            if force_type:
                raise ValueError(f"Invalid item type: {item_type}")
            # Fallback to consumable
            specs = self.consumable_specs
            item_type = 'consumable'
        
        # Get weighted pool and select item
        weighted_pool = self._get_weighted_pool(specs, level)
        selected_spec = self._select_item_from_pool(weighted_pool)
        
        # If no item could be selected and not forcing type, try other types
        if selected_spec is None and not force_type:
            # Try other item types
            all_types = ['consumable', 'pickup', 'weapon', 'armor', 'accessory']
            all_types.remove(item_type)  # Remove the type we already tried
            
            for fallback_type in all_types:
                if fallback_type == 'weapon':
                    specs = self.weapon_specs
                elif fallback_type == 'armor':
                    specs = self.armor_specs
                elif fallback_type == 'accessory':
                    specs = self.accessory_specs
                elif fallback_type == 'pickup':
                    specs = self.pickup_specs
                else:
                    specs = self.consumable_specs
                
                weighted_pool = self._get_weighted_pool(specs, level)
                selected_spec = self._select_item_from_pool(weighted_pool)
                
                if selected_spec is not None:
                    item_type = fallback_type
                    break
        
        # If still no item, use emergency fallback (HealthPotion)
        if selected_spec is None:
            from .consumables import HealthPotion
            return HealthPotion(x, y)
        
        # Create the item instance
        item = selected_spec.item_class(x, y)
        
        # Track spawned items for uniqueness
        if selected_spec.unique_per_game:
            self.game_spawned_accessories.add(selected_spec.item_class)
        elif selected_spec.unique_per_floor:
            if item_type == 'weapon':
                if level not in self.floor_spawned_weapons:
                    self.floor_spawned_weapons[level] = set()
                self.floor_spawned_weapons[level].add(selected_spec.item_class)
            elif item_type == 'armor':
                if level not in self.floor_spawned_armor:
                    self.floor_spawned_armor[level] = set()
                self.floor_spawned_armor[level].add(selected_spec.item_class)
        
        # Apply enchantments if applicable
        self.apply_enchantment_chance(item, level)
        
        return item
    
    def apply_enchantment_chance(self, item, level: int):
        """Apply enchantment based on level-appropriate chance."""
        from enchantments.utils import get_random_enchantment, get_random_armor_enchantment
        
        # Check if item can be enchanted
        if not hasattr(item, 'add_enchantment'):
            return
        
        # Check if item should not have initial enchantments
        if getattr(item, 'no_initial_enchantments', False):
            return
        
        # Calculate enchantment chance based on level
        chance = min(0.5, 0.1 + (level * 0.04))  # 10% at level 1, up to 50% at level 10
        
        if random.random() < chance:
            # Apply appropriate enchantment
            if hasattr(item, 'equipment_slot'):
                if item.equipment_slot == 'weapon':
                    enchantment = get_random_enchantment()
                    item.add_enchantment(enchantment)
                elif item.equipment_slot == 'armor':
                    enchantment = get_random_armor_enchantment()
                    item.add_enchantment(enchantment)
    
    def get_save_data(self) -> dict:
        """Get data for saving the pool state."""
        return {
            'floor_spawned_weapons': {
                level: [cls.__name__ for cls in classes]
                for level, classes in self.floor_spawned_weapons.items()
            },
            'floor_spawned_armor': {
                level: [cls.__name__ for cls in classes]
                for level, classes in self.floor_spawned_armor.items()
            },
            'game_spawned_accessories': [cls.__name__ for cls in self.game_spawned_accessories]
        }
    
    def load_save_data(self, data: dict):
        """Load pool state from save data."""
        # Build a map of class names to classes
        class_map = {}
        for spec in self.weapon_specs + self.armor_specs + self.accessory_specs:
            class_map[spec.item_class.__name__] = spec.item_class
        
        # Restore floor spawned weapons
        self.floor_spawned_weapons = {}
        for level, class_names in data.get('floor_spawned_weapons', {}).items():
            self.floor_spawned_weapons[int(level)] = {
                class_map[name] for name in class_names if name in class_map
            }
        
        # Restore floor spawned armor
        self.floor_spawned_armor = {}
        for level, class_names in data.get('floor_spawned_armor', {}).items():
            self.floor_spawned_armor[int(level)] = {
                class_map[name] for name in class_names if name in class_map
            }
        
        # Restore game spawned accessories
        self.game_spawned_accessories = {
            class_map[name] for name in data.get('game_spawned_accessories', [])
            if name in class_map
        }


# Global pool instance
item_pool = ItemPool()