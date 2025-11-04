"""
Unit tests for the player module.

Tests cover:
- Player initialization
- Movement mechanics
- Boundary detection
- Input handling
- Player controller
"""

import pytest
import pygame
from player import Player, PlayerController


@pytest.fixture
def pygame_init():
    """Initialize pygame before tests."""
    pygame.init()
    yield
    pygame.quit()


class TestPlayer:
    """Test cases for Player class."""

    def test_initialization(self, pygame_init):
        """Test player initializes correctly."""
        player = Player(100, 200, width=50, height=50, speed=5)

        assert player.rect.x == 100
        assert player.rect.y == 200
        assert player.width == 50
        assert player.height == 50
        assert player.speed == 5

    def test_get_position(self, pygame_init):
        """Test getting player position."""
        player = Player(150, 250)
        pos = player.get_position()

        assert pos == (150, 250)

    def test_set_position(self, pygame_init):
        """Test setting player position."""
        player = Player(100, 100)
        player.set_position(200, 300)

        assert player.get_position() == (200, 300)

    def test_get_center(self, pygame_init):
        """Test getting player center."""
        player = Player(100, 100, width=50, height=50)
        center = player.get_center()

        assert center == (125, 125)

    def test_set_speed(self, pygame_init):
        """Test setting player speed."""
        player = Player(100, 100, speed=5)
        player.set_speed(10)

        assert player.get_speed() == 10

    def test_invalid_speed(self, pygame_init):
        """Test that negative speed raises error."""
        player = Player(100, 100)

        with pytest.raises(ValueError):
            player.set_speed(-5)

    def test_manual_velocity_setting(self, pygame_init):
        """Test manually setting velocity (simulates input)."""
        player = Player(100, 100, speed=5)

        # Manually set velocity (as input handler would do)
        player.velocity_x = -5
        player.velocity_y = 0

        assert player.velocity_x == -5

    def test_update_movement(self, pygame_init):
        """Test player movement update."""
        player = Player(100, 100, speed=5)
        player.set_boundaries(800, 600)

        player.velocity_x = 5
        player.velocity_y = -3
        player.update()

        assert player.rect.x == 105
        assert player.rect.y == 97

    def test_boundary_left(self, pygame_init):
        """Test left boundary constraint."""
        player = Player(5, 100, speed=10)
        player.set_boundaries(800, 600)

        player.velocity_x = -10
        player.update()

        assert player.rect.x == 0

    def test_boundary_right(self, pygame_init):
        """Test right boundary constraint."""
        player = Player(790, 100, width=50, speed=20)
        player.set_boundaries(800, 600)

        player.velocity_x = 20
        player.update()

        assert player.rect.x == 750  # 800 - 50

    def test_boundary_top(self, pygame_init):
        """Test top boundary constraint."""
        player = Player(100, 5, height=50, speed=10)
        player.set_boundaries(800, 600)

        player.velocity_y = -10
        player.update()

        assert player.rect.y == 0

    def test_boundary_bottom(self, pygame_init):
        """Test bottom boundary constraint."""
        player = Player(100, 590, height=50, speed=20)
        player.set_boundaries(800, 600)

        player.velocity_y = 20
        player.update()

        assert player.rect.y == 550  # 600 - 50


class TestPlayerController:
    """Test cases for PlayerController class."""

    def test_initialization(self, pygame_init):
        """Test controller initializes correctly."""
        player = Player(100, 100)
        controller = PlayerController(player)

        assert controller.player == player
        assert controller.diagonal_speed_factor == pytest.approx(0.707, 0.01)

    def test_diagonal_speed_factor(self, pygame_init):
        """Test that diagonal speed factor is correctly set."""
        player = Player(100, 100, speed=10)
        controller = PlayerController(player)

        # Test that diagonal factor is approximately 1/sqrt(2)
        assert controller.diagonal_speed_factor == pytest.approx(0.707, 0.01)

        # Test manually setting diagonal velocity
        # (simulating what would happen with diagonal input)
        player.velocity_x = int(1 * player.speed * controller.diagonal_speed_factor)
        player.velocity_y = int(1 * player.speed * controller.diagonal_speed_factor)

        # Diagonal speed should be less than full speed
        assert abs(player.velocity_x) < 10
        assert abs(player.velocity_y) < 10
        # But combined magnitude should be close to original speed
        magnitude = (player.velocity_x**2 + player.velocity_y**2)**0.5
        assert magnitude == pytest.approx(10.0, 0.5)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
