import pygame
import sys
import random
import tkinter as tk
from tkinter import messagebox

# Initialize Pygame
pygame.init()

# Constants for screen dimensions and colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5
PLAYER_LEVEL = 1
BULLET_SPEED = 7
DAMAGE_PER_LEVEL = 2
PLAYER_HEALTH = 20
PLAYER_EXP = 0
EXP_TO_LEVEL_UP = 20
JUMP_STRENGTH = 15
GRAVITY = 1

# Ask the user if they want fullscreen or windowed mode using a popup window
def select_display_mode():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    mode = tk.StringVar()
    
    def on_confirm():
        root.quit()
        root.destroy()

    popup = tk.Toplevel()
    popup.title("Select Display Mode")
    
    tk.Label(popup, text="Select Display Mode:").pack(pady=10)
    fullscreen_checkbox = tk.Checkbutton(popup, text="Fullscreen", variable=mode, onvalue='fullscreen', offvalue='')
    fullscreen_checkbox.pack(anchor="w")
    windowed_checkbox = tk.Checkbutton(popup, text="Windowed", variable=mode, onvalue='windowed', offvalue='')
    windowed_checkbox.pack(anchor="w")
    full_screen_windowed_checkbox = tk.Checkbutton(popup, text="Full Screen Windowed", variable=mode, onvalue='full_windowed', offvalue='')
    full_screen_windowed_checkbox.pack(anchor="w")
    
    confirm_button = tk.Button(popup, text="Confirm", command=on_confirm)
    confirm_button.pack(pady=10)
    
    root.mainloop()
    return mode.get()

# Get the display mode selected by the user
mode = select_display_mode()

if mode == 'fullscreen':
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
elif mode == 'full_windowed':
    screen = pygame.display.set_mode((0, 0))  # Fullscreen windowed without being true fullscreen
elif mode == 'windowed':
    screen = pygame.display.set_mode((800, 600))
else:
    print("Invalid input, defaulting to windowed mode.")
    screen = pygame.display.set_mode((800, 600))

SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Side Scroller Game UI")

# Character customization settings
available_colors = [RED, GREEN, BLUE, YELLOW]
current_color_index = 0
PLAYER_COLOR = available_colors[current_color_index]

# Create the player object
player_x = 100
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 50
player_velocity_y = 0
is_jumping = False

# Enemy settings
enemy_x = SCREEN_WIDTH - 150
enemy_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 50
enemy_health = random.randint(1, 100)
ENEMY_BULLET_SPEED = 5
ENEMY_SHOOT_INTERVAL = 1000  # Milliseconds between enemy shots
last_enemy_shot_time = pygame.time.get_ticks()

# Bullets list
bullets = []
enemy_bullets = []

# Game loop variables
clock = pygame.time.Clock()
in_customization_screen = True

def restart_game():
    global player_x, player_y, player_velocity_y, PLAYER_HEALTH, PLAYER_LEVEL, PLAYER_EXP, enemy_health, bullets, enemy_bullets, is_jumping
    player_x = 100
    player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 50
    player_velocity_y = 0
    PLAYER_HEALTH = 20
    PLAYER_LEVEL = 1
    PLAYER_EXP = 0
    enemy_health = random.randint(1, 100)
    bullets = []
    enemy_bullets = []
    is_jumping = False

# Load 8-bit character sprite (a simple 8-bit style humanoid figure)
SPRITE_SIZE = 50
character_sprites = {
    RED: pygame.Surface((SPRITE_SIZE, SPRITE_SIZE)),
    GREEN: pygame.Surface((SPRITE_SIZE, SPRITE_SIZE)),
    BLUE: pygame.Surface((SPRITE_SIZE, SPRITE_SIZE)),
    YELLOW: pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
}
for color, surface in character_sprites.items():
    surface.fill(WHITE)
    pygame.draw.rect(surface, color, (10, 10, 30, 30))  # Basic 8-bit character look
    pygame.draw.rect(surface, (0, 0, 0), (18, 5, 4, 4))  # Eyes
    pygame.draw.rect(surface, (0, 0, 0), (28, 5, 4, 4))  # Eyes
    pygame.draw.rect(surface, (255, 224, 189), (15, 25, 20, 10))  # Face

# Character customization screen
def character_customization():
    global current_color_index, PLAYER_COLOR
    customization_running = True
    while customization_running:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text = font.render("Character Customization: Press Left/Right to change color, Enter to confirm", True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(text, text_rect)

        # Display the current character color
        character_sprite = character_sprites[available_colors[current_color_index]]
        screen.blit(character_sprite, (SCREEN_WIDTH // 2 - SPRITE_SIZE // 2, SCREEN_HEIGHT // 2 - SPRITE_SIZE // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_color_index = (current_color_index - 1) % len(available_colors)
                elif event.key == pygame.K_RIGHT:
                    current_color_index = (current_color_index + 1) % len(available_colors)
                elif event.key == pygame.K_RETURN:
                    PLAYER_COLOR = available_colors[current_color_index]
                    customization_running = False

# Main game loop
character_customization()
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_SPACE:
                # Shoot a bullet
                bullet = pygame.Rect(player_x + SPRITE_SIZE, player_y + SPRITE_SIZE // 2 - 5, 10, 10)
                bullets.append(bullet)
            elif event.key == pygame.K_UP and not is_jumping:
                # Start jump
                is_jumping = True
                player_velocity_y = -JUMP_STRENGTH
            elif PLAYER_HEALTH <= 0:
                if event.key == pygame.K_r:  # Restart game
                    restart_game()
                elif event.key == pygame.K_ESCAPE:  # Exit game
                    pygame.quit()
                    sys.exit()

    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_x += PLAYER_SPEED

    # Apply gravity
    if is_jumping:
        player_velocity_y += GRAVITY
        player_y += player_velocity_y
        # Stop jump when player lands
        if player_y >= SCREEN_HEIGHT - PLAYER_HEIGHT - 50:
            player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 50
            is_jumping = False

    # Keep the player within the screen bounds
    player_x = max(0, min(SCREEN_WIDTH - SPRITE_SIZE, player_x))

    # Update bullets
    for bullet in bullets[:]:
        bullet.x += BULLET_SPEED
        if bullet.colliderect(pygame.Rect(enemy_x, enemy_y, SPRITE_SIZE, SPRITE_SIZE)):
            bullets.remove(bullet)
            enemy_health -= PLAYER_LEVEL * DAMAGE_PER_LEVEL
            if enemy_health <= 0:
                enemy_health = 0
                # Award random EXP when enemy is defeated
                exp_gained = random.randint(1, 10)
                PLAYER_EXP += exp_gained
                if PLAYER_EXP >= EXP_TO_LEVEL_UP:
                    PLAYER_LEVEL += 1
                    PLAYER_HEALTH += 5
                    PLAYER_HEALTH = min(PLAYER_HEALTH, 20 + 5 * (PLAYER_LEVEL - 1))
                    PLAYER_EXP -= EXP_TO_LEVEL_UP
                # Respawn enemy with random health
                enemy_health = random.randint(1, 100)
        elif bullet.x > SCREEN_WIDTH:
            bullets.remove(bullet)

    # Enemy shooting
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_shot_time > ENEMY_SHOOT_INTERVAL:
        enemy_bullet = pygame.Rect(enemy_x, enemy_y + SPRITE_SIZE // 2 - 5, 10, 10)
        enemy_bullets.append(enemy_bullet)
        last_enemy_shot_time = current_time

    # Update enemy bullets
    for enemy_bullet in enemy_bullets[:]:
        enemy_bullet.x -= ENEMY_BULLET_SPEED
        if enemy_bullet.colliderect(pygame.Rect(player_x, player_y, SPRITE_SIZE, SPRITE_SIZE)):
            enemy_bullets.remove(enemy_bullet)
            PLAYER_HEALTH -= 1
            if PLAYER_HEALTH <= 0:
                PLAYER_HEALTH = 0
        elif enemy_bullet.x < 0:
            enemy_bullets.remove(enemy_bullet)

    # Draw everything
    screen.fill(WHITE)  # Fill the screen with white
    
    # Draw player
    character_sprite = character_sprites[PLAYER_COLOR]
    screen.blit(character_sprite, (player_x, player_y))  # Draw the player

    # Draw enemy
    pygame.draw.rect(screen, RED, (enemy_x, enemy_y, SPRITE_SIZE, SPRITE_SIZE))
    
    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, bullet)

    # Draw enemy bullets
    for enemy_bullet in enemy_bullets:
        pygame.draw.rect(screen, RED, enemy_bullet)

    # Draw enemy health bar
    font = pygame.font.Font(None, 36)
    health_text = font.render(f"Enemy Health: {enemy_health} HP", True, BLACK)
    screen.blit(health_text, (SCREEN_WIDTH // 2 - 100, 10))

    # Draw player health
    player_health_text = font.render(f"Player Health: {PLAYER_HEALTH} HP", True, BLACK)
    screen.blit(player_health_text, (10, 10))

    # Draw player status (health, level, damage) in the bottom left
    player_status_text = font.render(f"Health: {PLAYER_HEALTH} | Level: {PLAYER_LEVEL} | Damage: {PLAYER_LEVEL * DAMAGE_PER_LEVEL}", True, BLACK)
    screen.blit(player_status_text, (10, SCREEN_HEIGHT - 40))

    # Draw EXP bar
    exp_bar_width = 200
    exp_ratio = PLAYER_EXP / EXP_TO_LEVEL_UP
    exp_bar_filled = exp_bar_width * exp_ratio
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - 100, 50, exp_bar_width, 20), 2)  # Outline of EXP bar
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 - 100, 50, exp_bar_filled, 20))  # Filled portion of EXP bar
    exp_text = font.render(f"EXP: {PLAYER_EXP}/{EXP_TO_LEVEL_UP}", True, BLACK)
    screen.blit(exp_text, (SCREEN_WIDTH // 2 - 50, 75))

    # If player health reaches 0, display game over message
    if PLAYER_HEALTH <= 0:
        game_over_text = font.render("Game Over! Press 'R' to Restart or 'ESC' to Quit", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
