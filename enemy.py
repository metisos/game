"""
Enemy module for the game.

This module handles:
- Enemy sprite creation
- Basic enemy AI (movement patterns)
- Collision detection
- Enemy spawning
"""

import pygame
import random
import math
from typing import Tuple, List, Optional


class Enemy(pygame.sprite.Sprite):
    """Basic enemy sprite with AI movement."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int = 40,
        height: int = 40,
        color: Tuple[int, int, int] = (255, 0, 0),
        speed: int = 2,
        movement_pattern: str = "vertical"
    ):
        """
        Initialize enemy.

        Args:
            x: Initial x position
            y: Initial y position
            width: Enemy width
            height: Enemy height
            color: RGB color tuple
            speed: Movement speed
            movement_pattern: Movement pattern ('vertical', 'horizontal', 'chase', 'zigzag')
        """
        super().__init__()

        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.movement_pattern = movement_pattern

        # Create enemy surface
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Movement state
        self.velocity_x = 0
        self.velocity_y = speed

        # Screen boundaries
        self.screen_width = 800
        self.screen_height = 600

        # AI state
        self.direction = 1  # 1 for right/down, -1 for left/up
        self.zigzag_timer = 0
        self.target_pos = None

    def set_boundaries(self, width: int, height: int):
        """Set screen boundaries."""
        self.screen_width = width
        self.screen_height = height

    def set_target(self, target_pos: Tuple[int, int]):
        """
        Set target position for chase movement.

        Args:
            target_pos: (x, y) tuple of target position
        """
        self.target_pos = target_pos

    def update(self):
        """Update enemy position based on AI pattern."""
        if self.movement_pattern == "vertical":
            self._move_vertical()
        elif self.movement_pattern == "horizontal":
            self._move_horizontal()
        elif self.movement_pattern == "chase":
            self._move_chase()
        elif self.movement_pattern == "zigzag":
            self._move_zigzag()

        # Apply movement
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Remove enemy if it goes off screen (bottom)
        if self.rect.top > self.screen_height:
            self.kill()

    def _move_vertical(self):
        """Simple vertical downward movement."""
        self.velocity_x = 0
        self.velocity_y = self.speed

    def _move_horizontal(self):
        """Horizontal back-and-forth movement."""
        self.velocity_x = self.speed * self.direction
        self.velocity_y = 1  # Slow downward drift

        # Bounce off edges
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.direction *= -1

    def _move_chase(self):
        """Chase target position (usually player)."""
        if self.target_pos is None:
            self._move_vertical()
            return

        # Calculate direction to target
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery

        # Calculate distance
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            # Normalize and apply speed
            self.velocity_x = int((dx / distance) * self.speed)
            self.velocity_y = int((dy / distance) * self.speed)
        else:
            self.velocity_x = 0
            self.velocity_y = 0

    def _move_zigzag(self):
        """Zigzag movement pattern."""
        self.velocity_y = self.speed

        # Change horizontal direction periodically
        self.zigzag_timer += 1
        if self.zigzag_timer >= 30:  # Change direction every 30 frames
            self.direction *= -1
            self.zigzag_timer = 0

        self.velocity_x = self.speed * self.direction * 2

        # Bounce off edges
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.direction *= -1

    def get_position(self) -> Tuple[int, int]:
        """Get enemy position."""
        return (self.rect.x, self.rect.y)

    def get_center(self) -> Tuple[int, int]:
        """Get enemy center position."""
        return self.rect.center


class EnemySpawner:
    """Manages enemy spawning."""

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        spawn_rate: int = 120,  # Frames between spawns
        max_enemies: int = 10
    ):
        """
        Initialize enemy spawner.

        Args:
            screen_width: Screen width
            screen_height: Screen height
            spawn_rate: Frames between enemy spawns
            max_enemies: Maximum number of enemies at once
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spawn_rate = spawn_rate
        self.max_enemies = max_enemies

        self.spawn_timer = 0
        self.enemies = pygame.sprite.Group()

        # Movement patterns to choose from
        self.patterns = ["vertical", "horizontal", "zigzag", "chase"]

    def update(self, current_enemies: int, player_pos: Optional[Tuple[int, int]] = None):
        """
        Update spawner and spawn enemies if needed.

        Args:
            current_enemies: Number of enemies currently alive
            player_pos: Player position for chase enemies
        """
        self.spawn_timer += 1

        # Spawn new enemy if timer expires and under max
        if self.spawn_timer >= self.spawn_rate and current_enemies < self.max_enemies:
            self.spawn_enemy(player_pos)
            self.spawn_timer = 0

    def spawn_enemy(self, player_pos: Optional[Tuple[int, int]] = None) -> Enemy:
        """
        Spawn a new enemy.

        Args:
            player_pos: Player position for chase enemies

        Returns:
            Newly created Enemy instance
        """
        # Random x position at top of screen
        x = random.randint(20, self.screen_width - 60)
        y = -50

        # Random movement pattern
        pattern = random.choice(self.patterns)

        # Random speed variation
        speed = random.randint(2, 4)

        # Create enemy
        enemy = Enemy(x, y, speed=speed, movement_pattern=pattern)
        enemy.set_boundaries(self.screen_width, self.screen_height)

        if player_pos:
            enemy.set_target(player_pos)

        return enemy

    def set_spawn_rate(self, rate: int):
        """Set spawn rate (frames between spawns)."""
        self.spawn_rate = max(1, rate)

    def set_max_enemies(self, max_enemies: int):
        """Set maximum number of enemies."""
        self.max_enemies = max(1, max_enemies)


def check_collision(sprite1: pygame.sprite.Sprite, sprite2: pygame.sprite.Sprite) -> bool:
    """
    Check collision between two sprites.

    Args:
        sprite1: First sprite
        sprite2: Second sprite

    Returns:
        True if sprites collide, False otherwise
    """
    return sprite1.rect.colliderect(sprite2.rect)


def check_group_collision(
    sprite: pygame.sprite.Sprite,
    group: pygame.sprite.Group
) -> List[pygame.sprite.Sprite]:
    """
    Check collision between sprite and group.

    Args:
        sprite: Single sprite
        group: Group of sprites

    Returns:
        List of sprites in group that collide with sprite
    """
    return pygame.sprite.spritecollide(sprite, group, False)
