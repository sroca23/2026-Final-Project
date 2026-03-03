import pygame
import sys
import random

# Initialize Pygame
pygame.init()

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

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(YELLOW)  # Kid in yellow
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        
    def update(self):
        # Keep player in bounds horizontally
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    
    def move_left(self):
        if self.rect.left > 0:
            self.rect.x -= 15
    
    def move_right(self):
        if self.rect.right < SCREEN_WIDTH:
            self.rect.x += 15
    
    def draw(self, surface):
        # Draw kid as a simple sprite
        pygame.draw.rect(surface, YELLOW, self.rect)
        # Draw eyes
        pygame.draw.circle(surface, BLACK, (self.rect.centerx - 8, self.rect.centery - 5), 3)
        pygame.draw.circle(surface, BLACK, (self.rect.centerx + 8, self.rect.centery - 5), 3)

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

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width=80, height=20):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)  # Obstacle in brown
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 5  # Moving downward
        
    def update(self):
        self.rect.y += self.vel_y
    
    def draw(self, surface):
        pygame.draw.rect(surface, BROWN, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Subway Surfers: Kid on the Run")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        self.player = Player(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2)
        self.cop = Cop(SCREEN_WIDTH // 2 - 17, SCREEN_HEIGHT + 20)
        self.obstacles = pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_rate = 60  # Spawn obstacle every 60 frames
        self.score = 0
        self.time_survived = 0
        self.difficulty = 1.0
        self.cop_speed = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # Reset game
                    if self.game_over:
                        self.__init__()
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
    
    def spawn_obstacle(self):
        self.spawn_timer += 1
        spawn_rate = max(30, int(self.spawn_rate - (self.difficulty * 5)))
        
        if self.spawn_timer >= spawn_rate:
            x = random.randint(0, SCREEN_WIDTH - 80)
            width = random.randint(60, 100)
            obstacle = Obstacle(x, -20, width, 20)
            self.obstacles.add(obstacle)
            self.spawn_timer = 0
    
    def update(self):
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
            self.difficulty = 1.0 + (self.time_survived // 1000)
            
            # Cop only moves if speed is greater than 0 (activated by obstacles)
            if self.cop_speed > 0:
                self.cop.vel_y = -self.cop_speed - (self.difficulty * 0.5)
            else:
                self.cop.vel_y = 0
            
            # Check collisions with obstacles
            for obstacle in self.obstacles:
                if self.player.rect.colliderect(obstacle.rect):
                    self.game_over = True
                    # Cop starts chasing and speeds up when hitting obstacle
                    if self.cop_speed == 0:
                        self.cop_speed = 3
                    else:
                        self.cop_speed *= 1.5
            
            # Check if caught by cop
            if self.player.rect.colliderect(self.cop.rect):
                self.game_over = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
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
        
        # Draw game over message
        if self.game_over:
            game_over_font = pygame.font.Font(None, 60)
            game_over_text = game_over_font.render("GAME OVER", True, RED)
            final_score_font = pygame.font.Font(None, 36)
            final_score_text = final_score_font.render(f"Final Score: {self.score}", True, WHITE)
            restart_font = pygame.font.Font(None, 28)
            restart_text = restart_font.render("Press C to Restart", True, YELLOW)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 80))
            self.screen.blit(final_score_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 110, SCREEN_HEIGHT//2 + 60))
        
        pygame.display.flip()
    
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
