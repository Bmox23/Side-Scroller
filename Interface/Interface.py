import pygame
import sys
import random
from Player import Player
from Enemy import Enemy
import time

# Initialize Pygame
pygame.init()

# Constants for screen dimensions and colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((800, 600))
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Side Scroller Game UI")

# Create Player and Enemy objects
player = Player(100, SCREEN_HEIGHT - 110, SCREEN_WIDTH, SCREEN_HEIGHT)
enemy = Enemy(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 110)

# Bullets list
bullets = []
enemy_bullets = []

# Special attack variables
special_attack_last_used = 0
special_attack_cooldown = 30  # Cooldown time in seconds

# Game loop variables
clock = pygame.time.Clock()

# Main game loop
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
                bullet = player.shoot()
                if bullet:
                    bullets.append(bullet)
            elif event.key == pygame.K_UP:
                player.jump()
            elif event.key == pygame.K_b:
                current_time = time.time()
                if current_time - special_attack_last_used >= special_attack_cooldown:
                    special_attack_last_used = current_time
                    enemy.take_damage(50 * (1 + 0.01 * player.level))  # Special attack damage scales with level
                    print("Special attack used!")
            elif player.health <= 0:
                if event.key == pygame.K_r:  # Restart game
                    player.restart()
                    enemy.restart()
                    bullets.clear()
                    enemy_bullets.clear()

    # Handle key presses
    keys = pygame.key.get_pressed()
    player.handle_keys(keys)

    # Apply gravity to player
    player.apply_gravity()

    # Update bullets
    for bullet in bullets[:]:
        bullet.x += player.bullet_speed
        if bullet.colliderect(enemy.get_rect()):
            bullets.remove(bullet)
            enemy.take_damage(player.level * player.damage_per_level)
            if enemy.health <= 0:
                player.gain_experience(random.randint(1, 10))
                enemy.respawn(SCREEN_WIDTH)
        elif bullet.x > SCREEN_WIDTH:
            bullets.remove(bullet)

    # Enemy shooting
    if enemy.can_shoot():
        enemy_bullet = enemy.shoot()
        enemy_bullets.append(enemy_bullet)

    # Update enemy bullets
    for enemy_bullet in enemy_bullets[:]:
        enemy_bullet.x -= enemy.bullet_speed
        if enemy_bullet.colliderect(player.get_rect()):
            enemy_bullets.remove(enemy_bullet)
            player.take_damage(1)
        elif enemy_bullet.x < 0:
            enemy_bullets.remove(enemy_bullet)

    # Draw everything
    screen.fill(WHITE)  # Fill the screen with white
    player.draw(screen)
    enemy.draw(screen)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, bullet)

    # Draw enemy bullets
    for enemy_bullet in enemy_bullets:
        pygame.draw.rect(screen, (255, 0, 0), enemy_bullet)

    # Draw HUD
    player.draw_hud(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    enemy.draw_health(screen, SCREEN_WIDTH)

    # Draw special attack cooldown
    current_time = time.time()
    time_since_last_special = current_time - special_attack_last_used
    if time_since_last_special < special_attack_cooldown:
        cooldown_remaining = special_attack_cooldown - time_since_last_special
        cooldown_text = f"Special Attack Cooldown: {int(cooldown_remaining)}s"
    else:
        cooldown_text = "Special Attack Ready!"
    font = pygame.font.Font(None, 36)
    cooldown_surface = font.render(cooldown_text, True, RED)
    screen.blit(cooldown_surface, (20, 60))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
