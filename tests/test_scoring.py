"""
Unit tests for the scoring system.

Tests cover:
- Basic score tracking
- Point addition
- High score management
- Score multipliers
- Combo system
- Score persistence
"""

import pytest
import os
import json
from scoring import ScoreManager, ScoreDisplay


class TestScoreManager:
    """Test cases for ScoreManager class."""

    def test_initialization(self):
        """Test that ScoreManager initializes correctly."""
        score_manager = ScoreManager()
        assert score_manager.get_score() == 0
        assert score_manager.get_multiplier() == 1.0
        assert score_manager.get_combo_count() == 0

    def test_add_points(self):
        """Test adding points to the score."""
        score_manager = ScoreManager()
        score_manager.add_points(100)
        assert score_manager.get_score() == 100

        score_manager.add_points(50)
        assert score_manager.get_score() == 150

    def test_add_points_with_multiplier(self):
        """Test that multipliers correctly affect points."""
        score_manager = ScoreManager()
        score_manager.set_multiplier(2.0)
        actual_points = score_manager.add_points(100)

        assert actual_points == 200
        assert score_manager.get_score() == 200

    def test_add_negative_points_raises_error(self):
        """Test that adding negative points raises ValueError."""
        score_manager = ScoreManager()
        with pytest.raises(ValueError):
            score_manager.add_points(-50)

    def test_reset_score(self):
        """Test that reset_score clears the current score."""
        score_manager = ScoreManager()
        score_manager.add_points(500)
        score_manager.set_multiplier(3.0)
        score_manager.increment_combo()

        score_manager.reset_score()

        assert score_manager.get_score() == 0
        assert score_manager.get_multiplier() == 1.0
        assert score_manager.get_combo_count() == 0

    def test_high_score_updates(self):
        """Test that high score updates when current score exceeds it."""
        score_manager = ScoreManager(high_score_file="test_highscore.json")

        # Clean up any existing test file
        if os.path.exists("test_highscore.json"):
            os.remove("test_highscore.json")

        score_manager.add_points(100)
        assert score_manager.get_high_score() == 100

        score_manager.add_points(200)
        assert score_manager.get_high_score() == 300

        # Reset and verify high score persists
        score_manager.reset_score()
        assert score_manager.get_high_score() == 300
        assert score_manager.get_score() == 0

        # Clean up
        if os.path.exists("test_highscore.json"):
            os.remove("test_highscore.json")

    def test_set_multiplier(self):
        """Test setting score multiplier."""
        score_manager = ScoreManager()
        score_manager.set_multiplier(2.5)
        assert score_manager.get_multiplier() == 2.5

    def test_set_invalid_multiplier(self):
        """Test that invalid multiplier raises ValueError."""
        score_manager = ScoreManager()
        with pytest.raises(ValueError):
            score_manager.set_multiplier(0.5)

    def test_increment_combo(self):
        """Test combo increment and multiplier increase."""
        score_manager = ScoreManager()

        # First 4 combos don't increase multiplier
        for i in range(4):
            combo = score_manager.increment_combo()
            assert combo == i + 1
            assert score_manager.get_multiplier() == 1.0

        # 5th combo increases multiplier
        combo = score_manager.increment_combo()
        assert combo == 5
        assert score_manager.get_multiplier() == 1.5

        # 10th combo increases multiplier again
        for i in range(5):
            score_manager.increment_combo()
        assert score_manager.get_combo_count() == 10
        assert score_manager.get_multiplier() == 2.0

    def test_reset_combo(self):
        """Test that reset_combo clears combo and multiplier."""
        score_manager = ScoreManager()

        for _ in range(5):
            score_manager.increment_combo()

        score_manager.reset_combo()
        assert score_manager.get_combo_count() == 0
        assert score_manager.get_multiplier() == 1.0

    def test_combo_multiplier_cap(self):
        """Test that multiplier caps at 5.0."""
        score_manager = ScoreManager()

        # Increment combo 100 times
        for _ in range(100):
            score_manager.increment_combo()

        # Multiplier should be capped at 5.0
        assert score_manager.get_multiplier() <= 5.0

    def test_get_score_display(self):
        """Test score display string formatting."""
        score_manager = ScoreManager()
        score_manager.add_points(100)

        # Without multiplier
        display = score_manager.get_score_display()
        assert display == "Score: 100"

        # With multiplier
        score_manager.set_multiplier(2.5)
        display = score_manager.get_score_display()
        assert "x2.5" in display

    def test_get_stats(self):
        """Test getting all score statistics."""
        score_manager = ScoreManager()
        score_manager.add_points(100)
        score_manager.set_multiplier(2.0)
        score_manager.increment_combo()

        stats = score_manager.get_stats()

        assert stats['current_score'] == 100
        assert stats['multiplier'] == 2.0
        assert stats['combo_count'] == 1
        assert 'high_score' in stats

    def test_high_score_persistence(self):
        """Test that high scores persist across instances."""
        test_file = "test_persistence.json"

        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

        # Create first instance and set high score
        score_manager1 = ScoreManager(high_score_file=test_file)
        score_manager1.add_points(500)
        assert score_manager1.get_high_score() == 500

        # Create second instance and verify high score loaded
        score_manager2 = ScoreManager(high_score_file=test_file)
        assert score_manager2.get_high_score() == 500

        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

    def test_corrupted_high_score_file(self):
        """Test handling of corrupted high score file."""
        test_file = "test_corrupted.json"

        # Create corrupted file
        with open(test_file, 'w') as f:
            f.write("not valid json {{{")

        # Should handle gracefully
        score_manager = ScoreManager(high_score_file=test_file)
        assert score_manager.get_high_score() == 0

        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

    def test_multiple_score_additions(self):
        """Test adding points multiple times."""
        score_manager = ScoreManager()
        expected_score = 0

        for points in [10, 20, 30, 40, 50]:
            score_manager.add_points(points)
            expected_score += points

        assert score_manager.get_score() == expected_score


class TestScoreDisplay:
    """Test cases for ScoreDisplay class."""

    def test_initialization(self):
        """Test that ScoreDisplay initializes correctly."""
        display = ScoreDisplay(font_size=48)
        assert display.font_size == 48
        assert display.color == (255, 255, 255)

    def test_set_color(self):
        """Test setting display color."""
        display = ScoreDisplay()
        new_color = (255, 0, 0)
        display.set_color(new_color)
        assert display.color == new_color

    def test_initialize_pygame(self):
        """Test Pygame initialization."""
        try:
            import pygame
            pygame.init()

            display = ScoreDisplay()
            display.initialize_pygame(pygame)

            assert display.font is not None

            pygame.quit()
        except ImportError:
            pytest.skip("Pygame not available")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
