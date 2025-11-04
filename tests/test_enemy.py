"""
Unit tests for the enemy module.

Tests cover:
- Enemy initialization
- Movement patterns
- AI behavior
- Collision detection
- Enemy spawning
"""

import pytest
import pygame
from enemy import Enemy, EnemySpawner, check_collision, check_group_collision


@pytest.fixture
def pygame_init():
    """Initialize pygame before tests."""
    pygame.init()
    yield
    pygame.quit()


class TestEnemy:
    """Test cases for Enemy class."""

    def test_initialization(self, pygame_init):
        """Test enemy initializes correctly."""
        enemy = Enemy(100, 50, width=40, height=40, speed=2)

        assert enemy.rect.x == 100
        assert enemy.rect.y == 50
        assert enemy.width == 40
        assert enemy.height == 40
        assert enemy.speed == 2

    def test_vertical_movement(self, pygame_init):
        """Test vertical movement pattern."""
        enemy = Enemy(100, 50, speed=3, movement_pattern="vertical")
        enemy.set_boundaries(800, 600)

        initial_y = enemy.rect.y
        enemy.update()

        assert enemy.rect.y > initial_y
        assert enemy.velocity_y == 3

    def test_horizontal_movement(self, pygame_init):
        """Test horizontal movement pattern."""
        enemy = Enemy(100, 50, speed=2, movement_pattern="horizontal")
        enemy.set_boundaries(800, 600)

        enemy.update()

        # Should move horizontally
        assert enemy.velocity_x != 0

    def test_chase_movement_without_target(self, pygame_init):
        """Test chase movement defaults to vertical without target."""
        enemy = Enemy(100, 50, speed=2, movement_pattern="chase")
        enemy.set_boundaries(800, 600)

        enemy.update()

        # Should move downward when no target set
        assert enemy.velocity_y > 0

    def test_chase_movement_with_target(self, pygame_init):
        """Test chase movement towards target."""
        enemy = Enemy(100, 100, speed=3, movement_pattern="chase")
        enemy.set_boundaries(800, 600)
        enemy.set_target((200, 200))

        enemy.update()

        # Should move towards target
        assert enemy.velocity_x > 0  # Moving right
        assert enemy.velocity_y > 0  # Moving down

    def test_zigzag_movement(self, pygame_init):
        """Test zigzag movement pattern."""
        enemy = Enemy(100, 50, speed=2, movement_pattern="zigzag")
        enemy.set_boundaries(800, 600)

        enemy.update()

        assert enemy.velocity_y == 2
        assert enemy.velocity_x != 0

    def test_enemy_removed_offscreen(self, pygame_init):
        """Test enemy is removed when off screen."""
        enemy = Enemy(100, 700, speed=5, movement_pattern="vertical")
        enemy.set_boundaries(800, 600)

        # Create group and add enemy
        group = pygame.sprite.Group()
        group.add(enemy)

        # Update enemy (should go off screen)
        enemy.update()

        # Check if enemy was killed
        assert len(group) == 0

    def test_get_position(self, pygame_init):
        """Test getting enemy position."""
        enemy = Enemy(150, 250)

        pos = enemy.get_position()
        assert pos == (150, 250)

    def test_get_center(self, pygame_init):
        """Test getting enemy center."""
        enemy = Enemy(100, 100, width=40, height=40)

        center = enemy.get_center()
        assert center == (120, 120)


class TestEnemySpawner:
    """Test cases for EnemySpawner class."""

    def test_initialization(self, pygame_init):
        """Test spawner initializes correctly."""
        spawner = EnemySpawner(800, 600, spawn_rate=120, max_enemies=10)

        assert spawner.screen_width == 800
        assert spawner.screen_height == 600
        assert spawner.spawn_rate == 120
        assert spawner.max_enemies == 10
        assert spawner.spawn_timer == 0

    def test_spawn_enemy(self, pygame_init):
        """Test spawning an enemy."""
        spawner = EnemySpawner(800, 600)

        enemy = spawner.spawn_enemy()

        assert enemy is not None
        assert enemy.rect.y == -50  # Spawned above screen
        assert 20 <= enemy.rect.x <= 740

    def test_spawn_with_player_target(self, pygame_init):
        """Test spawning enemy with player target."""
        spawner = EnemySpawner(800, 600)
        player_pos = (400, 500)

        enemy = spawner.spawn_enemy(player_pos)

        assert enemy is not None
        assert enemy.target_pos == player_pos

    def test_update_spawner(self, pygame_init):
        """Test spawner update increments timer."""
        spawner = EnemySpawner(800, 600, spawn_rate=10)

        spawner.update(0)
        assert spawner.spawn_timer == 1

    def test_set_spawn_rate(self, pygame_init):
        """Test setting spawn rate."""
        spawner = EnemySpawner(800, 600)

        spawner.set_spawn_rate(60)
        assert spawner.spawn_rate == 60

    def test_set_max_enemies(self, pygame_init):
        """Test setting max enemies."""
        spawner = EnemySpawner(800, 600)

        spawner.set_max_enemies(15)
        assert spawner.max_enemies == 15

    def test_spawn_rate_minimum(self, pygame_init):
        """Test spawn rate has minimum of 1."""
        spawner = EnemySpawner(800, 600)

        spawner.set_spawn_rate(-5)
        assert spawner.spawn_rate == 1


class TestCollisionDetection:
    """Test cases for collision detection functions."""

    def test_check_collision_true(self, pygame_init):
        """Test collision detection when sprites collide."""
        enemy1 = Enemy(100, 100, width=40, height=40)
        enemy2 = Enemy(110, 110, width=40, height=40)

        result = check_collision(enemy1, enemy2)
        assert result is True

    def test_check_collision_false(self, pygame_init):
        """Test collision detection when sprites don't collide."""
        enemy1 = Enemy(100, 100, width=40, height=40)
        enemy2 = Enemy(200, 200, width=40, height=40)

        result = check_collision(enemy1, enemy2)
        assert result is False

    def test_check_group_collision(self, pygame_init):
        """Test collision with sprite group."""
        enemy1 = Enemy(100, 100, width=40, height=40)
        enemy2 = Enemy(110, 110, width=40, height=40)
        enemy3 = Enemy(200, 200, width=40, height=40)

        group = pygame.sprite.Group()
        group.add(enemy2, enemy3)

        collisions = check_group_collision(enemy1, group)

        assert len(collisions) == 1
        assert enemy2 in collisions


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
