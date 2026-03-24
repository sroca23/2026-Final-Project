import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

class Bat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 8))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.angle = 0
        self.swinging = False
        self.swing_speed = 0
        
    def update(self):
        if self.swinging:
            self.angle += self.swing_speed
            if self.angle >= 90:
                self.swinging = False
                self.angle = 0
                self.swing_speed = 0
    
    def swing(self):
        if not self.swinging:
            self.swinging = True
            self.swing_speed = 15
    
    def draw(self, surface):
        # Create rotated bat
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, rotated_rect)

class Dodgeball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radius = 8
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.5
        self.hit = False
        self.pitching = False
        self.pitch_start_x = x
        self.pitch_start_y = y
        
    def update(self):
        if self.pitching:
            # Move ball towards batter during pitch
            target_x = 200  # Bat center position
            target_y = 400  # Bat height position
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 5:
                self.vel_x = (dx / distance) * 8  # Pitch speed
                self.vel_y = (dy / distance) * 8
                self.rect.x += self.vel_x
                self.rect.y += self.vel_y
            else:
                # Ball reached bat position, stop pitching
                self.pitching = False
                self.vel_x = 0
                self.vel_y = 0
        
        elif self.hit:
            self.vel_x *= 0.99  # Air resistance
            self.vel_y += self.gravity
            self.rect.x += self.vel_x
            self.rect.y += self.vel_y
            
            # Bounce off ground
            if self.rect.bottom >= SCREEN_HEIGHT - 50:
                self.rect.bottom = SCREEN_HEIGHT - 50
                self.vel_y *= -0.7
                self.vel_x *= 0.8
                
                if abs(self.vel_y) < 1:
                    self.vel_y = 0
    
    def hit_ball(self, power, angle):
        self.hit = True
        self.vel_x = power * math.cos(math.radians(angle))
        self.vel_y = power * math.sin(math.radians(angle))
    
    def start_pitch(self):
        if not self.pitching and not self.hit:
            self.pitching = True
            self.rect.centerx = self.pitch_start_x
            self.rect.centery = self.pitch_start_y
    
    def draw(self, surface):
        pygame.draw.circle(surface, RED, self.rect.center, self.radius)
        pygame.draw.circle(surface, WHITE, (self.rect.centerx - 3, self.rect.centery - 3), 2)

class Pitcher(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pitching = False
        self.pitch_timer = 0
        
    def update(self):
        if self.pitching:
            self.pitch_timer += 1
            if self.pitch_timer >= 30:
                self.pitching = False
                self.pitch_timer = 0
    
    def pitch(self):
        if not self.pitching:
            self.pitching = True
            self.pitch_timer = 0
            return True
        return False
    
    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)
        # Draw head
        pygame.draw.circle(surface, (255, 220, 177), (self.rect.centerx, self.rect.top - 10), 10)
        # Draw cap
        pygame.draw.rect(surface, RED, (self.rect.centerx - 12, self.rect.top - 20, 24, 8))

class Batter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25, 45))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw(self, surface):
        pygame.draw.rect(surface, YELLOW, self.rect)
        # Draw head
        pygame.draw.circle(surface, (255, 220, 177), (self.rect.centerx, self.rect.top - 8), 8)
        # Draw helmet
        pygame.draw.circle(surface, BLUE, (self.rect.centerx, self.rect.top - 8), 10, 2)

class Outfielder(pygame.sprite.Sprite):
    def __init__(self, x, y, number):
        super().__init__()
        self.image = pygame.Surface((25, 40))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.number = number
        self.target_x = x
        self.target_y = y
        self.speed = 2
        
    def move_to_ball(self, ball):
        if ball.hit:
            dx = ball.rect.centerx - self.rect.centerx
            dy = ball.rect.centery - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 30:
                self.rect.x += (dx / distance) * self.speed
                self.rect.y += (dy / distance) * self.speed
    
    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        # Draw head
        pygame.draw.circle(surface, (255, 220, 177), (self.rect.centerx, self.rect.top - 8), 8)
        # Draw number
        font = pygame.font.Font(None, 16)
        number_text = font.render(str(self.number), True, WHITE)
        surface.blit(number_text, (self.rect.centerx - 5, self.rect.centery - 5))

class Base(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.size = 30
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.occupied = False
        
    def draw(self, surface):
        color = YELLOW if self.occupied else WHITE
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        # Draw base label
        font = pygame.font.Font(None, 20)
        label = font.render(self.name, True, BLACK)
        surface.blit(label, (self.rect.centerx - 8, self.rect.centery - 8))

class HomePlate(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 40
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw(self, surface):
        # Draw home plate as a pentagon shape
        points = [
            (self.rect.centerx, self.rect.bottom),
            (self.rect.right, self.rect.centery),
            (self.rect.centerx + 10, self.rect.top),
            (self.rect.centerx - 10, self.rect.top),
            (self.rect.left, self.rect.centery)
        ]
        pygame.draw.polygon(surface, WHITE, points)
        pygame.draw.polygon(surface, BLACK, points, 2)

class BattersBox(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 60
        self.height = 80
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def draw(self, surface):
        pygame.draw.rect(surface, BROWN, self.rect, 3)

class BaseballGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Baseball Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create game objects
        self.bat = Bat(200, 400)
        self.ball = Dodgeball(100, 320)  # Start ball at pitcher position
        self.pitcher = Pitcher(100, 300)
        self.batter = Batter(180, 380)
        
        # Create outfielders
        self.outfielders = [
            Outfielder(500, 200, 1),
            Outfielder(600, 150, 2),
            Outfielder(700, 250, 3)
        ]
        
        # Create bases
        self.bases = [
            Base(300, 450, "1B"),
            Base(400, 400, "2B"),
            Base(500, 450, "3B")
        ]
        
        # Create home plate and batter's box
        self.home_plate = HomePlate(380, 440)
        self.batters_box = BattersBox(160, 360)
        
        self.score = 0
        self.ball_in_play = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Only allow swing when ball is not pitching and not already hit
                    if not self.ball.pitching and not self.ball.hit:
                        self.bat.swing()
                        if self.check_bat_collision():
                            power = random.randint(15, 25)
                            angle = random.randint(-45, 45)
                            self.ball.hit_ball(power, angle)
                            self.ball_in_play = True
                            self.score += 10
                if event.key == pygame.K_p:
                    if self.pitcher.pitch():
                        self.ball.start_pitch()
                if event.key == pygame.K_r:
                    self.__init__()
    
    def check_bat_collision(self):
        # Check collision when ball is near bat and bat is swinging
        if self.bat.swinging and not self.ball.hit and not self.ball.pitching:
            # Create a larger collision area for the bat during swing
            bat_rect = self.bat.rect.inflate(40, 40)
            return bat_rect.colliderect(self.ball.rect)
        return False
    
    def update(self):
        self.bat.update()
        self.ball.update()
        self.pitcher.update()
        
        for outfielder in self.outfielders:
            outfielder.move_to_ball(self.ball)
        
        # Check if outfielders catch the ball
        for outfielder in self.outfielders:
            if self.ball.hit and outfielder.rect.colliderect(self.ball.rect):
                self.ball.hit = False
                self.ball.vel_x = 0
                self.ball.vel_y = 0
                self.ball_in_play = False
                self.score -= 5
        
        # Reset ball if it goes off screen
        if self.ball.rect.left > SCREEN_WIDTH or self.ball.rect.top > SCREEN_HEIGHT or self.ball.rect.right < 0:
            self.ball.hit = False
            self.ball.pitching = False
            self.ball.vel_x = 0
            self.ball.vel_y = 0
            self.ball_in_play = False
    
    def draw_field(self):
        # Draw grass
        self.screen.fill(GREEN)
        
        # Draw dirt infield
        pygame.draw.ellipse(self.screen, BROWN, (250, 350, 300, 200))
        
        # Draw field lines
        pygame.draw.line(self.screen, WHITE, (250, 450), (400, 350), 3)
        pygame.draw.line(self.screen, WHITE, (400, 350), (550, 450), 3)
        pygame.draw.line(self.screen, WHITE, (550, 450), (400, 550), 3)
        pygame.draw.line(self.screen, WHITE, (400, 550), (250, 450), 3)
        
        # Draw pitcher's mound
        pygame.draw.circle(self.screen, BROWN, (400, 450), 20)
    
    def draw(self):
        self.draw_field()
        
        # Draw game objects
        self.bat.draw(self.screen)
        self.ball.draw(self.screen)
        self.pitcher.draw(self.screen)
        self.batter.draw(self.screen)
        
        for outfielder in self.outfielders:
            outfielder.draw(self.screen)
        
        for base in self.bases:
            base.draw(self.screen)
        
        # Draw home plate and batter's box
        self.home_plate.draw(self.screen)
        self.batters_box.draw(self.screen)
        
        # Draw score and instructions
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        font_small = pygame.font.Font(None, 24)
        instructions = [
            "SPACE - Swing Bat",
            "P - Pitch Ball",
            "R - Reset Game"
        ]
        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, WHITE)
            self.screen.blit(text, (10, 50 + i * 25))
        
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
    game = BaseballGame()
    game.run()
