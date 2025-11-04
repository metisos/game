"""
Unit tests for the game states module.

Tests cover:
- Game over state
- Pause state
- State transitions
- State rendering
"""

import pytest
import pygame
from game_states import GameOverState, PauseState, GameStateManager


@pytest.fixture
def pygame_init():
    """Initialize pygame before tests."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_game():
    """Create a mock game object."""
    class MockGame:
        def __init__(self):
            self.width = 800
            self.height = 600

    return MockGame()


class TestGameOverState:
    """Test cases for GameOverState class."""

    def test_initialization(self, pygame_init, mock_game):
        """Test game over state initializes correctly."""
        state = GameOverState(mock_game, final_score=1000, high_score=500)

        assert state.final_score == 1000
        assert state.high_score == 500
        assert state.is_new_high_score is True

    def test_not_new_high_score(self, pygame_init, mock_game):
        """Test detection of non-new high score."""
        state = GameOverState(mock_game, final_score=300, high_score=500)

        assert state.is_new_high_score is False

    def test_handle_restart_key(self, pygame_init, mock_game):
        """Test handling restart key press."""
        state = GameOverState(mock_game, final_score=100, high_score=100)

        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_r})
        result = state.handle_events([event])

        assert result == "restart"

    def test_handle_quit_key(self, pygame_init, mock_game):
        """Test handling quit key press."""
        state = GameOverState(mock_game, final_score=100, high_score=100)

        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_q})
        result = state.handle_events([event])

        assert result == "quit"

    def test_render_creates_surface(self, pygame_init, mock_game):
        """Test that render doesn't crash."""
        state = GameOverState(mock_game, final_score=100, high_score=100)
        surface = pygame.Surface((800, 600))

        # Should not raise exception
        state.render(surface)


class TestPauseState:
    """Test cases for PauseState class."""

    def test_initialization(self, pygame_init, mock_game):
        """Test pause state initializes correctly."""
        state = PauseState(mock_game)

        assert state.game == mock_game

    def test_handle_resume_key(self, pygame_init, mock_game):
        """Test handling resume key press."""
        state = PauseState(mock_game)

        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_p})
        result = state.handle_events([event])

        assert result == "resume"

    def test_handle_escape_key(self, pygame_init, mock_game):
        """Test handling escape key press."""
        state = PauseState(mock_game)

        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
        result = state.handle_events([event])

        assert result == "resume"

    def test_handle_quit_key(self, pygame_init, mock_game):
        """Test handling quit key press."""
        state = PauseState(mock_game)

        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_q})
        result = state.handle_events([event])

        assert result == "quit"

    def test_render_creates_surface(self, pygame_init, mock_game):
        """Test that render doesn't crash."""
        state = PauseState(mock_game)
        surface = pygame.Surface((800, 600))

        # Should not raise exception
        state.render(surface)


class TestGameStateManager:
    """Test cases for GameStateManager class."""

    def test_initialization(self, pygame_init):
        """Test state manager initializes correctly."""
        manager = GameStateManager()

        assert manager.current_state is None
        assert len(manager.states) == 0

    def test_add_state(self, pygame_init, mock_game):
        """Test adding a state."""
        manager = GameStateManager()
        state = PauseState(mock_game)

        manager.add_state("pause", state)

        assert "pause" in manager.states
        assert manager.states["pause"] == state

    def test_set_state(self, pygame_init, mock_game):
        """Test setting current state."""
        manager = GameStateManager()
        state = PauseState(mock_game)

        manager.add_state("pause", state)
        manager.set_state("pause")

        assert manager.current_state == state

    def test_get_state(self, pygame_init, mock_game):
        """Test getting current state."""
        manager = GameStateManager()
        state = PauseState(mock_game)

        manager.add_state("pause", state)
        manager.set_state("pause")

        assert manager.get_state() == state

    def test_handle_events_with_state(self, pygame_init, mock_game):
        """Test handling events when state is set."""
        manager = GameStateManager()
        state = PauseState(mock_game)

        manager.add_state("pause", state)
        manager.set_state("pause")

        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_p})
        result = manager.handle_events([event])

        assert result == "resume"

    def test_handle_events_without_state(self, pygame_init):
        """Test handling events when no state is set."""
        manager = GameStateManager()

        result = manager.handle_events([])

        assert result is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
