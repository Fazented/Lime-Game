import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 1000 # Default 1000x800
HEIGHT = 800
FPS = 60

# GAME VARIABLES
enemiespawner = 10 # Amount of enemies to spawn, Default 10
powerupspawner = 15 # Amount of powerups to spawn, Default 15
winscore = 15 # Amount of powerups to win, Default 10
timelimit = 100 # Time limit, Default 100

spawnprotection = 4 # Sets the spawn protection time, Default 4
playerspeed = 7 # Sets the player speed, Default 7
enemyspeed_x = [-2,2] # Sets the enemy speed, Default for both is -2,2
enemyspeed_y = [-2,2]
playersize = (50, 50) # Sets the player size, Default (50, 50)
healthbarcount = 2 # Sets the lives for the player, Default 2


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Family Friendly Python Game") # Game window name
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20) # Default is 0, 0, 0
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

playercolour = BLUE

icon_img = pygame.image.load("window_icon.ico")
pygame.display.set_icon(icon_img)

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(playersize)
        self.image.fill(playercolour)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speed = playerspeed
        self.score = 0
        self.max_health = healthbarcount
        self.current_health = self.max_health
        self.spawn_protection_timer = None
        self.spawn_protection_duration = spawnprotection * FPS  # 4 seconds in frames
        self.spawn_protected = False

    def update(self):
        # Move the player
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        elif keys[pygame.K_a]:
            self.rect.x -= self.speed
        
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
        
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        elif keys[pygame.K_w]:
            self.rect.y -= self.speed
        
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        elif keys[pygame.K_s]:
            self.rect.y += self.speed

        # Keep the player within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        # Update spawn protection timer
        if self.spawn_protection_timer:
            self.spawn_protection_timer -= 1
            if self.spawn_protection_timer <= 0:
                self.spawn_protected = False

    def take_damage(self):
        if not self.spawn_protected:
            self.current_health -= 1
            self.rect.x = 500
            self.rect.y = 400
            if self.current_health <= 0:
                self.kill()  # Player is dead
            else:
                self.spawn_protected = True
                self.spawn_protection_timer = self.spawn_protection_duration

    def increase_score_health(self):
        if self.current_health < self.max_health:
            self.current_health += 1
            if self.current_health > self.max_health:  # Add this condition to prevent exceeding max health
                self.current_health = self.max_health
        self.score += 1

# Define enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy_sprite.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.speed_x = random.choice(enemyspeed_x)
        self.speed_y = random.choice(enemyspeed_y)
        self.spawn_position()

    def spawn_position(self):
        while True:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            if not player.rect.colliderect(self.rect):
                break


    def update(self):
        # Move the enemy
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce the enemy off the screen edges
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_y *= -1

# Define power-up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("powerup_sprite.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.spawn_position()

    def spawn_position(self):
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)

    def update(self):
        pass

# Define healthbar class
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.max_health = player.max_health  # Use the player's max health
        self.current_health = player.current_health  # Use the player's current health
        self.width = 200
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.update_position()
        self.update_color()

    def update(self):
        # Update health bar based on player's current health
        self.current_health = self.player.current_health
        self.update_position()
        self.update_color()

    def update_position(self):
        self.rect.centerx = WIDTH / 2
        self.rect.y = 10

    def update_color(self):
        health_ratio = player.current_health / player.max_health
        if health_ratio > 0.5:
            self.image.fill(GREEN)
        else:
            self.image.fill(RED)

# Define health_regenbar class
class Health_RegenBar(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.max_health = player.max_health  # Use the player's max health
        self.current_health = player.current_health  # Use the player's current health
        self.width = 200
        self.height = 5
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.update_position()
        self.update_color()

    def update(self):
        # Update health bar based on player's current health
        self.current_health = self.player.current_health
        self.update_position()
        self.update_color()

    def update_position(self):
        self.rect.centerx = WIDTH / 2
        self.rect.y = 32

    def update_color(self):
        health_ratio = player.current_health / player.max_health
        if health_ratio > 0.5:
            self.image.fill(WHITE)
        else:
            self.image.fill(RED)

# Load sound effects
pygame.mixer.music.load(os.path.join("sounds", "background_music.mp3"))
pygame.mixer.music.set_volume(0.08) # Default 0.08
pygame.mixer.music.play(-1)

powerup_sound = pygame.mixer.Sound(os.path.join("sounds", "powerup.wav"))
powerup_sound.set_volume(0.6)

collision_sound = pygame.mixer.Sound(os.path.join("sounds", "collision.mp3"))
collision_sound.set_volume(0.6)

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Create the player
player = Player()
all_sprites.add(player)

# Create enemies
for _ in range(enemiespawner):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Create power-ups
for _ in range(powerupspawner):
    powerup = PowerUp()
    all_sprites.add(powerup)
    powerups.add(powerup)

# Create health bar
health_bar = HealthBar(player)
all_sprites.add(health_bar)

# Create the health regen bar
regen_bar = Health_RegenBar(player)
all_sprites.add(regen_bar)

# Game variables
game_over = False
win = False
score_to_win = winscore
time_limit =  timelimit * 60 # 100 seconds at 60 FPS
timer = time_limit

# Game loop
running = True
restart = False
restart_pressed = False  # Flag to track if 'R' key has been pressed

while running:
    # Keep the loop running at the right speed
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if not restart_pressed:  # Check if 'R' key has not been pressed before
                restart_pressed = True
                restart = True

    if restart:
        restart = False
        restart_pressed = False  # Reset the restart_pressed flag
        game_over = False
        win = False
        timer = time_limit
        player.score = 0
        player.current_health = player.max_health
        all_sprites.empty()
        enemies.empty()
        powerups.empty()
        player.spawn_protected = True

        # Create a new player and health bar
        player = Player()
        health_bar = HealthBar(player)
        regen_bar = Health_RegenBar(player)
        all_sprites.add(player, health_bar, regen_bar)

        for _ in range(enemiespawner):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        for _ in range(powerupspawner):
            powerup = PowerUp()
            all_sprites.add(powerup)
            powerups.add(powerup)

    if not game_over:
        # Update
        all_sprites.update()

        # Check for collisions between player and enemies
        if not player.spawn_protected:  # Check for spawn protection
            hits = pygame.sprite.spritecollide(player, enemies, False)
            if hits:
                collision_sound.play()
                player.take_damage()

        # Check for collisions between player and power-ups
        powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
        for powerup in powerup_hits:
            powerup_sound.play()
            player.increase_score_health()
            if player.score >= score_to_win:
                win = True
                game_over = True

        # Update timer
        timer -= 1
        if timer <= 0 or player.current_health <= 0:
            game_over = True

        # Render (draw)
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(player.score), True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw timer
        timer_text = font.render("Time: " + str(timer // FPS), True, WHITE)
        screen.blit(timer_text, (10, 50))

        # TEST DRAW HEALTH
        #healthtest = font.render("Health: " + str(player.current_health), True, WHITE)
        #screen.blit(healthtest, (10, 70))

    if game_over:
        # Draw game over message
        font = pygame.font.Font(None, 72)
        if win:
            message = font.render("You Win!", True, GREEN)
        else:
            message = font.render("Game Over", True, RED)
        message_rect = message.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(message, message_rect)
        restart_text = font.render("Press R to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100))
        screen.blit(restart_text, restart_rect)

    # Flip the display
    pygame.display.flip()

# Clean up
pygame.quit()
