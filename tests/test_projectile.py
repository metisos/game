"""
Unit tests for the projectile module.

Tests cover:
- Projectile creation and movement
- Weapon firing mechanics
- Fire rate and cooldown
- Projectile manager
- Auto-fire controller
"""

import pytest
import pygame
from projectile import Projectile, Weapon, ProjectileManager, AutoFire


@pytest.fixture
def pygame_init():
    """Initialize pygame before tests."""
    pygame.init()
    yield
    pygame.quit()


class TestProjectile:
    """Test cases for Projectile class."""

    def test_initialization(self, pygame_init):
        """Test projectile initializes correctly."""
        projectile = Projectile(100, 200, direction=(0, -1), speed=10, damage=1)

        assert projectile.rect.centerx == 100
        assert projectile.rect.centery == 200
        assert projectile.speed == 10
        assert projectile.damage == 1

    def test_direction_normalization(self, pygame_init):
        """Test that direction is normalized."""
        projectile = Projectile(100, 100, direction=(3, 4), speed=5)

        # Direction should be normalized (3,4) -> (0.6, 0.8)
        assert projectile.direction == pytest.approx((0.6, 0.8), 0.01)

    def test_upward_movement(self, pygame_init):
        """Test upward projectile movement."""
        projectile = Projectile(100, 100, direction=(0, -1), speed=10)
        projectile.set_boundaries(800, 600)

        initial_y = projectile.rect.y
        projectile.update()

        assert projectile.rect.y < initial_y

    def test_horizontal_movement(self, pygame_init):
        """Test horizontal projectile movement."""
        projectile = Projectile(100, 100, direction=(1, 0), speed=10)
        projectile.set_boundaries(800, 600)

        initial_x = projectile.rect.x
        projectile.update()

        assert projectile.rect.x > initial_x

    def test_projectile_removed_offscreen_top(self, pygame_init):
        """Test projectile removed when off screen (top)."""
        projectile = Projectile(100, 10, direction=(0, -1), speed=20)
        projectile.set_boundaries(800, 600)

        group = pygame.sprite.Group()
        group.add(projectile)

        projectile.update()

        assert len(group) == 0

    def test_projectile_removed_offscreen_bottom(self, pygame_init):
        """Test projectile removed when off screen (bottom)."""
        projectile = Projectile(100, 590, direction=(0, 1), speed=20)
        projectile.set_boundaries(800, 600)

        group = pygame.sprite.Group()
        group.add(projectile)

        projectile.update()

        assert len(group) == 0

    def test_get_damage(self, pygame_init):
        """Test getting projectile damage."""
        projectile = Projectile(100, 100, damage=5)

        assert projectile.get_damage() == 5


class TestWeapon:
    """Test cases for Weapon class."""

    def test_initialization(self, pygame_init):
        """Test weapon initializes correctly."""
        weapon = Weapon(fire_rate=10, projectile_speed=15, projectile_damage=2)

        assert weapon.fire_rate == 10
        assert weapon.projectile_speed == 15
        assert weapon.projectile_damage == 2
        assert weapon.can_fire is True

    def test_fire_projectile(self, pygame_init):
        """Test firing a projectile."""
        weapon = Weapon()

        projectile = weapon.fire((100, 100))

        assert projectile is not None
        assert projectile.rect.centerx == 100
        assert projectile.rect.centery == 100

    def test_cooldown_prevents_firing(self, pygame_init):
        """Test that cooldown prevents immediate firing."""
        weapon = Weapon(fire_rate=10)

        # Fire first shot
        projectile1 = weapon.fire((100, 100))
        assert projectile1 is not None

        # Immediate second shot should fail
        projectile2 = weapon.fire((100, 100))
        assert projectile2 is None

    def test_cooldown_recovery(self, pygame_init):
        """Test that cooldown recovers after updates."""
        weapon = Weapon(fire_rate=2)

        # Fire first shot
        weapon.fire((100, 100))

        # Update cooldown - need fire_rate+1 updates for can_fire to become True
        for _ in range(3):  # 2 + 1
            weapon.update()

        # Should be able to fire again
        projectile = weapon.fire((100, 100))
        assert projectile is not None

    def test_is_ready(self, pygame_init):
        """Test checking if weapon is ready to fire."""
        weapon = Weapon(fire_rate=5)

        assert weapon.is_ready() is True

        weapon.fire((100, 100))
        assert weapon.is_ready() is False

        # Update until ready - need fire_rate+1 updates
        for _ in range(6):  # 5 + 1
            weapon.update()

        assert weapon.is_ready() is True

    def test_set_fire_rate(self, pygame_init):
        """Test setting fire rate."""
        weapon = Weapon()

        weapon.set_fire_rate(20)
        assert weapon.get_fire_rate() == 20

    def test_fire_rate_minimum(self, pygame_init):
        """Test fire rate has minimum of 1."""
        weapon = Weapon()

        weapon.set_fire_rate(-5)
        assert weapon.get_fire_rate() == 1


class TestProjectileManager:
    """Test cases for ProjectileManager class."""

    def test_initialization(self, pygame_init):
        """Test manager initializes correctly."""
        manager = ProjectileManager()

        assert manager.get_count() == 0

    def test_add_player_projectile(self, pygame_init):
        """Test adding player projectile."""
        manager = ProjectileManager()
        projectile = Projectile(100, 100)

        manager.add_player_projectile(projectile)

        assert manager.get_count() == 1
        assert len(manager.player_projectiles) == 1

    def test_add_enemy_projectile(self, pygame_init):
        """Test adding enemy projectile."""
        manager = ProjectileManager()
        projectile = Projectile(100, 100)

        manager.add_enemy_projectile(projectile)

        assert manager.get_count() == 1
        assert len(manager.enemy_projectiles) == 1

    def test_clear_projectiles(self, pygame_init):
        """Test clearing all projectiles."""
        manager = ProjectileManager()

        projectile1 = Projectile(100, 100)
        projectile2 = Projectile(200, 200)

        manager.add_player_projectile(projectile1)
        manager.add_enemy_projectile(projectile2)

        manager.clear()

        assert manager.get_count() == 0


class TestAutoFire:
    """Test cases for AutoFire class."""

    def test_initialization(self, pygame_init):
        """Test auto-fire initializes correctly."""
        weapon = Weapon()
        auto_fire = AutoFire(weapon)

        assert auto_fire.weapon == weapon
        assert auto_fire.is_firing is False

    def test_start_firing(self, pygame_init):
        """Test starting auto-fire."""
        weapon = Weapon()
        auto_fire = AutoFire(weapon)

        auto_fire.start_firing()

        assert auto_fire.is_firing is True

    def test_stop_firing(self, pygame_init):
        """Test stopping auto-fire."""
        weapon = Weapon()
        auto_fire = AutoFire(weapon)

        auto_fire.start_firing()
        auto_fire.stop_firing()

        assert auto_fire.is_firing is False

    def test_auto_fire_shoots_when_active(self, pygame_init):
        """Test auto-fire shoots when active."""
        weapon = Weapon(fire_rate=1)
        auto_fire = AutoFire(weapon)

        auto_fire.start_firing()
        projectile = auto_fire.update_and_fire((100, 100))

        assert projectile is not None

    def test_auto_fire_doesnt_shoot_when_inactive(self, pygame_init):
        """Test auto-fire doesn't shoot when inactive."""
        weapon = Weapon(fire_rate=1)
        auto_fire = AutoFire(weapon)

        projectile = auto_fire.update_and_fire((100, 100))

        assert projectile is None

    def test_auto_fire_respects_cooldown(self, pygame_init):
        """Test auto-fire respects weapon cooldown."""
        weapon = Weapon(fire_rate=10)
        auto_fire = AutoFire(weapon)

        auto_fire.start_firing()

        # First shot
        projectile1 = auto_fire.update_and_fire((100, 100))
        assert projectile1 is not None

        # Immediate second shot should fail
        projectile2 = auto_fire.update_and_fire((100, 100))
        assert projectile2 is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
