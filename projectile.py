"""
Projectile module for the game.

This module handles:
- Projectile/bullet creation
- Projectile movement
- Projectile collision detection
- Shooting mechanics
"""

import pygame
from typing import Tuple, Optional


class Projectile(pygame.sprite.Sprite):
    """Projectile/bullet sprite."""

    def __init__(
        self,
        x: int,
        y: int,
        direction: Tuple[int, int] = (0, -1),
        width: int = 5,
        height: int = 15,
        color: Tuple[int, int, int] = (255, 255, 0),
        speed: int = 10,
        damage: int = 1
    ):
        """
        Initialize projectile.

        Args:
            x: Initial x position
            y: Initial y position
            direction: Direction vector (dx, dy)
            width: Projectile width
            height: Projectile height
            color: RGB color tuple
            speed: Movement speed
            damage: Damage dealt on hit
        """
        super().__init__()

        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.damage = damage

        # Normalize direction
        length = (direction[0]**2 + direction[1]**2)**0.5
        if length > 0:
            self.direction = (direction[0] / length, direction[1] / length)
        else:
            self.direction = (0, -1)

        # Create projectile surface
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Screen boundaries
        self.screen_width = 800
        self.screen_height = 600

    def set_boundaries(self, width: int, height: int):
        """Set screen boundaries."""
        self.screen_width = width
        self.screen_height = height

    def update(self):
        """Update projectile position."""
        # Move in direction
        self.rect.x += int(self.direction[0] * self.speed)
        self.rect.y += int(self.direction[1] * self.speed)

        # Remove if off screen
        if (self.rect.bottom < 0 or self.rect.top > self.screen_height or
                self.rect.right < 0 or self.rect.left > self.screen_width):
            self.kill()

    def get_position(self) -> Tuple[int, int]:
        """Get projectile position."""
        return (self.rect.x, self.rect.y)

    def get_damage(self) -> int:
        """Get projectile damage."""
        return self.damage


class Weapon:
    """
    Weapon class for managing shooting mechanics.

    Handles:
    - Firing cooldown
    - Projectile creation
    - Fire rate management
    """

    def __init__(
        self,
        fire_rate: int = 10,  # Frames between shots
        projectile_speed: int = 10,
        projectile_damage: int = 1,
        projectile_color: Tuple[int, int, int] = (255, 255, 0)
    ):
        """
        Initialize weapon.

        Args:
            fire_rate: Frames between shots (lower = faster)
            projectile_speed: Speed of projectiles
            projectile_damage: Damage per projectile
            projectile_color: Color of projectiles
        """
        self.fire_rate = fire_rate
        self.projectile_speed = projectile_speed
        self.projectile_damage = projectile_damage
        self.projectile_color = projectile_color

        self.cooldown_timer = 0
        self.can_fire = True

    def update(self):
        """Update weapon cooldown."""
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
            self.can_fire = False
        else:
            self.can_fire = True

    def fire(
        self,
        position: Tuple[int, int],
        direction: Tuple[int, int] = (0, -1),
        screen_width: int = 800,
        screen_height: int = 600
    ) -> Optional[Projectile]:
        """
        Fire a projectile.

        Args:
            position: Starting position (x, y)
            direction: Direction vector (dx, dy)
            screen_width: Screen width for boundaries
            screen_height: Screen height for boundaries

        Returns:
            Projectile instance if fired, None if on cooldown
        """
        if not self.can_fire:
            return None

        # Create projectile
        projectile = Projectile(
            position[0],
            position[1],
            direction=direction,
            speed=self.projectile_speed,
            damage=self.projectile_damage,
            color=self.projectile_color
        )
        projectile.set_boundaries(screen_width, screen_height)

        # Start cooldown
        self.cooldown_timer = self.fire_rate
        self.can_fire = False

        return projectile

    def set_fire_rate(self, rate: int):
        """Set fire rate (lower = faster)."""
        self.fire_rate = max(1, rate)

    def get_fire_rate(self) -> int:
        """Get current fire rate."""
        return self.fire_rate

    def is_ready(self) -> bool:
        """Check if weapon can fire."""
        return self.can_fire


class ProjectileManager:
    """Manages all projectiles in the game."""

    def __init__(self):
        """Initialize projectile manager."""
        self.projectiles = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()

    def add_player_projectile(self, projectile: Projectile):
        """Add player projectile."""
        self.projectiles.add(projectile)
        self.player_projectiles.add(projectile)

    def add_enemy_projectile(self, projectile: Projectile):
        """Add enemy projectile."""
        self.projectiles.add(projectile)
        self.enemy_projectiles.add(projectile)

    def update(self):
        """Update all projectiles."""
        self.projectiles.update()

    def draw(self, surface: pygame.Surface):
        """Draw all projectiles."""
        self.projectiles.draw(surface)

    def clear(self):
        """Clear all projectiles."""
        self.projectiles.empty()
        self.player_projectiles.empty()
        self.enemy_projectiles.empty()

    def get_count(self) -> int:
        """Get total projectile count."""
        return len(self.projectiles)


class AutoFire:
    """
    Auto-fire controller for continuous shooting.

    Handles automatic firing when button/key is held down.
    """

    def __init__(self, weapon: Weapon):
        """
        Initialize auto-fire controller.

        Args:
            weapon: Weapon instance to control
        """
        self.weapon = weapon
        self.is_firing = False

    def start_firing(self):
        """Start auto-fire mode."""
        self.is_firing = True

    def stop_firing(self):
        """Stop auto-fire mode."""
        self.is_firing = False

    def update_and_fire(
        self,
        position: Tuple[int, int],
        direction: Tuple[int, int] = (0, -1),
        screen_width: int = 800,
        screen_height: int = 600
    ) -> Optional[Projectile]:
        """
        Update and fire if in auto-fire mode.

        Args:
            position: Firing position
            direction: Firing direction
            screen_width: Screen width
            screen_height: Screen height

        Returns:
            Projectile if fired, None otherwise
        """
        self.weapon.update()

        if self.is_firing and self.weapon.can_fire:
            return self.weapon.fire(position, direction, screen_width, screen_height)

        return None
