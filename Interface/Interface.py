import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for screen dimensions and colors
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)

# Colors for character customization
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side Scroller Game UI")

# Character customization settings
available_colors = [RED, GREEN, BLUE, YELLOW]
current_color_index = 0
PLAYER_COLOR = available_colors[current_color_index]

# Create the player object
player_x = 100
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 50

# Game loop variables
clock = pygame.time.Clock()
in_customization_screen = True

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
        screen.blit(text, (50, 50))

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

    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_x += PLAYER_SPEED

    # Keep the player within the screen bounds
    player_x = max(0, min(SCREEN_WIDTH - SPRITE_SIZE, player_x))

    # Draw everything
    screen.fill(WHITE)  # Fill the screen with white
    character_sprite = character_sprites[PLAYER_COLOR]
    screen.blit(character_sprite, (player_x, player_y))  # Draw the player

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
