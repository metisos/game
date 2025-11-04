"""
Player module for the game.

This module handles:
- Player sprite creation
- Keyboard/controller input handling
- Player movement mechanics (up, down, left, right)
- Player boundary detection
- Player state management
"""

import pygame
from typing import Tuple, Optional


class Player(pygame.sprite.Sprite):
    """Player sprite with movement mechanics."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int = 50,
        height: int = 50,
        color: Tuple[int, int, int] = (0, 255, 0),
        speed: int = 5
    ):
        """
        Initialize the player.

        Args:
            x: Initial x position
            y: Initial y position
            width: Player width in pixels
            height: Player height in pixels
            color: RGB color tuple
            speed: Movement speed in pixels per frame
        """
        super().__init__()

        self.width = width
        self.height = height
        self.color = color
        self.speed = speed

        # Create player surface
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        # Get rect for collision and positioning
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Movement state
        self.velocity_x = 0
        self.velocity_y = 0

        # Screen boundaries (set by game)
        self.screen_width = 800
        self.screen_height = 600

    def set_boundaries(self, width: int, height: int):
        """
        Set screen boundaries for movement constraints.

        Args:
            width: Screen width
            height: Screen height
        """
        self.screen_width = width
        self.screen_height = height

    def handle_input(self, keys: pygame.key.ScancodeWrapper):
        """
        Handle keyboard input for player movement.

        Args:
            keys: Pygame key state from pygame.key.get_pressed()
        """
        # Reset velocity
        self.velocity_x = 0
        self.velocity_y = 0

        # Check for arrow keys or WASD
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y = self.speed

    def update(self):
        """Update player position based on velocity."""
        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Constrain to screen boundaries
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_height - self.height))

    def get_position(self) -> Tuple[int, int]:
        """
        Get current player position.

        Returns:
            Tuple of (x, y) coordinates
        """
        return (self.rect.x, self.rect.y)

    def set_position(self, x: int, y: int):
        """
        Set player position.

        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.rect.x = x
        self.rect.y = y

    def get_center(self) -> Tuple[int, int]:
        """
        Get center position of player.

        Returns:
            Tuple of (center_x, center_y)
        """
        return self.rect.center

    def set_speed(self, speed: int):
        """
        Set player movement speed.

        Args:
            speed: New speed in pixels per frame
        """
        if speed < 0:
            raise ValueError("Speed must be non-negative")
        self.speed = speed

    def get_speed(self) -> int:
        """Get current movement speed."""
        return self.speed

    def draw(self, surface: pygame.Surface):
        """
        Draw player on surface.

        Args:
            surface: Pygame surface to draw on
        """
        surface.blit(self.image, self.rect)


class PlayerController:
    """
    Advanced player controller with additional features.

    Handles:
    - Diagonal movement normalization
    - Controller input support
    - Movement smoothing
    """

    def __init__(self, player: Player):
        """
        Initialize controller.

        Args:
            player: Player instance to control
        """
        self.player = player
        self.diagonal_speed_factor = 0.707  # 1/sqrt(2) for normalized diagonal movement

    def handle_keyboard_input(self, keys: pygame.key.ScancodeWrapper):
        """
        Handle keyboard input with diagonal movement normalization.

        Args:
            keys: Pygame key state
        """
        # Get input directions
        move_x = 0
        move_y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y += 1

        # Normalize diagonal movement
        if move_x != 0 and move_y != 0:
            self.player.velocity_x = int(move_x * self.player.speed * self.diagonal_speed_factor)
            self.player.velocity_y = int(move_y * self.player.speed * self.diagonal_speed_factor)
        else:
            self.player.velocity_x = move_x * self.player.speed
            self.player.velocity_y = move_y * self.player.speed

    def handle_joystick_input(self, joystick: Optional[pygame.joystick.Joystick]):
        """
        Handle joystick/controller input.

        Args:
            joystick: Pygame joystick instance (or None)
        """
        if joystick is None:
            return

        # Get analog stick values (-1.0 to 1.0)
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        # Apply deadzone
        deadzone = 0.15
        if abs(axis_x) < deadzone:
            axis_x = 0
        if abs(axis_y) < deadzone:
            axis_y = 0

        # Set velocity
        self.player.velocity_x = int(axis_x * self.player.speed)
        self.player.velocity_y = int(axis_y * self.player.speed)
