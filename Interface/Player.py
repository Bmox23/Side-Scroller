import pygame

RED = (255, 0, 0)
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5
BULLET_SPEED = 200
DAMAGE_PER_LEVEL = 2
PLAYER_HEALTH = 20
EXP_TO_LEVEL_UP = 20
JUMP_STRENGTH = 15
GRAVITY = 1

class Player:
    EXP_TABLE = [8, 19, 37, 61, 91, 127, 169, 217, 271, 331, 397, 469, 547, 631, 721, 817, 919, 1027, 1141, 1261, 1387, 1519, 1657, 1801, 1951, 2107, 2269, 2437, 2611, 2791, 2977, 3169, 3367, 3571, 3781, 3997, 4219, 4447, 4681, 4921, 5167, 5419, 5677, 5941, 6211, 6487, 6769, 7057, 7351, 7651, 7957, 8269, 8587, 8911, 9241, 9577, 9919, 10267, 10621, 10981, 11347, 11719, 12097, 12481, 12871, 13267, 13669, 14077, 14491, 14911, 15337, 15769, 16207, 16651, 17101, 17557, 18019, 18487, 18961, 19441, 19927, 20419, 20917, 21421, 21931, 22447, 22969, 23497, 24031, 24571, 25117, 25669, 26227, 26791, 27361, 27937, 28519, 29107, 29701, 30301]

    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_y = 0
        self.is_jumping = False
        self.color = RED
        self.level = 1
        self.health = PLAYER_HEALTH
        self.exp = 0
        self.exp_to_level_up = self.EXP_TABLE[0] if len(self.EXP_TABLE) > 0 else EXP_TO_LEVEL_UP
        self.bullet_speed = BULLET_SPEED
        self.damage_per_level = DAMAGE_PER_LEVEL
        self.special_attack_cooldown = 0  # Track cooldown time for special attack

    def handle_keys(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.x += PLAYER_SPEED
        # Keep the player within screen bounds
        self.x = max(0, min(self.screen_width - PLAYER_WIDTH, self.x))

    def apply_gravity(self):
        if self.is_jumping:
            self.velocity_y += GRAVITY
            self.y += self.velocity_y
            if self.y >= self.screen_height - PLAYER_HEIGHT - 50:
                self.y = self.screen_height - PLAYER_HEIGHT - 50
                self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -JUMP_STRENGTH

    def shoot(self):
        return pygame.Rect(self.x + PLAYER_WIDTH, self.y + PLAYER_HEIGHT // 2 - 5, 10, 10)

    def special_attack(self, current_time, enemy):
        if current_time - self.special_attack_cooldown >= 30:
            damage = 50 + (0.01 * self.level * 50)
            enemy.take_damage(damage)
            self.special_attack_cooldown = current_time

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def gain_experience(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_level_up:
            self.level += 1
            self.health = min(self.health + 5, 20 + 5 * (self.level - 1))
            self.exp -= self.exp_to_level_up
            if self.level < len(self.EXP_TABLE):
                self.exp_to_level_up = self.EXP_TABLE[self.level - 1]
            else:
                self.exp_to_level_up = int(self.exp_to_level_up * 1.2)  # Increase the EXP needed for each subsequent level

    def restart(self):
        self.x = 100
        self.y = self.screen_height - PLAYER_HEIGHT - 50
        self.velocity_y = 0
        self.health = PLAYER_HEALTH
        self.level = 1
        self.exp = 0
        self.exp_to_level_up = self.EXP_TABLE[0] if len(self.EXP_TABLE) > 0 else EXP_TO_LEVEL_UP  # Reset exp to level up
        self.is_jumping = False
        self.special_attack_cooldown = 0  # Reset special attack cooldown

    def draw_hud(self, screen, screen_width, screen_height):
        font = pygame.font.Font(None, 36)
        player_status_text = font.render(f"Health: {self.health} | Level: {self.level} | Damage: {self.level * self.damage_per_level} | EXP: {self.exp}/{self.exp_to_level_up}", True, (0, 0, 0))
        screen.blit(player_status_text, (10, screen_height - 40))
