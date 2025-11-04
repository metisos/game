"""
Main game file for the Pygame-based shooter game.

Features:
- Player movement (WASD or Arrow keys)
- Shooting mechanics (SPACE to shoot)
- Enemy AI with multiple movement patterns
- Scoring system with combos and multipliers
- Game over screen with restart option
"""

import pygame
import sys
from scoring import ScoreManager, ScoreDisplay
from player import Player, PlayerController
from enemy import Enemy, EnemySpawner, check_group_collision
from projectile import Weapon, ProjectileManager, AutoFire
from game_states import GameOverState, PauseState


class Game:
    """Main game class."""

    def __init__(self, width: int = 800, height: int = 600):
        """
        Initialize the game.

        Args:
            width: Screen width in pixels
            height: Screen height in pixels
        """
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Space Shooter")

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        self.game_state = "playing"  # playing, paused, game_over

        # Initialize game systems
        self.init_game()

    def init_game(self):
        """Initialize/reset game objects."""
        # Scoring system
        self.score_manager = ScoreManager()
        self.score_display = ScoreDisplay(font_size=36)
        self.score_display.initialize_pygame(pygame)

        # Player
        self.player = Player(
            x=self.width // 2 - 25,
            y=self.height - 100,
            color=(0, 255, 0)
        )
        self.player.set_boundaries(self.width, self.height)
        self.player_controller = PlayerController(self.player)

        # Weapon and shooting
        self.weapon = Weapon(fire_rate=15, projectile_speed=12)
        self.auto_fire = AutoFire(self.weapon)
        self.projectile_manager = ProjectileManager()

        # Enemies
        self.enemy_spawner = EnemySpawner(
            self.width,
            self.height,
            spawn_rate=90,
            max_enemies=8
        )
        self.enemies = pygame.sprite.Group()

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Player health
        self.player_health = 3
        self.player_invulnerable = False
        self.invulnerable_timer = 0

        # Game state objects
        self.game_over_state = None
        self.pause_state = PauseState(self)

    def handle_events(self):
        """Handle game events."""
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if self.game_state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "paused"
                    elif event.key == pygame.K_p:
                        self.game_state = "paused"

        # Handle state-specific events
        if self.game_state == "game_over":
            if self.game_over_state:
                action = self.game_over_state.handle_events(events)
                if action == "restart":
                    self.restart_game()
                elif action == "quit":
                    self.running = False

        elif self.game_state == "paused":
            action = self.pause_state.handle_events(events)
            if action == "resume":
                self.game_state = "playing"
            elif action == "quit":
                self.running = False

        elif self.game_state == "playing":
            # Player input
            keys = pygame.key.get_pressed()
            self.player_controller.handle_keyboard_input(keys)

            # Shooting
            if keys[pygame.K_SPACE]:
                self.auto_fire.start_firing()
            else:
                self.auto_fire.stop_firing()

    def update(self):
        """Update game state."""
        if self.game_state != "playing":
            return

        # Update player
        self.player.update()

        # Handle shooting
        projectile = self.auto_fire.update_and_fire(
            self.player.get_center(),
            direction=(0, -1),
            screen_width=self.width,
            screen_height=self.height
        )
        if projectile:
            self.projectile_manager.add_player_projectile(projectile)
            self.all_sprites.add(projectile)

        # Update projectiles
        self.projectile_manager.update()

        # Update enemy spawner and spawn enemies
        self.enemy_spawner.update(len(self.enemies), self.player.get_center())

        # Spawn new enemies
        if len(self.enemies) < self.enemy_spawner.max_enemies:
            if self.enemy_spawner.spawn_timer == 0:
                enemy = self.enemy_spawner.spawn_enemy(self.player.get_center())
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

        # Update enemies
        for enemy in self.enemies:
            enemy.update()

        # Check collisions: projectiles hitting enemies
        for projectile in self.projectile_manager.player_projectiles:
            hit_enemies = check_group_collision(projectile, self.enemies)
            if hit_enemies:
                # Add score for hit
                points = self.score_manager.add_points(100)
                self.score_manager.increment_combo()

                # Remove projectile and enemy
                projectile.kill()
                for enemy in hit_enemies:
                    enemy.kill()

        # Check collisions: enemies hitting player
        if not self.player_invulnerable:
            hit_enemies = check_group_collision(self.player, self.enemies)
            if hit_enemies:
                self.player_health -= 1
                self.player_invulnerable = True
                self.invulnerable_timer = 60  # 1 second at 60 FPS

                # Reset combo on hit
                self.score_manager.reset_combo()

                # Remove enemy
                for enemy in hit_enemies:
                    enemy.kill()

                # Check for game over
                if self.player_health <= 0:
                    self.game_over()

        # Update invulnerability
        if self.player_invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.player_invulnerable = False

    def render(self):
        """Render game graphics."""
        # Clear screen
        self.screen.fill((0, 0, 50))

        if self.game_state == "playing":
            # Draw all sprites
            self.all_sprites.draw(self.screen)

            # Draw score
            self.score_display.render_score(self.screen, self.score_manager)

            # Draw health
            self.render_health()

            # Draw player flash if invulnerable
            if self.player_invulnerable and self.invulnerable_timer % 10 < 5:
                # Flash player by not drawing it (already drawn above)
                pass

        elif self.game_state == "game_over":
            if self.game_over_state:
                self.game_over_state.render(self.screen)

        elif self.game_state == "paused":
            # Draw game scene first
            self.all_sprites.draw(self.screen)
            self.score_display.render_score(self.screen, self.score_manager)
            self.render_health()

            # Draw pause overlay
            self.pause_state.render(self.screen)

        pygame.display.flip()

    def render_health(self):
        """Render player health bar."""
        font = pygame.font.Font(None, 36)
        health_text = f"Health: {self.player_health}"
        health_surface = font.render(health_text, True, (255, 100, 100))
        self.screen.blit(health_surface, (self.width - 180, 10))

    def game_over(self):
        """Handle game over."""
        self.game_state = "game_over"
        final_score = self.score_manager.get_score()
        high_score = self.score_manager.get_high_score()
        self.game_over_state = GameOverState(self, final_score, high_score)

    def restart_game(self):
        """Restart the game."""
        self.game_state = "playing"
        self.init_game()

    def run(self):
        """Main game loop."""
        print("Space Shooter - Game Started!")
        print("Controls:")
        print("  WASD or Arrow Keys - Move")
        print("  SPACE - Shoot")
        print("  P or ESC - Pause")
        print("\nFeatures:")
        print("  - Destroy enemies to score points")
        print("  - Combo system increases score multiplier")
        print("  - Avoid enemies to survive")

        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

        self.quit()

    def quit(self):
        """Clean up and quit."""
        final_stats = self.score_manager.get_stats()
        print(f"\nGame Over!")
        print(f"Final Score: {final_stats['current_score']}")
        print(f"High Score: {final_stats['high_score']}")
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
