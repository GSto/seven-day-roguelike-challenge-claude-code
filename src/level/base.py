"""
Base class for safe zone areas between dungeon floors.
"""

import numpy as np
import tcod
from constants import (
    MAP_WIDTH, MAP_HEIGHT,
    TILE_WALL, TILE_FLOOR, TILE_STAIRS_DOWN, TILE_STAIRS_UP,
    COLOR_DARK_WALL, COLOR_DARK_GROUND, COLOR_LIGHT_WALL, COLOR_LIGHT_GROUND
)
from shop import Shop


class Base:
    """Represents a safe base area between dungeon levels."""
    
    # Fixed dimensions for all bases
    ROOM_WIDTH = 18
    ROOM_HEIGHT = 11
    
    def __init__(self, base_number):
        """Initialize a base level."""
        self.base_number = base_number
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        
        # Initialize the map with walls
        self.tiles = np.full((MAP_WIDTH, MAP_HEIGHT), TILE_WALL, dtype=int)
        self.explored = np.full((MAP_WIDTH, MAP_HEIGHT), False, dtype=bool)
        self.fov = np.full((MAP_WIDTH, MAP_HEIGHT), False, dtype=bool)
        
        # No monsters or random items in bases
        self.monsters = []
        self.items = []
        
        # Generate the fixed base layout
        self.generate_base_layout()
        
        # Create shop for the NEXT floor's items
        self.create_base_shop()
        
        # Set up FOV map
        self.fov_map = tcod.map.Map(MAP_WIDTH, MAP_HEIGHT)
        self.update_fov_map()
    
    def generate_base_layout(self):
        """Create fixed rectangular room with walls."""
        # Calculate room position (centered in map)
        room_x = (MAP_WIDTH - self.ROOM_WIDTH) // 2
        room_y = (MAP_HEIGHT - self.ROOM_HEIGHT) // 2
        
        # Store room bounds for reference
        self.room_x1 = room_x
        self.room_y1 = room_y
        self.room_x2 = room_x + self.ROOM_WIDTH - 1
        self.room_y2 = room_y + self.ROOM_HEIGHT - 1
        
        # Carve out the room (fill with floor tiles)
        for x in range(room_x + 1, room_x + self.ROOM_WIDTH - 1):
            for y in range(room_y + 1, room_y + self.ROOM_HEIGHT - 1):
                self.tiles[x, y] = TILE_FLOOR
        
        # Place entry stairs (bottom center, offset from wall)
        entry_x = room_x + self.ROOM_WIDTH // 2
        entry_y = room_y + self.ROOM_HEIGHT - 3  # 2 tiles from bottom wall
        self.tiles[entry_x, entry_y] = TILE_STAIRS_UP
        self.stairs_up_pos = (entry_x, entry_y)
        
        # Place exit stairs (top center, offset from wall)
        exit_x = room_x + self.ROOM_WIDTH // 2
        exit_y = room_y + 2  # 2 tiles from top wall
        self.tiles[exit_x, exit_y] = TILE_STAIRS_DOWN
        self.stairs_down_pos = (exit_x, exit_y)
    
    def create_base_shop(self):
        """Generate shop with next floor's items."""
        # Shop position (top-right corner, offset from walls)
        shop_x = self.room_x2 - 3  # 3 tiles from right wall
        shop_y = self.room_y1 + 2  # 2 tiles from top wall
        
        # Create shop for the NEXT floor (base N has floor N+1 items)
        next_floor_level = self.base_number + 1
        self.shop = Shop(floor_level=next_floor_level)
        self.shop.x = shop_x
        self.shop.y = shop_y
    
    def is_safe_zone(self):
        """Always returns True - no combat allowed in bases."""
        return True
    
    def is_walkable(self, x, y):
        """Check if a tile is walkable."""
        if x < 0 or x >= MAP_WIDTH or y < 0 or y >= MAP_HEIGHT:
            return False
        if self.tiles[x, y] == TILE_WALL:
            return False
        # No monsters to check in bases (safe zone)
        return True
    
    def is_stairs_down(self, x, y):
        """Check if position has stairs down."""
        return self.tiles[x, y] == TILE_STAIRS_DOWN
    
    def is_stairs_up(self, x, y):
        """Check if position has stairs up."""
        return self.tiles[x, y] == TILE_STAIRS_UP
    
    def is_shop_at(self, x, y):
        """Check if there's a shop at the given position."""
        if self.shop:
            return self.shop.x == x and self.shop.y == y
        return False
    
    def get_stairs_up_position(self):
        """Get the position of stairs up."""
        return self.stairs_up_pos
    
    def get_stairs_down_position(self):
        """Get the position of stairs down."""
        return self.stairs_down_pos
    
    def update_fov_map(self):
        """Update the FOV map based on current tiles."""
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                is_transparent = self.tiles[x, y] != TILE_WALL
                self.fov_map.transparent[y, x] = is_transparent
                self.fov_map.walkable[y, x] = is_transparent
    
    def update_fov(self, player_x, player_y, fov_radius):
        """Update field of view from player position."""
        if player_x < 0 or player_x >= MAP_WIDTH:
            return
        if player_y < 0 or player_y >= MAP_HEIGHT:
            return
            
        # Calculate FOV using the FOV map
        self.fov[:] = False
        self.fov[player_x, player_y] = True
        
        # Compute FOV using tcod's algorithm
        self.fov[:] = tcod.map.compute_fov(
            transparency=self.fov_map.transparent,
            pov=(player_y, player_x),
            radius=fov_radius,
            light_walls=True,
            algorithm=tcod.FOV_BASIC
        ).T
        
        # Mark visible areas as explored
        self.explored |= self.fov
    
    def render(self, console):
        """Render the base to the console."""
        # Render terrain
        for x in range(min(MAP_WIDTH, console.width)):
            for y in range(min(MAP_HEIGHT, console.height)):
                if x < MAP_WIDTH and y < MAP_HEIGHT:
                    visible = self.fov[x, y]
                    explored = self.explored[x, y]
                    
                    if visible:
                        if self.tiles[x, y] == TILE_WALL:
                            console.print(x, y, '#', fg=COLOR_LIGHT_WALL)
                        elif self.tiles[x, y] == TILE_FLOOR:
                            console.print(x, y, '.', fg=COLOR_LIGHT_GROUND)
                        elif self.tiles[x, y] == TILE_STAIRS_DOWN:
                            console.print(x, y, '>', fg=COLOR_LIGHT_GROUND)
                        elif self.tiles[x, y] == TILE_STAIRS_UP:
                            console.print(x, y, '<', fg=COLOR_LIGHT_GROUND)
                    elif explored:
                        if self.tiles[x, y] == TILE_WALL:
                            console.print(x, y, '#', fg=COLOR_DARK_WALL)
                        elif self.tiles[x, y] == TILE_FLOOR:
                            console.print(x, y, '.', fg=COLOR_DARK_GROUND)
                        elif self.tiles[x, y] == TILE_STAIRS_DOWN:
                            console.print(x, y, '>', fg=COLOR_DARK_GROUND)
                        elif self.tiles[x, y] == TILE_STAIRS_UP:
                            console.print(x, y, '<', fg=COLOR_DARK_GROUND)
        
        # Render shop symbol if present
        if self.shop:
            self.shop.render(console, self.fov)
    
    # Stub methods to maintain compatibility with Level interface
    def is_position_occupied(self, x, y):
        """No monsters in bases - always returns False."""
        return False
    
    def get_monster_at(self, x, y):
        """No monsters in bases - always returns None."""
        return None
    
    def get_item_at(self, x, y):
        """No random items in bases - always returns None."""
        return None
    
    def remove_item(self, item):
        """No items to remove in bases."""
        pass
    
    def add_item_drop(self, x, y, item):
        """Items cannot be dropped in bases."""
        pass