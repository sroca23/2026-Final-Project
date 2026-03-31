import pygame
import sys
import random
import math

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.load_sounds()
        
    def load_sounds(self):
        try:
            # Create simple beep sounds using pygame's built-in capabilities
            # Since numpy isn't available, we'll use placeholder sounds
            print("Sound system initialized (no external files needed)")
            
        except Exception as e:
            print(f"Sound loading failed: {e}")
            self.sounds = {}
    
    def play_sound(self, sound_name):
        # Placeholder for sound effects - just print for now
        sound_effects = {
            'boost': "BOOST SOUND!",
            'collision': "COLLISION SOUND!", 
            'achievement': "ACHIEVEMENT SOUND!",
            'menu_select': "MENU CLICK!"
        }
        if sound_name in sound_effects:
            print(f"Playing: {sound_effects[sound_name]}")
    
    def play_music(self, loop=True):
        print("Background music started (looping)")
    
    def stop_music(self):
        print("Music stopped")
    
    def set_music_volume(self, volume):
        self.music_volume = max(0, min(1, volume))
        print(f"Music volume set to {int(self.music_volume * 100)}%")
    
    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0, min(1, volume))
        print(f"SFX volume set to {int(self.sfx_volume * 100)}%")

# Create global sound manager
sound_manager = SoundManager()

class Avatar:
    def __init__(self, name, color, hair_color, shirt_color, pants_color):
        self.name = name
        self.skin_color = color
        self.hair_color = hair_color
        self.shirt_color = shirt_color
        self.pants_color = pants_color
        
    def draw_player(self, surface, x, y, boost_active=False):
        # Head
        pygame.draw.rect(surface, self.skin_color, (x, y, 25, 35))
        # Hair
        pygame.draw.rect(surface, self.hair_color, (x + 2, y - 5, 21, 8))
        # Eyes
        pygame.draw.circle(surface, BLACK, (x + 12 - 6, y + 17 - 8), 2)
        pygame.draw.circle(surface, BLACK, (x + 12 + 6, y + 17 - 8), 2)
        # Smile
        pygame.draw.arc(surface, BLACK, (x + 12 - 5, y + 17 - 5, 10, 8), 0, 3.14, 1)
        # Shirt
        pygame.draw.rect(surface, self.shirt_color, (x, y + 15, 25, 15))
        # Pants
        pygame.draw.rect(surface, self.pants_color, (x, y + 25, 25, 10))
        
        # Draw boost effect
        if boost_active:
            # Draw speed lines
            for i in range(3):
                pygame.draw.line(surface, YELLOW, 
                               (x - 10 - i*5, y + 17),
                               (x - 20 - i*8, y + 17), 2)
                pygame.draw.line(surface, YELLOW,
                               (x + 25 + 10 + i*5, y + 17),
                               (x + 25 + 20 + i*8, y + 17), 2)
            
            # Draw boost glow
            pygame.draw.circle(surface, (255, 255, 100, 50), (x + 12, y + 17), 25, 2)
            
            # Draw boost particles
            for i in range(5):
                particle_x = x + 12 + random.randint(-20, 20)
                particle_y = y + 35 + random.randint(0, 10)
                pygame.draw.circle(surface, YELLOW, (particle_x, particle_y), 2)
    
    def draw_avatar_preview(self, surface, x, y, selected=False):
        # Draw smaller version for menu
        scale = 0.8
        head_w, head_h = int(25 * scale), int(35 * scale)
        
        # Selection highlight
        if selected:
            pygame.draw.rect(surface, YELLOW, (x - 5, y - 5, head_w + 10, head_h + 20), 3)
        
        # Draw avatar
        pygame.draw.rect(surface, self.skin_color, (x, y, head_w, head_h))
        pygame.draw.rect(surface, self.hair_color, (x + 2, y - 3, int(21 * scale), 6))
        pygame.draw.circle(surface, BLACK, (x + int(12 * scale) - 4, y + int(17 * scale) - 6), 1)
        pygame.draw.circle(surface, BLACK, (x + int(12 * scale) + 4, y + int(17 * scale) - 6), 1)
        pygame.draw.rect(surface, self.shirt_color, (x, y + int(15 * scale), head_w, int(15 * scale)))
        pygame.draw.rect(surface, self.pants_color, (x, y + int(25 * scale), head_w, int(10 * scale)))
        
        # Draw name
        font = pygame.font.Font(None, 16)
        name_text = font.render(self.name, True, WHITE)
        text_rect = name_text.get_rect(center=(x + head_w//2, y + head_h + 10))
        surface.blit(name_text, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, avatar):
        super().__init__()
        self.avatar = avatar
        self.image = pygame.Surface((25, 35))
        self.image.fill(avatar.skin_color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.boost_active = False
        self.boost_timer = 0
        self.boost_duration = 180  # 3 seconds at 60 FPS
        self.boost_cooldown = 0
        self.boost_cooldown_max = 600  # 10 seconds cooldown
        
    def update(self):
        # Update boost timers
        if self.boost_active:
            self.boost_timer -= 1
            if self.boost_timer <= 0:
                self.boost_active = False
        
        if self.boost_cooldown > 0:
            self.boost_cooldown -= 1
        
        # Keep player in bounds horizontally
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    
    def move_left(self):
        speed = 25 if self.boost_active else 15
        if self.rect.left > 0:
            self.rect.x -= speed
    
    def move_right(self):
        speed = 25 if self.boost_active else 15
        if self.rect.right < SCREEN_WIDTH:
            self.rect.x += speed
    
    def activate_boost(self):
        if self.boost_cooldown <= 0 and not self.boost_active:
            self.boost_active = True
            self.boost_timer = self.boost_duration
            self.boost_cooldown = self.boost_cooldown_max
            return True
        return False
    
    def draw(self, surface):
        # Use avatar to draw player
        self.avatar.draw_player(surface, self.rect.x, self.rect.y, self.boost_active)

class Cop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((35, 40))
        self.image.fill(BLUE)  # Cop in blue
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0  # Starts stationary
        
    def update(self):
        self.rect.y += self.vel_y
    
    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)
        # Draw cop's face
        pygame.draw.circle(surface, YELLOW, (self.rect.centerx - 8, self.rect.centery - 8), 4)
        pygame.draw.circle(surface, YELLOW, (self.rect.centerx + 8, self.rect.centery - 8), 4)
        # Draw hat (badge)
        pygame.draw.rect(surface, RED, (self.rect.centerx - 10, self.rect.centery - 18, 20, 8))

class Achievement:
    def __init__(self, name, description, requirement, color):
        self.name = name
        self.description = description
        self.requirement = requirement  # Time in seconds
        self.color = color
        self.unlocked = False
        self.unlock_time = 0
        
    def check_unlock(self, time_survived):
        if not self.unlocked and time_survived >= self.requirement:
            self.unlocked = True
            self.unlock_time = pygame.time.get_ticks()
            return True
        return False
    
    def draw(self, surface, x, y, font):
        # Draw achievement box
        box_color = self.color if self.unlocked else (50, 50, 50)
        pygame.draw.rect(surface, box_color, (x, y, 200, 60))
        pygame.draw.rect(surface, WHITE, (x, y, 200, 60), 2)
        
        # Draw achievement text
        text_color = WHITE if self.unlocked else (150, 150, 150)
        name_text = font.render(self.name, True, text_color)
        desc_text = font.render(self.description, True, text_color)
        
        surface.blit(name_text, (x + 5, y + 5))
        surface.blit(desc_text, (x + 5, y + 25))
        
        # Draw unlock indicator
        if self.unlocked:
            pygame.draw.circle(surface, GOLD, (x + 180, y + 30), 8)
            pygame.draw.polygon(surface, WHITE, [
                (x + 175, y + 30),
                (x + 178, y + 33),
                (x + 185, y + 26)
            ], 2)

class Train(pygame.sprite.Sprite):
    def __init__(self, x, y, lane):
        super().__init__()
        self.lane = lane
        self.width = random.randint(60, 100)
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((100, 100, 100))  # Gray train body
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = random.randint(4, 8)  # Variable speed
        
    def update(self):
        self.rect.y += self.vel_y
    
    def draw(self, surface):
        # Draw train body
        pygame.draw.rect(surface, (100, 100, 100), self.rect)
        # Draw train windows
        window_width = 12
        window_height = 8
        for i in range(0, self.width - 15, 20):
            pygame.draw.rect(surface, (200, 200, 255), 
                           (self.rect.x + i + 5, self.rect.y + 8, window_width, window_height))
        # Draw train front light
        pygame.draw.circle(surface, YELLOW, (self.rect.centerx, self.rect.bottom - 5), 4)
        # Draw train wheels
        for i in range(10, self.width - 5, 20):
            pygame.draw.circle(surface, BLACK, (self.rect.x + i, self.rect.bottom), 3)

class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y, lane):
        super().__init__()
        self.lane = lane
        self.width = 80
        self.height = 25
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((150, 75, 0))  # Brown barrier
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = random.randint(3, 6)
        
    def update(self):
        self.rect.y += self.vel_y
    
    def draw(self, surface):
        # Draw barrier body
        pygame.draw.rect(surface, (150, 75, 0), self.rect)
        # Draw warning stripes
        for i in range(0, self.width, 10):
            pygame.draw.rect(surface, YELLOW, (self.rect.x + i, self.rect.y, 5, self.height))
        # Draw bolts
        pygame.draw.circle(surface, BLACK, (self.rect.x + 10, self.rect.y + 10), 2)
        pygame.draw.circle(surface, BLACK, (self.rect.x + self.width - 10, self.rect.y + 10), 2)

class Sign(pygame.sprite.Sprite):
    def __init__(self, x, y, lane):
        super().__init__()
        self.lane = lane
        self.width = 30
        self.height = 50
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((200, 200, 200))  # Gray pole
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = random.randint(2, 5)
        
    def update(self):
        self.rect.y += self.vel_y
    
    def draw(self, surface):
        # Draw pole
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        # Draw sign
        sign_y = self.rect.y - 15
        pygame.draw.rect(surface, RED, (self.rect.x - 10, sign_y, 50, 15))
        pygame.draw.rect(surface, WHITE, (self.rect.x - 10, sign_y, 50, 15), 2)
        # Draw STOP text
        font = pygame.font.Font(None, 12)
        stop_text = font.render("STOP", True, WHITE)
        surface.blit(stop_text, (self.rect.x - 5, sign_y + 2))

class Tunnel(pygame.sprite.Sprite):
    def __init__(self, x, y, lane):
        super().__init__()
        self.lane = lane
        self.width = SCREEN_WIDTH
        self.height = 60
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((50, 50, 50))  # Dark tunnel
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 7  # Fast moving
        
    def update(self):
        self.rect.y += self.vel_y
    
    def draw(self, surface):
        # Draw tunnel entrance
        pygame.draw.rect(surface, (50, 50, 50), self.rect)
        # Draw tunnel arch
        pygame.draw.arc(surface, (30, 30, 30), 
                       (self.rect.x, self.rect.y - 20, SCREEN_WIDTH, 80), 
                       0, 3.14, 20)
        # Draw warning lights
        for i in range(0, SCREEN_WIDTH, 100):
            pygame.draw.circle(surface, YELLOW, (self.rect.x + i, self.rect.y + 10), 3)
            pygame.draw.circle(surface, YELLOW, (self.rect.x + i, self.rect.y + self.height - 10), 3)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Subway Surfers: Kid on the Run")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.in_menu = True
        self.selected_avatar = 0
        
        # Create avatars
        self.avatars = [
            Avatar("Default", (255, 220, 177), (139, 90, 43), (70, 130, 180), (80, 80, 80)),
            Avatar("Ginger", (255, 200, 150), (200, 100, 50), (255, 100, 100), (100, 50, 50)),
            Avatar("Dark", (139, 90, 60), (50, 25, 0), (0, 100, 200), (50, 50, 50)),
            Avatar("Blonde", (255, 240, 200), (255, 220, 100), (100, 200, 100), (100, 100, 150)),
            Avatar("Purple", (220, 180, 220), (150, 50, 200), (200, 100, 200), (150, 50, 150))
        ]
        
        # Game objects (initialized when starting game)
        self.player = None
        self.cop = None
        self.obstacles = pygame.sprite.Group()  # All obstacles in one group
        self.spawn_timer = 0
        self.spawn_rate = 60
        self.score = 0
        self.time_survived = 0
        self.difficulty = 1.0
        self.cop_speed = 0
        self.blocks_hit = 0
        
        # Initialize achievements
        self.achievements = [
            Achievement("First Steps", "Survive for 10 seconds", 10, GREEN),
            Achievement("Getting Started", "Survive for 30 seconds", 30, BLUE),
            Achievement("Runner", "Survive for 60 seconds", 60, YELLOW),
            Achievement("Expert", "Survive for 120 seconds", 120, PURPLE),
            Achievement("Master", "Survive for 180 seconds", 180, RED),
            Achievement("Legend", "Survive for 300 seconds", 300, GOLD)
        ]
        self.new_unlocks = []
        
    def start_game(self):
        # Initialize game objects with selected avatar
        self.player = Player(SCREEN_WIDTH // 2 - 12, SCREEN_HEIGHT // 2, self.avatars[self.selected_avatar])
        self.cop = Cop(SCREEN_WIDTH // 2 - 17, SCREEN_HEIGHT + 20)
        self.obstacles = pygame.sprite.Group()
        self.spawn_timer = 0
        self.score = 0
        self.time_survived = 0
        self.difficulty = 1.0
        self.cop_speed = 0
        self.blocks_hit = 0
        self.game_over = False
        self.in_menu = False
        
        # Start game music
        sound_manager.play_music()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.in_menu:
                    if event.key == pygame.K_LEFT:
                        self.selected_avatar = (self.selected_avatar - 1) % len(self.avatars)
                        sound_manager.play_sound('menu_select')
                    elif event.key == pygame.K_RIGHT:
                        self.selected_avatar = (self.selected_avatar + 1) % len(self.avatars)
                        sound_manager.play_sound('menu_select')
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.start_game()
                else:
                    if event.key == pygame.K_c:  # Reset game
                        if self.game_over:
                            self.start_game()  # Restart with same avatar
                    elif event.key == pygame.K_ESCAPE:  # Return to menu
                        self.in_menu = True
                        self.game_over = False
                    elif event.key == pygame.K_SPACE:  # Activate boost
                        if self.player and self.player.activate_boost():
                            self.score += 50
                            sound_manager.play_sound('boost')
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
    
    def spawn_obstacle(self):
        self.spawn_timer += 1
        # Spawn rate decreases (more frequent) as difficulty increases
        spawn_rate = max(15, int(self.spawn_rate - (self.difficulty * 10)))
        
        if self.spawn_timer >= spawn_rate:
            # Random lane selection (left, middle, right)
            lanes = [50, SCREEN_WIDTH // 2 - 30, SCREEN_WIDTH - 130]
            lane = random.choice(lanes)
            
            # Random obstacle type based on difficulty
            obstacle_types = ['train', 'barrier', 'sign']
            if self.difficulty > 2:
                obstacle_types.append('tunnel')
            
            obstacle_type = random.choice(obstacle_types)
            
            if obstacle_type == 'train':
                obstacle = Train(lane, -50, lane)
                obstacle.vel_y = 5 + (self.difficulty * 0.5)
            elif obstacle_type == 'barrier':
                obstacle = Barrier(lane, -30, lane)
                obstacle.vel_y = 4 + (self.difficulty * 0.4)
            elif obstacle_type == 'sign':
                obstacle = Sign(lane, -60, lane)
                obstacle.vel_y = 3 + (self.difficulty * 0.3)
            elif obstacle_type == 'tunnel':
                obstacle = Tunnel(0, -70, 0)
                obstacle.vel_y = 7 + (self.difficulty * 0.6)
            
            self.obstacles.add(obstacle)
            self.spawn_timer = 0
    
    def update(self):
        if self.in_menu:
            return  # Don't update game when in menu
            
        if not self.game_over:
            self.handle_input()
            self.player.update()
            self.cop.update()
            
            # Move obstacles and remove off-screen ones
            for obstacle in self.obstacles:
                obstacle.update()
            
            # Remove obstacles that are off-screen (bottom)
            self.obstacles = pygame.sprite.Group([obs for obs in self.obstacles if obs.rect.top < SCREEN_HEIGHT])
            
            # Spawn new obstacles
            self.spawn_obstacle()
            
            # Update score and time
            self.time_survived += 1
            self.score = self.time_survived // 10
            # Difficulty increases after each block hit
            self.difficulty = 1.0 + (self.blocks_hit * 0.3)
            
            # Check achievements
            current_time = self.time_survived // 60  # Convert to seconds
            for achievement in self.achievements:
                if achievement.check_unlock(current_time):
                    self.new_unlocks.append(achievement)
                    sound_manager.play_sound('achievement')
            
            # Cop only moves if speed is greater than 0 (activated by obstacles)
            if self.cop_speed > 0:
                self.cop.vel_y = -self.cop_speed - (self.difficulty * 0.5)
            else:
                self.cop.vel_y = 0
            
            # Check collisions with obstacles
            for obstacle in self.obstacles:
                if self.player.rect.colliderect(obstacle.rect):
                    self.game_over = True
                    sound_manager.play_sound('collision')
                    # Increment blocks hit counter
                    self.blocks_hit += 1
                    # Cop starts chasing and speeds up when hitting obstacle
                    if self.cop_speed == 0:
                        self.cop_speed = 3
                    else:
                        self.cop_speed *= 1.5
            
            # Check if caught by cop
            if self.player.rect.colliderect(self.cop.rect):
                self.game_over = True
                sound_manager.play_sound('collision')
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.in_menu:
            self.draw_menu()
        else:
            self.draw_game()
        
        pygame.display.flip()
    
    def draw_menu(self):
        # Stop game music when in menu
        sound_manager.stop_music()
        
        # Draw title
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("SUBWAY SURFERS", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title_text, title_rect)
        
        subtitle_font = pygame.font.Font(None, 24)
        subtitle_text = subtitle_font.render("Select Your Avatar", True, YELLOW)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw avatars
        avatar_spacing = 120
        start_x = (SCREEN_WIDTH - (len(self.avatars) * avatar_spacing)) // 2
        
        for i, avatar in enumerate(self.avatars):
            x = start_x + i * avatar_spacing
            y = 200
            avatar.draw_avatar_preview(self.screen, x, y, i == self.selected_avatar)
        
        # Draw instructions
        inst_font = pygame.font.Font(None, 20)
        instructions = [
            "Use LEFT/RIGHT arrows to select",
            "Press SPACE or ENTER to start",
            "Press ESC to return during game"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = inst_font.render(instruction, True, WHITE)
            inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH//2, 350 + i * 30))
            self.screen.blit(inst_text, inst_rect)
    
    def draw_game(self):
        # Draw subway background (simple pattern)
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, (50, 50, 50), (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw game objects
        self.player.draw(self.screen)
        self.cop.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        time_text = pygame.font.Font(None, 24).render(f"Time: {self.time_survived // 60}s", True, WHITE)
        self.screen.blit(time_text, (10, 50))
        
        # Draw sound indicator
        sound_text = pygame.font.Font(None, 16).render("[SOUND ON]", True, GREEN)
        self.screen.blit(sound_text, (SCREEN_WIDTH - 80, 10))
        
        # Draw boost status
        boost_color = YELLOW if self.player.boost_active else (100, 100, 100)
        boost_text = "BOOST ACTIVE!" if self.player.boost_active else f"Boost Ready: {max(0, self.player.boost_cooldown // 60)}s"
        boost_status = pygame.font.Font(None, 20).render(boost_text, True, boost_color)
        self.screen.blit(boost_status, (10, 80))
        
        # Draw boost bar
        bar_width = 200
        bar_height = 10
        bar_x = 10
        bar_y = 105
        
        # Background bar
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Boost cooldown bar
        if self.player.boost_cooldown > 0:
            cooldown_percentage = 1 - (self.player.boost_cooldown / self.player.boost_cooldown_max)
            pygame.draw.rect(self.screen, (100, 100, 255), 
                           (bar_x, bar_y, int(bar_width * cooldown_percentage), bar_height))
        else:
            # Boost ready - green bar
            pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, bar_width, bar_height))
        
        # Active boost bar
        if self.player.boost_active:
            boost_percentage = self.player.boost_timer / self.player.boost_duration
            pygame.draw.rect(self.screen, YELLOW, 
                           (bar_x, bar_y, int(bar_width * boost_percentage), bar_height))
        
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
        
        # Draw achievements
        small_font = pygame.font.Font(None, 18)
        achievement_y = 80
        for i, achievement in enumerate(self.achievements[:3]):  # Show first 3 achievements
            achievement.draw(self.screen, SCREEN_WIDTH - 210, achievement_y, small_font)
            achievement_y += 65
        
        # Draw achievement unlock notifications
        current_time = pygame.time.get_ticks()
        self.new_unlocks = [a for a in self.new_unlocks if current_time - a.unlock_time < 3000]  # Show for 3 seconds
        
        for i, achievement in enumerate(self.new_unlocks):
            # Draw unlock notification
            notification_y = 150 + i * 70
            pygame.draw.rect(self.screen, achievement.color, (50, notification_y, 250, 50))
            pygame.draw.rect(self.screen, GOLD, (50, notification_y, 250, 50), 3)
            
            unlock_text = pygame.font.Font(None, 24).render("ACHIEVEMENT UNLOCKED!", True, WHITE)
            name_text = pygame.font.Font(None, 20).render(achievement.name, True, WHITE)
            
            self.screen.blit(unlock_text, (60, notification_y + 5))
            self.screen.blit(name_text, (60, notification_y + 25))
        
        # Draw game over message
        if self.game_over:
            # Stop music on game over
            sound_manager.stop_music()
            
            # Draw dark overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Draw game over box
            box_width, box_height = 350, 250
            box_x = (SCREEN_WIDTH - box_width) // 2
            box_y = (SCREEN_HEIGHT - box_height) // 2
            
            # Draw box background with gradient effect
            for i in range(box_height):
                color_value = 50 + (i * 2)
                if color_value > 150:
                    color_value = 150
                pygame.draw.line(self.screen, (color_value, 0, 0), 
                               (box_x, box_y + i), (box_x + box_width, box_y + i))
            
            # Draw box border
            pygame.draw.rect(self.screen, RED, (box_x, box_y, box_width, box_height), 3)
            pygame.draw.rect(self.screen, YELLOW, (box_x - 2, box_y - 2, box_width + 4, box_height + 4), 2)
            
            # Draw "GAME OVER" with shadow effect
            game_over_font = pygame.font.Font(None, 72)
            shadow_text = game_over_font.render("GAME OVER", True, BLACK)
            game_over_text = game_over_font.render("GAME OVER", True, RED)
            
            self.screen.blit(shadow_text, (SCREEN_WIDTH//2 - 148, SCREEN_HEIGHT//2 - 158))
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 160))
            
            # Draw stats
            stats_font = pygame.font.Font(None, 28)
            
            # Final score
            score_shadow = stats_font.render(f"Final Score: {self.score}", True, BLACK)
            score_text = stats_font.render(f"Final Score: {self.score}", True, WHITE)
            self.screen.blit(score_shadow, (SCREEN_WIDTH//2 - 118, SCREEN_HEIGHT//2 - 18))
            self.screen.blit(score_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 20))
            
            # Time survived
            time_shadow = stats_font.render(f"Time Survived: {self.time_survived // 60}s", True, BLACK)
            time_text = stats_font.render(f"Time Survived: {self.time_survived // 60}s", True, YELLOW)
            self.screen.blit(time_shadow, (SCREEN_WIDTH//2 - 108, SCREEN_HEIGHT//2 + 12))
            self.screen.blit(time_text, (SCREEN_WIDTH//2 - 110, SCREEN_HEIGHT//2 + 10))
            
            # Blocks hit
            blocks_shadow = stats_font.render(f"Trains Hit: {self.blocks_hit}", True, BLACK)
            blocks_text = stats_font.render(f"Trains Hit: {self.blocks_hit}", True, (255, 150, 150))
            self.screen.blit(blocks_shadow, (SCREEN_WIDTH//2 - 88, SCREEN_HEIGHT//2 + 42))
            self.screen.blit(blocks_text, (SCREEN_WIDTH//2 - 90, SCREEN_HEIGHT//2 + 40))
            
            # Draw options
            option_font = pygame.font.Font(None, 24)
            
            # Restart option
            restart_shadow = option_font.render("Press C to Restart", True, BLACK)
            restart_text = option_font.render("Press C to Restart", True, GREEN)
            self.screen.blit(restart_shadow, (SCREEN_WIDTH//2 - 78, SCREEN_HEIGHT//2 + 82))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 80))
            
            # Menu option
            menu_shadow = option_font.render("Press ESC for Menu", True, BLACK)
            menu_text = option_font.render("Press ESC for Menu", True, YELLOW)
            self.screen.blit(menu_shadow, (SCREEN_WIDTH//2 - 78, SCREEN_HEIGHT//2 + 102))
            self.screen.blit(menu_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 100))
            
            # Draw achievement summary
            unlocked_count = sum(1 for a in self.achievements if a.unlocked)
            achievement_text = option_font.render(f"Achievements: {unlocked_count}/{len(self.achievements)}", True, GOLD)
            self.screen.blit(achievement_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 120))
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
