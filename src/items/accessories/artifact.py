"""
Base Artifact class for artifact accessories.
"""
from .accessory import Accessory


class Artifact(Accessory):
    """Base class for artifacts"""
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0, fov_bonus=0, health_aspect_bonus=0,
              attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
              evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
              attack_traits=None, weaknesses=None, resistances=None,
               description="An enchanted card", is_cleanup=False):
      super().__init__(x, y, name, 'a', attack_bonus, defense_bonus, description, fov_bonus, health_aspect_bonus,
                      attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus,
                      evade_bonus, crit_bonus, crit_multiplier_bonus, attack_traits, weaknesses, resistances,  is_cleanup)