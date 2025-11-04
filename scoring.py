"""
Scoring system module for the game.

This module handles:
- Point tracking
- Score display
- High score management
- Score events (combos, multipliers, etc.)
"""

import json
import os
from typing import Optional


class ScoreManager:
    """Manages game scoring, including points, high scores, and multipliers."""

    def __init__(self, high_score_file: str = "highscore.json"):
        """
        Initialize the score manager.

        Args:
            high_score_file: Path to file storing high scores
        """
        self.current_score = 0
        self.high_score = 0
        self.multiplier = 1.0
        self.high_score_file = high_score_file
        self.combo_count = 0
        self.load_high_score()

    def add_points(self, points: int) -> int:
        """
        Add points to the current score.

        Args:
            points: Base points to add (before multiplier)

        Returns:
            Actual points added (after multiplier)
        """
        if points < 0:
            raise ValueError("Points must be non-negative")

        actual_points = int(points * self.multiplier)
        self.current_score += actual_points

        # Update high score if current score exceeds it
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            self.save_high_score()

        return actual_points

    def reset_score(self):
        """Reset the current score to zero."""
        self.current_score = 0
        self.multiplier = 1.0
        self.combo_count = 0

    def get_score(self) -> int:
        """Get the current score."""
        return self.current_score

    def get_high_score(self) -> int:
        """Get the high score."""
        return self.high_score

    def set_multiplier(self, multiplier: float):
        """
        Set the score multiplier.

        Args:
            multiplier: Score multiplier (must be >= 1.0)
        """
        if multiplier < 1.0:
            raise ValueError("Multiplier must be at least 1.0")
        self.multiplier = multiplier

    def get_multiplier(self) -> float:
        """Get the current score multiplier."""
        return self.multiplier

    def increment_combo(self) -> int:
        """
        Increment combo counter and update multiplier.

        Returns:
            Current combo count
        """
        self.combo_count += 1

        # Increase multiplier every 5 combos
        if self.combo_count % 5 == 0:
            self.multiplier = min(self.multiplier + 0.5, 5.0)  # Cap at 5x

        return self.combo_count

    def reset_combo(self):
        """Reset combo counter and multiplier."""
        self.combo_count = 0
        self.multiplier = 1.0

    def get_combo_count(self) -> int:
        """Get current combo count."""
        return self.combo_count

    def load_high_score(self):
        """Load high score from file."""
        if os.path.exists(self.high_score_file):
            try:
                with open(self.high_score_file, 'r') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
            except (json.JSONDecodeError, IOError):
                self.high_score = 0

    def save_high_score(self):
        """Save high score to file."""
        try:
            with open(self.high_score_file, 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except IOError:
            pass  # Silently fail if we can't save

    def get_score_display(self) -> str:
        """
        Get formatted score string for display.

        Returns:
            Formatted score string
        """
        if self.multiplier > 1.0:
            return f"Score: {self.current_score} (x{self.multiplier:.1f})"
        return f"Score: {self.current_score}"

    def get_stats(self) -> dict:
        """
        Get all score statistics.

        Returns:
            Dictionary containing all score stats
        """
        return {
            'current_score': self.current_score,
            'high_score': self.high_score,
            'multiplier': self.multiplier,
            'combo_count': self.combo_count
        }


class ScoreDisplay:
    """Handles rendering of scores on screen using Pygame."""

    def __init__(self, font_size: int = 36):
        """
        Initialize score display.

        Args:
            font_size: Font size for score display
        """
        self.font_size = font_size
        self.font = None
        self.color = (255, 255, 255)  # White
        self.high_score_color = (255, 215, 0)  # Gold
        self.combo_color = (255, 165, 0)  # Orange

    def initialize_pygame(self, pygame_module):
        """
        Initialize Pygame font.

        Args:
            pygame_module: The pygame module (must be initialized)
        """
        self.font = pygame_module.font.Font(None, self.font_size)

    def render_score(self, surface, score_manager: ScoreManager, position: tuple = (10, 10)):
        """
        Render current score on the screen.

        Args:
            surface: Pygame surface to render on
            score_manager: ScoreManager instance
            position: (x, y) position for score display
        """
        if self.font is None:
            return

        # Render current score
        score_text = score_manager.get_score_display()
        score_surface = self.font.render(score_text, True, self.color)
        surface.blit(score_surface, position)

        # Render high score
        high_score_text = f"High: {score_manager.get_high_score()}"
        high_score_surface = self.font.render(high_score_text, True, self.high_score_color)
        surface.blit(high_score_surface, (position[0], position[1] + 40))

        # Render combo if active
        if score_manager.get_combo_count() > 0:
            combo_text = f"Combo: {score_manager.get_combo_count()}"
            combo_surface = self.font.render(combo_text, True, self.combo_color)
            surface.blit(combo_surface, (position[0], position[1] + 80))

    def set_color(self, color: tuple):
        """
        Set the color for score display.

        Args:
            color: RGB tuple (r, g, b)
        """
        self.color = color
