import pygame
import random

# Initialize pygame and its mixer for sound
pygame.init()
pygame.mixer.init()

# Define the dimensions of the game window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 400
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Endless Runner")

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()

# Load sound effects (placeholders - replace with actual file paths)
jump_sound = pygame.mixer.Sound('sound/jump_sound.wav')  # First jump sound
double_jump_sound = pygame.mixer.Sound('sound/double_jump_sound.mp3')  # Double jump sound
land_sound = pygame.mixer.Sound('sound/land_sound.mp3')  # Land sound
hit_sound = pygame.mixer.Sound('sound/hit_sound.mp3')  # Obstacle hit sound
game_over_sound = pygame.mixer.Sound('sound/gameover_sound.wav')  # Game over sound
background_music = 'sound/background_music.mp3'  # Background music

# Function to start background music
def start_background_music():
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)  # Loop the background music indefinitely

# Start background music at game start
start_background_music()

# Define player properties
player_width, player_height = 50, 50
player_x = 100
player_y = WINDOW_HEIGHT - player_height - 50  # Starting position
player_velocity_y = 0  # For jumping
gravity = 0.5
jumps_left = 2  # Allow double jump

# Ground level to compare jump heights
ground_y = WINDOW_HEIGHT - player_height - 50

# Variable to track the maximum jump height
max_jump_height = player_y

# Define obstacle properties
obstacle_width, obstacle_height = 50, 50
obstacle_x = WINDOW_WIDTH
obstacle_y = WINDOW_HEIGHT - obstacle_height - 50
obstacle_speed = 5

# List to hold sky obstacles
sky_obstacles = []
sky_obstacle_chance = 0.0  # Start with no sky obstacles

# Initialize the score
score = 0

# Difficulty levels
difficulty_levels = [
    {"name": "Easy", "speed": 5, "sky_obstacles": False, "ground_obstacle_count": 1},
    {"name": "Medium", "speed": 7, "sky_obstacles": False, "ground_obstacle_count": 2},
    {"name": "Hard", "speed": 10, "sky_obstacles": True, "ground_obstacle_count": 3},
    {"name": "Insane", "speed": 12, "sky_obstacles": True, "ground_obstacle_count": 4},
]
current_difficulty = 0  # Start at Easy

# Player's lives
lives = 3

# Load heart image to represent lives (replace with actual file path)
heart_img = pygame.image.load('images/heart.png')
heart_img = pygame.transform.scale(heart_img, (30, 30))  # Resize hearts

# Font setup
font = pygame.font.Font(None, 36)

# Function to reset game state
def reset_game():
    global player_y, player_velocity_y, jumps_left, obstacle_x, obstacle_speed, score, max_jump_height, sky_obstacles, current_difficulty, lives
    player_y = WINDOW_HEIGHT - player_height - 50  # Reset player position
    player_velocity_y = 0
    jumps_left = 2  # Reset jumps
    obstacle_x = WINDOW_WIDTH  # Reset obstacle position
    obstacle_speed = difficulty_levels[current_difficulty]["speed"]  # Set initial speed
    score = 0  # Reset score
    max_jump_height = player_y  # Reset max jump height
    sky_obstacles = []  # Clear sky obstacles
    current_difficulty = 0  # Reset difficulty to Easy
    lives = 3  # Reset lives
    start_background_music()  # Restart background music

# Function to display the game-over screen and wait for restart
def game_over_screen():
    window.fill((0, 0, 0))  # Fill the screen with black
    
    # Render game over text
    game_over_text = font.render(f"Game Over! You scored {score}", True, (255, 255, 255))
    restart_text = font.render("Press R to Restart", True, (255, 255, 255))
    
    # Position the texts
    window.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 50))
    window.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2))
    
    pygame.display.update()

    # Play game over sound
    pygame.mixer.Sound.play(game_over_sound)

    # Stop the background music on game over
    pygame.mixer.music.stop()

    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()  # Reset game state
                restart = True

# Function to draw lives as hearts
def draw_lives():
    for i in range(lives):
        window.blit(heart_img, (10 + i * 35, 40))  # Spacing between hearts

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Check for jump and allow double jump
            if event.key == pygame.K_SPACE:
                if player_y == ground_y or jumps_left > 0:
                    if jumps_left == 2 or player_y == ground_y:  # First jump
                        player_velocity_y = -10  # Initial jump velocity
                        pygame.mixer.Sound.play(jump_sound)  # Play jump sound
                    elif jumps_left == 1:  # Second jump
                        player_velocity_y = -12  # Stronger double jump velocity
                        pygame.mixer.Sound.play(double_jump_sound)  # Play double jump sound
                    jumps_left -= 1  # Reduce the number of available jumps

    # Apply gravity
    player_y += player_velocity_y
    player_velocity_y += gravity

    # Track the maximum jump height
    if player_y < max_jump_height:
        max_jump_height = player_y  # Update maximum height reached

    # Prevent player from falling below the ground
    if player_y >= ground_y:
        if player_velocity_y != 0:  # If player was falling and lands
            pygame.mixer.Sound.play(land_sound)  # Play landing sound
        player_y = ground_y
        player_velocity_y = 0
        jumps_left = 2  # Reset jump count when player hits the ground
        max_jump_height = player_y  # Reset maximum height when player hits the ground

    # Move the ground obstacle left
    obstacle_x -= obstacle_speed

    # Respawn the ground obstacle with random sizes once it goes off-screen
    if obstacle_x < -obstacle_width:
        obstacle_x = WINDOW_WIDTH
        obstacle_width = random.randint(30, 80)  # Random obstacle width
        obstacle_height = random.randint(30, 80)  # Random obstacle height
        obstacle_y = WINDOW_HEIGHT - obstacle_height - 50
        score += 1

        # Increase difficulty based on score
        if score >= 10 and current_difficulty == 0:
            current_difficulty = 1
            obstacle_speed = difficulty_levels[current_difficulty]["speed"]
        elif score >= 20 and current_difficulty == 1:
            current_difficulty = 2
            obstacle_speed = difficulty_levels[current_difficulty]["speed"]
        elif score >= 30 and current_difficulty == 2:
            current_difficulty = 3
            obstacle_speed = difficulty_levels[current_difficulty]["speed"]

    # Adjust sky obstacle chance based on difficulty
    if difficulty_levels[current_difficulty]["sky_obstacles"]:
        sky_obstacle_chance = 0.01  # Probability of spawning a sky obstacle each frame
    else:
        sky_obstacle_chance = 0.0  # No sky obstacles in lower difficulties

    # Randomly spawn a sky obstacle with some probability
    if random.random() < sky_obstacle_chance:
        sky_obstacle_x = WINDOW_WIDTH
        sky_obstacle_y = random.randint(160, 240)  # Random height for the sky obstacle
        sky_obstacle_width = random.randint(30, 50)
        sky_obstacle_height = random.randint(30, 50)
        sky_obstacles.append([sky_obstacle_x, sky_obstacle_y, sky_obstacle_width, sky_obstacle_height])

    # Move and remove sky obstacles
    for sky_obstacle in sky_obstacles[:]:
        sky_obstacle[0] -= obstacle_speed  # Move left with obstacle speed
        if sky_obstacle[0] < -sky_obstacle[2]:  # If off-screen, remove
            sky_obstacles.remove(sky_obstacle)

    # Check for collision with ground obstacle
    if player_x < obstacle_x + obstacle_width and player_x + player_width > obstacle_x:
        if player_y + player_height > obstacle_y:
            pygame.mixer.Sound.play(hit_sound)  # Play hit sound
            obstacle_x = WINDOW_WIDTH  # Reset obstacle position
            lives -= 1  # Lose a life
            if lives == 0:  # Check for game over
                game_over_screen()

    # Check for collision with sky obstacles
    for sky_obstacle in sky_obstacles[:]:
        if player_x < sky_obstacle[0] + sky_obstacle[2] and player_x + player_width > sky_obstacle[0]:
            if player_y < sky_obstacle[1] + sky_obstacle[3] and player_y + player_height > sky_obstacle[1]:
                pygame.mixer.Sound.play(hit_sound)  # Play hit sound
                sky_obstacles.remove(sky_obstacle)  # Remove the hit obstacle
                lives -= 1  # Lose a life
                if lives == 0:  # Check for game over
                    game_over_screen()

    # Fill the window with a background color (light blue)
    window.fill((135, 206, 235))

    # Draw the player (red rectangle)
    pygame.draw.rect(window, (255, 0, 0), (player_x, player_y, player_width, player_height))

    # Draw the ground obstacle (green rectangle)
    pygame.draw.rect(window, (0, 255, 0), (obstacle_x, obstacle_y, obstacle_width, obstacle_height))

    # Draw the sky obstacles (yellow rectangles)
    for sky_obstacle in sky_obstacles:
        pygame.draw.rect(window, (255, 255, 0), (sky_obstacle[0], sky_obstacle[1], sky_obstacle[2], sky_obstacle[3]))

    # Display the score in the top left corner
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    window.blit(score_text, (10, 10))

    # Draw the player's lives
    draw_lives()

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(60)

# Quit the game after the loop ends
pygame.quit()
