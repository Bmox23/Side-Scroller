import pygame
import random

RED = (255, 0, 0)
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 60
ENEMY_BULLET_SPEED = 5

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.max_health = random.randint(50, 100)  # Randomly assign max health between 50 and 100
        self.health = self.max_health
        self.bullet_speed = ENEMY_BULLET_SPEED
        self.color = RED

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, ENEMY_WIDTH, ENEMY_HEIGHT))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, ENEMY_WIDTH, ENEMY_HEIGHT)

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def can_shoot(self):
        # Logic to decide if the enemy can shoot (e.g., based on a timer or random chance)
        return True  # Placeholder for example purposes

    def shoot(self):
        return pygame.Rect(self.x, self.y + ENEMY_HEIGHT // 2 - 5, 10, 10)

    def draw_health(self, screen, screen_width):
        # Draw enemy health bar
        health_bar_width = 200
        health_ratio = self.health / self.max_health
        health_bar_filled = health_bar_width * health_ratio
        pygame.draw.rect(screen, (0, 0, 0), (screen_width // 2 - 100, 40, health_bar_width, 20), 2)  # Outline of enemy health bar
        pygame.draw.rect(screen, RED, (screen_width // 2 - 100, 40, health_bar_filled, 20))  # Filled portion of health bar

    def restart(self):
        # Reset enemy health and position
        self.health = self.max_health
        self.x = random.randint(100, 400)  # Reset to a new random position

    def respawn(self):
    # Respawn enemy with full health and at a new random position
        self.health = self.max_health
        self.x = random.randint(100, self.screen_width - 200)
        self.y = random.randint(50, 400)
