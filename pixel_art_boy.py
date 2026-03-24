import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKIN = (255, 220, 177)
BROWN = (139, 69, 19)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

def draw_pixel_art_boy(surface, x, y):
    # Draw head (12x12 pixels for more detail)
    head_pixels = [
        [0,0,0,1,1,1,1,1,1,0,0,0],
        [0,0,1,2,2,2,2,2,2,1,0,0],
        [0,1,2,2,2,2,2,2,2,2,1,0],
        [1,2,2,1,3,3,3,3,1,2,2,1],
        [1,2,1,3,4,4,4,4,3,1,2,1],
        [1,2,1,3,4,4,4,4,3,1,2,1],
        [1,2,1,3,3,3,3,3,3,1,2,1],
        [1,2,1,1,3,5,5,3,1,1,2,1],
        [1,2,1,1,1,5,5,1,1,1,2,1],
        [0,1,2,2,2,2,2,2,2,2,1,0],
        [0,0,1,2,2,2,2,2,2,1,0,0],
        [0,0,0,1,1,1,1,1,1,0,0,0]
    ]
    
    # Enhanced color mapping with shading
    colors = {
        0: None,           # Transparent
        1: SKIN,           # Base skin
        2: (139, 90, 43),  # Darker hair (more realistic brown)
        3: (0, 0, 0),      # Eyes/mouth
        4: (100, 150, 200), # Eye color (blue)
        5: (200, 100, 100) # Mouth/tongue color
    }
    
    # Draw head with smaller pixels for more detail
    pixel_size = 3
    for row_idx, row in enumerate(head_pixels):
        for col_idx, pixel in enumerate(row):
            if colors[pixel] is not None:
                pygame.draw.rect(surface, colors[pixel], 
                               (x + col_idx * pixel_size, 
                                y + row_idx * pixel_size, 
                                pixel_size, pixel_size))
    
    # Draw neck
    pygame.draw.rect(surface, SKIN, (x + 18, y + 36, 12, 8))
    
    # Draw body with more realistic clothing
    # Enhanced shirt with better design
    shirt_pixels = [
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,2,2,2,1,1,2,2,2,1,1,0],
        [1,1,2,2,2,2,1,1,2,2,2,2,1,1],
        [1,1,2,2,2,2,1,1,2,2,2,2,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,3,3,3,3,4,4,3,3,3,3,1,1],
        [1,1,3,3,3,3,4,4,3,3,3,3,1,1],
        [1,1,5,5,5,5,5,5,5,5,5,5,1,1],
        [1,1,5,5,5,5,5,5,5,5,5,5,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,0,0]
    ]
    
    shirt_colors = {
        0: None,
        1: (70, 130, 180),   # More realistic blue shirt
        2: (255, 220, 100),  # Gold/yellow design
        3: (220, 20, 60),     # Darker red for graphics
        4: (255, 255, 255),   # White accents
        5: (50, 50, 150)      # Dark blue for shadow/detail
    }
    
    # Draw enhanced shirt
    for row_idx, row in enumerate(shirt_pixels):
        for col_idx, pixel in enumerate(row):
            if shirt_colors[pixel] is not None:
                pygame.draw.rect(surface, shirt_colors[pixel], 
                               (x - 12 + col_idx * pixel_size, 
                                y + 44 + row_idx * pixel_size, 
                                pixel_size, pixel_size))
    
    # Draw more realistic arms
    # Left arm with better proportions
    pygame.draw.rect(surface, SKIN, (x - 18, y + 44, 10, 25))
    pygame.draw.rect(surface, (70, 130, 180), (x - 18, y + 56, 10, 18))
    # Hand
    pygame.draw.circle(surface, SKIN, (x - 13, y + 78), 6)
    
    # Right arm with better proportions
    pygame.draw.rect(surface, SKIN, (x + 32, y + 44, 10, 25))
    pygame.draw.rect(surface, (70, 130, 180), (x + 32, y + 56, 10, 18))
    # Hand
    pygame.draw.circle(surface, SKIN, (x + 37, y + 78), 6)
    
    # Draw realistic pants with better fit
    pygame.draw.rect(surface, (80, 80, 80), (x - 8, y + 80, 36, 30))
    pygame.draw.rect(surface, (40, 40, 40), (x - 8, y + 80, 36, 3))  # Belt
    
    # Add pockets for realism
    pygame.draw.rect(surface, (60, 60, 60), (x - 5, y + 90, 8, 6))
    pygame.draw.rect(surface, (60, 60, 60), (x + 15, y + 90, 8, 6))
    
    # Draw more realistic legs
    # Left leg
    pygame.draw.rect(surface, SKIN, (x - 2, y + 110, 12, 25))
    pygame.draw.rect(surface, SKIN, (x - 2, y + 132, 8, 3))  # Ankle detail
    
    # Right leg
    pygame.draw.rect(surface, SKIN, (x + 18, y + 110, 12, 25))
    pygame.draw.rect(surface, SKIN, (x + 22, y + 132, 8, 3))  # Ankle detail
    
    # Draw more realistic shoes
    # Left shoe with better shape
    pygame.draw.ellipse(surface, (20, 20, 20), (x - 6, y + 133, 20, 10))
    pygame.draw.ellipse(surface, (40, 40, 40), (x - 4, y + 135, 16, 6))
    
    # Right shoe with better shape
    pygame.draw.ellipse(surface, (20, 20, 20), (x + 16, y + 133, 20, 10))
    pygame.draw.ellipse(surface, (40, 40, 40), (x + 18, y + 135, 16, 6))
    
    # Add shoelaces for detail
    pygame.draw.line(surface, WHITE, (x + 2, y + 137), (x + 8, y + 137), 1)
    pygame.draw.line(surface, WHITE, (x + 24, y + 137), (x + 30, y + 137), 1)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Art Boy")
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BLACK)
        
        # Draw the static pixel art boy
        draw_pixel_art_boy(screen, SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 50)
        
        # Draw title
        font = pygame.font.Font(None, 36)
        title_text = font.render("Pixel Art Boy", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - 80, 30))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
