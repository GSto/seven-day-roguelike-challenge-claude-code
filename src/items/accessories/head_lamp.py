"""
HeadLamp - Hat that increases FOV.
"""
from .hat import Hat


class HeadLamp(Hat):
    """Hat that increases FOV"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "HeadLamp", attack_bonus=0, defense_bonus=1, fov_bonus=5, description="lamp on your head")