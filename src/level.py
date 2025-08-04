"""
Level generation and management.
"""

import random
import numpy as np
import tcod

from constants import (
    MAP_WIDTH, MAP_HEIGHT, FOV_RADIUS,
    TILE_WALL, TILE_FLOOR, TILE_STAIRS_DOWN, TILE_STAIRS_UP,
    COLOR_DARK_WALL, COLOR_DARK_GROUND, COLOR_LIGHT_WALL, COLOR_LIGHT_GROUND
)


class Room:
    """Represents a room in the dungeon."""
    
    def __init__(self, x, y, width, height):
        """Initialize the room."""
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height
    
    def center(self):
        """Get the center coordinates of the room."""
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y
    
    def intersect(self, other):
        """Check if this room intersects with another room."""
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


class Level:
    """Represents a dungeon level."""
    
    def __init__(self, level_number):
        """Initialize the level."""
        self.level_number = level_number
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        
        # Initialize the map with walls
        self.tiles = np.full((MAP_WIDTH, MAP_HEIGHT), TILE_WALL, dtype=int)
        self.explored = np.full((MAP_WIDTH, MAP_HEIGHT), False, dtype=bool)
        self.fov = np.full((MAP_WIDTH, MAP_HEIGHT), False, dtype=bool)
        
        # Generate the level
        self.rooms = []
        self.generate_level()
        
        # Set up FOV map - note tcod uses (width, height) order
        self.fov_map = tcod.map.Map(MAP_WIDTH, MAP_HEIGHT)
        self.update_fov_map()
    
    def generate_level(self):
        """Generate the dungeon level."""
        # Room generation parameters
        max_rooms = 30
        room_min_size = 6
        room_max_size = 10
        
        for r in range(max_rooms):
            # Random width and height
            w = random.randint(room_min_size, room_max_size)
            h = random.randint(room_min_size, room_max_size)
            
            # Random position without going out of bounds
            x = random.randint(0, MAP_WIDTH - w - 1)
            y = random.randint(0, MAP_HEIGHT - h - 1)
            
            # Create the room
            new_room = Room(x, y, w, h)
            
            # Check if room intersects with existing rooms
            failed = False
            for other_room in self.rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break
            
            if not failed:
                # Create the room
                self.create_room(new_room)
                
                # Connect to previous room with a tunnel
                if len(self.rooms) > 0:
                    new_x, new_y = new_room.center()
                    prev_x, prev_y = self.rooms[-1].center()
                    
                    # 50% chance to go horizontal first, then vertical
                    if random.randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                
                self.rooms.append(new_room)
        
        # Place stairs
        self.place_stairs()
    
    def create_room(self, room):
        """Create a room by setting tiles to floor."""
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x, y] = TILE_FLOOR
    
    def create_h_tunnel(self, x1, x2, y):
        """Create a horizontal tunnel."""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x, y] = TILE_FLOOR
    
    def create_v_tunnel(self, y1, y2, x):
        """Create a vertical tunnel."""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x, y] = TILE_FLOOR
    
    def place_stairs(self):
        """Place stairs in the level."""
        if len(self.rooms) < 2:
            return
        
        # Place stairs up in the first room
        first_room = self.rooms[0]
        stairs_up_x, stairs_up_y = first_room.center()
        self.tiles[stairs_up_x, stairs_up_y] = TILE_STAIRS_UP
        self.stairs_up_pos = (stairs_up_x, stairs_up_y)
        
        # Place stairs down in the last room (unless this is the final level)
        if self.level_number < 10:  # Max 10 levels
            last_room = self.rooms[-1]
            stairs_down_x, stairs_down_y = last_room.center()
            self.tiles[stairs_down_x, stairs_down_y] = TILE_STAIRS_DOWN
            self.stairs_down_pos = (stairs_down_x, stairs_down_y)
        else:
            self.stairs_down_pos = None
    
    def is_walkable(self, x, y):
        """Check if a tile is walkable."""
        if x < 0 or x >= MAP_WIDTH or y < 0 or y >= MAP_HEIGHT:
            return False
        return self.tiles[x, y] != TILE_WALL
    
    def is_stairs_down(self, x, y):
        """Check if position has stairs down."""
        return self.tiles[x, y] == TILE_STAIRS_DOWN
    
    def is_stairs_up(self, x, y):
        """Check if position has stairs up."""
        return self.tiles[x, y] == TILE_STAIRS_UP
    
    def get_stairs_up_position(self):
        """Get the position of stairs up."""
        return self.stairs_up_pos
    
    def get_stairs_down_position(self):
        """Get the position of stairs down."""
        return self.stairs_down_pos if self.stairs_down_pos else (0, 0)
    
    def update_fov_map(self):
        """Update the FOV map based on current tiles."""
        # tcod.map.Map uses (y, x) indexing, opposite of our tiles array
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                is_transparent = self.tiles[x, y] != TILE_WALL
                self.fov_map.transparent[y, x] = is_transparent
                self.fov_map.walkable[y, x] = is_transparent
    
    def update_fov(self, player_x, player_y):
        """Update field of view from player position."""
        # Ensure player is within bounds
        if (0 <= player_x < MAP_WIDTH and 0 <= player_y < MAP_HEIGHT):
            # tcod.map.Map.compute_fov expects (x, y) coordinates
            self.fov_map.compute_fov(player_x, player_y, FOV_RADIUS)
            
            # Update explored tiles 
            for x in range(MAP_WIDTH):
                for y in range(MAP_HEIGHT):
                    # Check FOV using our coordinate system
                    if (0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and 
                        self.fov_map.fov[y, x]):
                        self.explored[x, y] = True
                        self.fov[x, y] = True
                    else:
                        self.fov[x, y] = False
    
    def render(self, console):
        """Render the level to the console."""
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