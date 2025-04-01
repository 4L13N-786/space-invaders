# Space Invaders Game

A modern Python implementation of the classic Space Invaders arcade game using Pygame.

## Features

- Classic Space Invaders gameplay with player movement and shooting
- Multiple alien types with different point values
- Obstacles that can be destroyed by both player and alien lasers
- Extra aliens that fly across the top of the screen for bonus points
- Lives system and score tracking
- CRT-style visual effect for retro feel
- Sound effects for lasers and explosions
- Victory condition when all aliens are defeated

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Clone this repository or download the source files
2. Ensure you have Python installed
3. Install Pygame:

## How to Play

- Use **LEFT/RIGHT arrow keys** or **A/D** to move your spaceship
- Press **SPACEBAR** to shoot lasers
- Destroy aliens to earn points:
- Red aliens: 100 points
- Green aliens: 200 points
- Yellow aliens: 300 points
- Extra aliens: 500 points
- Avoid alien lasers and collisions with aliens
- You have 3 lives - lose them all and the game ends
- Destroy all aliens to win!

## File Structure

- `main.py`: Main game loop and logic
- `player.py`: Player spaceship class
- `alien.py`: Alien and Extra alien classes
- `laser.py`: Laser projectile class
- `obstacle.py`: Obstacle/barrier classes
- `graphics/`: Contains all image assets
- `audio/`: Contains all sound effects
- `font/`: Contains game font

## Customisation

You can modify:
- Game difficulty by adjusting alien movement speed
- Player laser cooldown time
- Alien laser frequency
- Screen size in `main.py`

## Credits

Created with Pygame. Sound effects and graphics can be replaced with your own assets.

Enjoy the game!
