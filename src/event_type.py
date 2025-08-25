from enum import Enum

class EventType(Enum):
    PLAYER_HEAL = "player_heal"
    PLAYER_CONSUME_ITEM = "player_consume_item"
    PLAYER_ATTACK_MONSTER = "player_attack_monster"
    MONSTER_ATTACK_PLAYER = "monster_attack_player"
    MONSTER_DEATH = "monster_death"
    LEVEL_UP = "level_up"
    FLOOR_CHANGE = "floor_change"
    SUCCESSFUL_DODGE = "successful_dodge"
    CRITICAL_HIT = "critical_hit"
    MISS = "miss"
    WEAKNESS_HIT = "weakness_hit"
    RESISTANCE_HIT = "resistance_hit"