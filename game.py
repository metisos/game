"""
Main game file for the Pygame-based shooter game.

This is a basic framework demonstrating the scoring system.
Player movement, shooting mechanics, and enemy AI will be added in subsequent tickets.
"""

import pygame
import sys
from scoring import ScoreManager, ScoreDisplay


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
        pygame.display.set_caption("Space Shooter - Score System Demo")

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True

        # Initialize scoring system
        self.score_manager = ScoreManager()
        self.score_display = ScoreDisplay(font_size=36)
        self.score_display.initialize_pygame(pygame)

        # Demo: Track when to add points
        self.last_point_time = 0
        self.point_interval = 2000  # Add points every 2 seconds for demo

    def handle_events(self):
        """Handle game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Demo: Add points manually with spacebar
                    points_added = self.score_manager.add_points(100)
                    self.score_manager.increment_combo()
                    print(f"Added {points_added} points! Combo: {self.score_manager.get_combo_count()}")
                elif event.key == pygame.K_r:
                    # Reset score
                    self.score_manager.reset_score()
                    print("Score reset!")

    def update(self):
        """Update game state."""
        # Demo: Auto-add points every 2 seconds
        current_time = pygame.time.get_ticks()
        if current_time - self.last_point_time >= self.point_interval:
            self.score_manager.add_points(50)
            self.last_point_time = current_time

    def render(self):
        """Render game graphics."""
        # Clear screen with dark blue background
        self.screen.fill((0, 0, 50))

        # Render score display
        self.score_display.render_score(self.screen, self.score_manager)

        # Render instructions
        font = pygame.font.Font(None, 24)
        instructions = [
            "Press SPACE to add 100 points and increase combo",
            "Press R to reset score",
            "Press ESC to quit",
            "",
            f"Current Stats:",
            f"  Score: {self.score_manager.get_score()}",
            f"  Multiplier: {self.score_manager.get_multiplier():.1f}x",
            f"  Combo: {self.score_manager.get_combo_count()}",
        ]

        y_offset = 150
        for instruction in instructions:
            text_surface = font.render(instruction, True, (200, 200, 200))
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 30

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        print("Game started! Press SPACE to score points.")
        print("Score system features:")
        print("  - Point tracking")
        print("  - High score persistence")
        print("  - Combo system")
        print("  - Score multipliers")

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
