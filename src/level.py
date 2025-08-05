"""
Level generation and management.
"""

import random
import numpy as np
import tcod

from constants import (
    MAP_WIDTH, MAP_HEIGHT,
    TILE_WALL, TILE_FLOOR, TILE_STAIRS_DOWN, TILE_STAIRS_UP,
    COLOR_DARK_WALL, COLOR_DARK_GROUND, COLOR_LIGHT_WALL, COLOR_LIGHT_GROUND
)
from monster import create_monster_for_level
from items import create_random_item_for_level


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
        self.monsters = []
        self.items = []
        self.generate_level()
        
        # Place monsters and items after level generation
        self.place_monsters()
        self.place_items()
        
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
    
    def place_monsters(self):
        """Place monsters randomly throughout the level."""
        # Number of monsters based on level
        if self.level_number == 1:
            monster_count = random.randint(1, 2)  # Few monsters to introduce combat
        elif self.level_number <= 3:
            monster_count = random.randint(2, 4)
        elif self.level_number <= 6:
            monster_count = random.randint(3, 6)
        elif self.level_number <= 9:
            monster_count = random.randint(4, 8)
        else:  # Level 10 - boss level
            monster_count = 1  # Just the boss
        
        monsters_placed = 0
        attempts = 0
        max_attempts = 100
        
        while monsters_placed < monster_count and attempts < max_attempts:
            attempts += 1
            
            # Pick a random room
            if len(self.rooms) == 0:
                break
                
            room = random.choice(self.rooms)
            
            # Pick a random position in the room
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)
            
            # Check if position is valid (walkable and not occupied)
            if self.is_walkable(x, y) and not self.is_position_occupied(x, y):
                # Don't place monsters on stairs
                if not (self.is_stairs_down(x, y) or self.is_stairs_up(x, y)):
                    # Create appropriate monster for this level
                    monster_class = create_monster_for_level(self.level_number)
                    monster = monster_class(x, y)
                    self.monsters.append(monster)
                    monsters_placed += 1
    
    def is_position_occupied(self, x, y):
        """Check if a position is occupied by a monster."""
        for monster in self.monsters:
            if monster.x == x and monster.y == y and monster.is_alive():
                return True
        return False
    
    def get_monster_at(self, x, y):
        """Get the monster at the given position, if any."""
        for monster in self.monsters:
            if monster.x == x and monster.y == y and monster.is_alive():
                return monster
        return None
    
    def remove_dead_monsters(self):
        """Remove dead monsters from the level."""
        self.monsters = [monster for monster in self.monsters if monster.is_alive()]
    
    def place_items(self):
        """Place items randomly throughout the level."""
        # Number of items based on level
        if self.level_number <= 2:
            item_count = random.randint(1, 3)
        elif self.level_number <= 5:
            item_count = random.randint(2, 4)
        elif self.level_number <= 8:
            item_count = random.randint(3, 5)
        else:  # Level 9-10
            item_count = random.randint(2, 4)  # Fewer items on boss levels, but higher quality
        
        items_placed = 0
        attempts = 0
        max_attempts = 100
        
        while items_placed < item_count and attempts < max_attempts:
            attempts += 1
            
            # Pick a random room
            if len(self.rooms) == 0:
                break
                
            room = random.choice(self.rooms)
            
            # Pick a random position in the room
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)
            
            # Check if position is valid (walkable, not occupied, not on stairs)
            if (self.is_walkable(x, y) and 
                not self.is_position_occupied(x, y) and
                not self.is_item_at(x, y) and
                not (self.is_stairs_down(x, y) or self.is_stairs_up(x, y))):
                
                # Create appropriate item for this level
                item = create_random_item_for_level(self.level_number, x, y)
                self.items.append(item)
                items_placed += 1
    
    def is_item_at(self, x, y):
        """Check if there's an item at the given position."""
        for item in self.items:
            if item.x == x and item.y == y:
                return True
        return False
    
    def get_item_at(self, x, y):
        """Get the item at the given position, if any."""
        for item in self.items:
            if item.x == x and item.y == y:
                return item
        return None
    
    def remove_item(self, item):
        """Remove an item from the level."""
        if item in self.items:
            self.items.remove(item)
    
    def add_item_drop(self, x, y, item):
        """Add an item drop at the specified position."""
        item.x = x
        item.y = y
        self.items.append(item)
    
    def is_walkable(self, x, y):
        """Check if a tile is walkable."""
        if x < 0 or x >= MAP_WIDTH or y < 0 or y >= MAP_HEIGHT:
            return False
        if self.tiles[x, y] == TILE_WALL:
            return False
        # Can't walk through living monsters
        if self.is_position_occupied(x, y):
            return False
        return True
    
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
    
    def update_fov(self, player_x, player_y, fov_radius):
        """Update field of view from player position."""
        # Ensure player is within bounds
        if (0 <= player_x < MAP_WIDTH and 0 <= player_y < MAP_HEIGHT):
            # tcod.map.Map.compute_fov expects (x, y) coordinates
            self.fov_map.compute_fov(player_x, player_y, fov_radius)
            
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
        
        # Render items on top of terrain (but below monsters)
        for item in self.items:
            item.render(console, self.fov)
        
        # Render monsters on top of everything
        for monster in self.monsters:
            if monster.is_alive():
                monster.render(console, self.fov)