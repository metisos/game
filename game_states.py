"""
Game states module.

This module handles:
- Game state management (menu, playing, game over, paused)
- Game over screen
- Menu screens
"""

import pygame
from typing import Tuple, Optional


class GameState:
    """Base class for game states."""

    def __init__(self, game):
        """
        Initialize game state.

        Args:
            game: Reference to main game instance
        """
        self.game = game

    def handle_events(self, events):
        """Handle events for this state."""
        pass

    def update(self):
        """Update state logic."""
        pass

    def render(self, surface):
        """Render state graphics."""
        pass


class GameOverState(GameState):
    """Game over screen state."""

    def __init__(self, game, final_score: int, high_score: int):
        """
        Initialize game over state.

        Args:
            game: Reference to main game
            final_score: Player's final score
            high_score: High score
        """
        super().__init__(game)
        self.final_score = final_score
        self.high_score = high_score
        self.is_new_high_score = final_score >= high_score

        # UI elements
        self.title_font = pygame.font.Font(None, 72)
        self.text_font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 32)

        # Colors
        self.bg_color = (0, 0, 50)
        self.title_color = (255, 50, 50)
        self.text_color = (255, 255, 255)
        self.high_score_color = (255, 215, 0)
        self.button_color = (100, 100, 200)
        self.button_hover_color = (150, 150, 255)

        # Button rects
        self.restart_button = pygame.Rect(0, 0, 200, 50)
        self.quit_button = pygame.Rect(0, 0, 200, 50)

        self.hovered_button = None

    def handle_events(self, events):
        """Handle game over screen events."""
        mouse_pos = pygame.mouse.get_pos()

        # Check button hover
        if self.restart_button.collidepoint(mouse_pos):
            self.hovered_button = "restart"
        elif self.quit_button.collidepoint(mouse_pos):
            self.hovered_button = "quit"
        else:
            self.hovered_button = None

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart game
                    return "restart"
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    # Quit game
                    return "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.restart_button.collidepoint(mouse_pos):
                        return "restart"
                    elif self.quit_button.collidepoint(mouse_pos):
                        return "quit"

        return None

    def render(self, surface):
        """Render game over screen."""
        screen_width = surface.get_width()
        screen_height = surface.get_height()

        # Clear screen
        surface.fill(self.bg_color)

        # Render title
        title_text = "GAME OVER"
        title_surface = self.title_font.render(title_text, True, self.title_color)
        title_rect = title_surface.get_rect(center=(screen_width // 2, 100))
        surface.blit(title_surface, title_rect)

        # Render final score
        score_text = f"Final Score: {self.final_score}"
        score_surface = self.text_font.render(score_text, True, self.text_color)
        score_rect = score_surface.get_rect(center=(screen_width // 2, 200))
        surface.blit(score_surface, score_rect)

        # Render high score
        if self.is_new_high_score:
            high_score_text = "NEW HIGH SCORE!"
            color = self.high_score_color
        else:
            high_score_text = f"High Score: {self.high_score}"
            color = self.text_color

        high_score_surface = self.text_font.render(high_score_text, True, color)
        high_score_rect = high_score_surface.get_rect(center=(screen_width // 2, 250))
        surface.blit(high_score_surface, high_score_rect)

        # Position buttons
        self.restart_button.center = (screen_width // 2, 350)
        self.quit_button.center = (screen_width // 2, 420)

        # Render restart button
        restart_color = self.button_hover_color if self.hovered_button == "restart" else self.button_color
        pygame.draw.rect(surface, restart_color, self.restart_button, border_radius=10)
        restart_text = self.button_font.render("Restart (R)", True, self.text_color)
        restart_rect = restart_text.get_rect(center=self.restart_button.center)
        surface.blit(restart_text, restart_rect)

        # Render quit button
        quit_color = self.button_hover_color if self.hovered_button == "quit" else self.button_color
        pygame.draw.rect(surface, quit_color, self.quit_button, border_radius=10)
        quit_text = self.button_font.render("Quit (Q)", True, self.text_color)
        quit_rect = quit_text.get_rect(center=self.quit_button.center)
        surface.blit(quit_text, quit_rect)

        # Render instructions
        instructions = [
            "Press R to restart",
            "Press Q or ESC to quit",
            "Click buttons to select"
        ]

        y_offset = 500
        for instruction in instructions:
            inst_surface = pygame.font.Font(None, 20).render(instruction, True, (150, 150, 150))
            inst_rect = inst_surface.get_rect(center=(screen_width // 2, y_offset))
            surface.blit(inst_surface, inst_rect)
            y_offset += 25


class PauseState(GameState):
    """Pause screen state."""

    def __init__(self, game):
        """Initialize pause state."""
        super().__init__(game)
        self.font = pygame.font.Font(None, 72)
        self.text_font = pygame.font.Font(None, 36)

    def handle_events(self, events):
        """Handle pause screen events."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    return "resume"
                elif event.key == pygame.K_q:
                    return "quit"
        return None

    def render(self, surface):
        """Render pause screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface(surface.get_size())
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        # Paused text
        text = "PAUSED"
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 50))
        surface.blit(text_surface, text_rect)

        # Instructions
        instructions = [
            "Press P or ESC to resume",
            "Press Q to quit"
        ]

        y_offset = surface.get_height() // 2 + 50
        for instruction in instructions:
            inst_surface = self.text_font.render(instruction, True, (200, 200, 200))
            inst_rect = inst_surface.get_rect(center=(surface.get_width() // 2, y_offset))
            surface.blit(inst_surface, inst_rect)
            y_offset += 50


class GameStateManager:
    """Manages game state transitions."""

    def __init__(self):
        """Initialize state manager."""
        self.current_state = None
        self.states = {}

    def add_state(self, name: str, state: GameState):
        """
        Add a state to the manager.

        Args:
            name: State name
            state: GameState instance
        """
        self.states[name] = state

    def set_state(self, name: str):
        """
        Change to a different state.

        Args:
            name: Name of state to switch to
        """
        if name in self.states:
            self.current_state = self.states[name]

    def get_state(self) -> Optional[GameState]:
        """Get current state."""
        return self.current_state

    def handle_events(self, events):
        """Handle events for current state."""
        if self.current_state:
            return self.current_state.handle_events(events)
        return None

    def update(self):
        """Update current state."""
        if self.current_state:
            self.current_state.update()

    def render(self, surface):
        """Render current state."""
        if self.current_state:
            self.current_state.render(surface)
