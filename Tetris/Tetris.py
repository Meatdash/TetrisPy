import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
background_color = BLACK
Music = pygame.mixer.music

# Setup the Music

songs = ["Alan Walker The Spectre.mp3", "Breaking Bad Theme Trap Remix.mp3", "Tetris Theme Song.mp3"]

Music.load(random.choice(songs))
Music.play(-1)


# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 1, 1]],
]

# Tetrimino colors
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
          (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 128, 128)]

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")


# Initialize variables
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
current_shape = None
current_color = None
current_x, current_y = 0, 0
score = 0

# Functions
def draw_grid(surface, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, COLORS[cell - 1], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_tetrimino(surface, shape, x, y, color):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                pygame.draw.rect(surface, COLORS[color - 1], ((x + col) * GRID_SIZE, (y + row) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def new_tetrimino():
    global current_shape, current_color, current_x, current_y
    current_shape = random.choice(SHAPES)
    current_color = random.randint(1, len(COLORS))
    current_x = GRID_WIDTH // 2 - len(current_shape[0]) // 4
    current_y = 0

def can_move(shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                if (x + col < 0 or x + col >= GRID_WIDTH or
                    y + row >= GRID_HEIGHT or
                    grid[y + row][x + col]):
                    return False
    return True

def merge_shape(shape, x, y, color):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                grid[y + row][x + col] = color

def check_lines():
    global score
    lines_to_clear = [i for i, row in enumerate(grid) if all(row)]
    for line in lines_to_clear:
        grid.pop(line)
        grid.insert(0, [0] * GRID_WIDTH)
        score += 100 * len(lines_to_clear)

def game_over_screen(score):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    game_over_text = font.render(f"Game Over - Score: {score}", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    restart_text = font.render("Press R to Restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()

def restart_game():
    Music.load(random.choice(songs))
    Music.play(-1)
    global grid, current_shape, current_color, current_x, current_y, score, game_over
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    current_shape = None
    current_color = None
    current_x, current_y = 0, 0
    score = 0
    game_over = False
    new_tetrimino()



# Game loop
clock = pygame.time.Clock()
fall_speed = 0.2  # Initial falling speed
game_over = False
target_fps = 60

# Constants for fixed time step
delta_time = 1 / target_fps
accumulator = 0.0

new_tetrimino()
while not game_over:
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            fall_speed = 0.2 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if can_move(current_shape, current_x - 1, current_y):
                        current_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if can_move(current_shape, current_x + 1, current_y):
                        current_x += 1
                elif event.key == pygame.K_DOWN:
                    if can_move(current_shape, current_x, current_y + 1):
                        current_y += 1
                        fall_speed = 0.1 
                elif event.key == pygame.K_UP:
                    rotated_shape = [list(row) for row in zip(*reversed(current_shape))]
                    if can_move(rotated_shape, current_x, current_y):
                        current_shape = rotated_shape

        accumulator += delta_time

        # Move the tetrimino down when it's time to do so
        if accumulator >= fall_speed:
            if can_move(current_shape, current_x, current_y + 1):
                current_y += 1
            else:
                merge_shape(current_shape, current_x, current_y, current_color)
                check_lines()
                new_tetrimino()
            accumulator = 0.0

        # Clear the screen
        screen.fill(BLACK)

        # Draw the grid
        draw_grid(screen, grid)

        # Draw the current tetrimino
        draw_tetrimino(screen, current_shape, current_x, current_y, current_color)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(target_fps)


    # Game over screen
    game_over_screen(score)


    # Wait for a key press to exit

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                    waiting = False


# Quit Pygame
pygame.quit()
