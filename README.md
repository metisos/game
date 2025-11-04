# Space Shooter Game

A complete pygame-based space shooter with advanced features including player movement, shooting mechanics, intelligent enemy AI, scoring system with combos, and game state management.

## 🎮 Features

### Core Gameplay
- **Smooth Player Movement**: WASD or Arrow key controls with diagonal movement normalization
- **Auto-Fire Weapon System**: Hold SPACE to continuously shoot with configurable fire rates
- **Smart Enemy AI**: Multiple movement patterns (vertical, horizontal, chase, zigzag)
- **Dynamic Spawning**: Configurable enemy spawn rates and maximum enemy counts
- **Health System**: 3 health points with invulnerability frames after taking damage
- **Pause System**: Press P or ESC to pause/resume gameplay

### Scoring System
- **Point Tracking**: Score points by destroying enemies
- **Combo System**: Chain kills to build combos and increase your score multiplier
- **Score Multipliers**: Every 5 combos increases multiplier by 0.5x (capped at 5x)
- **High Score Persistence**: Automatically saves and loads high scores
- **Real-time Display**: Current score, multiplier, combo count, and health displayed during gameplay

### Game States
- **Playing**: Main gameplay with all features active
- **Paused**: Semi-transparent overlay with resume/quit options
- **Game Over**: Final score display, high score tracking, restart or quit options

## 🚀 Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python game.py
```

## 🎯 Controls

| Input | Action |
|-------|--------|
| **WASD** or **Arrow Keys** | Move player |
| **SPACE** | Shoot (hold for auto-fire) |
| **P** or **ESC** | Pause/Unpause |
| **R** | Restart (game over screen) |
| **Q** | Quit (game over/pause screen) |

## 🧪 Running Tests

Run all 92 unit tests:
```bash
pytest tests/ -v
```

Run with coverage report:
```bash
pytest tests/ -v --cov=. --cov-report=html
```

### Test Coverage
- **92 tests total** (100% passing)
- `test_scoring.py`: 19 tests - Scoring system
- `test_player.py`: 14 tests - Player movement and controls
- `test_enemy.py`: 19 tests - Enemy AI and spawning
- `test_projectile.py`: 24 tests - Shooting mechanics
- `test_game_states.py`: 16 tests - Game state management

## 📁 Project Structure

```
game/
├── game.py              # Main game loop and integration
├── player.py            # Player class and controller
├── enemy.py             # Enemy AI and spawner
├── projectile.py        # Projectile, weapon, and auto-fire systems
├── scoring.py           # Score manager and display
├── game_states.py       # Game state management (pause, game over)
├── requirements.txt     # Python dependencies
├── highscore.json       # Persistent high score storage
└── tests/
    ├── test_player.py
    ├── test_enemy.py
    ├── test_projectile.py
    ├── test_scoring.py
    └── test_game_states.py
```

## 🏗️ Architecture

### Modular Design
Each major system is implemented in its own module with well-defined interfaces:

- **player.py**: Player sprite, movement mechanics, input handling
- **enemy.py**: Enemy sprites, AI patterns, collision detection, spawning
- **projectile.py**: Projectiles, weapons, fire rate management, auto-fire
- **scoring.py**: Score tracking, combos, multipliers, persistence, display
- **game_states.py**: State machine for game/pause/game-over states
- **game.py**: Main integration bringing all systems together

### Key Classes

#### Player System
- `Player`: Pygame sprite with movement and boundaries
- `PlayerController`: Handles input with diagonal movement normalization

#### Enemy System
- `Enemy`: AI-controlled enemy sprite with multiple movement patterns
- `EnemySpawner`: Manages enemy creation and spawn timing

#### Projectile System
- `Projectile`: Bullet sprite with direction and speed
- `Weapon`: Fire rate management and cooldown system
- `ProjectileManager`: Organizes player and enemy projectiles
- `AutoFire`: Continuous firing controller

#### Scoring System
- `ScoreManager`: Point tracking, combos, multipliers, persistence
- `ScoreDisplay`: Pygame rendering of score information

#### Game States
- `GameOverState`: End screen with restart/quit
- `PauseState`: Pause overlay with resume/quit
- `GameStateManager`: State transition management

## 🎮 Gameplay Tips

1. **Build Combos**: Destroy enemies quickly in succession to build your combo multiplier
2. **Avoid Damage**: Taking damage resets your combo and multiplier
3. **Use Movement**: Diagonal movement is normalized for consistent speed
4. **Chase Enemies**: Some enemies will follow you - use this to your advantage
5. **Watch Spawn Patterns**: Enemies spawn from the top with various movement patterns

## 🔧 Development

### Adding New Enemy Patterns
Add a new pattern to `enemy.py`:
```python
def _move_new_pattern(self):
    """Your custom movement pattern."""
    # Implement movement logic
    self.velocity_x = ...
    self.velocity_y = ...
```

### Adjusting Difficulty
Modify spawn rates and enemy counts in `game.py`:
```python
self.enemy_spawner = EnemySpawner(
    self.width,
    self.height,
    spawn_rate=90,    # Lower = more frequent spawns
    max_enemies=8     # Higher = more enemies on screen
)
```

### Customizing Scoring
Adjust scoring parameters in `game.py`:
```python
self.score_manager.add_points(100)  # Points per enemy kill
```

## 📊 Technical Details

- **Language**: Python 3.11+
- **Game Engine**: Pygame 2.5.2
- **Testing**: Pytest 7.4.3
- **Architecture**: Object-oriented with sprite-based collision detection
- **Frame Rate**: 60 FPS
- **Resolution**: 800x600 (configurable)

## 🐛 Known Issues

- No sound effects or music yet (planned feature)
- No graphics/sprites yet - using colored rectangles (planned feature)
- Controller support implemented but not fully tested

## 🚧 Future Enhancements

- Add sound effects and background music
- Create sprite graphics for player, enemies, and projectiles
- Implement power-ups and special weapons
- Add more enemy types and boss battles
- Create multiple levels with increasing difficulty
- Add particle effects for explosions
- Implement a main menu and settings screen

## 📝 License

This project was developed as part of the tickets-gen automated development system.

## 🤝 Contributing

This game was built through an automated ticketing system. See the commit history for the complete development process including:
- Scoring System implementation
- Player Movement system
- Shooting Mechanics
- Enemy AI with multiple patterns
- Game Over and Pause screens
- Comprehensive test suite
