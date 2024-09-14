import pygame

# Define colors
BLACK = (0, 0, 0)
INPUT_GREY = (47, 47, 47)
OUTPUT_GREY = (77, 77, 77)
LANE_YELLOW = (212, 190, 106)
WHITE = (255, 255, 255)

class Intersection:
    def draw(self, screen):
        # Draw the intersection
        pygame.draw.rect(screen, BLACK, (540, 300, 200, 200))

        # Draw the input lanes
        pygame.draw.rect(screen, INPUT_GREY, (0, 300, 540, 100))  # West input lane
        pygame.draw.rect(screen, INPUT_GREY, (640, 0, 100, 300))  # North input lane
        pygame.draw.rect(screen, INPUT_GREY, (540, 500, 100, 300))  # South input lane
        pygame.draw.rect(screen, INPUT_GREY, (740, 400, 540, 100))  # East input lane

        # Draw the output lanes
        pygame.draw.rect(screen, OUTPUT_GREY, (640, 500, 100, 300))  # South output lane
        pygame.draw.rect(screen, OUTPUT_GREY, (540, 0, 100, 300))  # North output lane
        pygame.draw.rect(screen, OUTPUT_GREY, (740, 300, 540, 100))  # East output lane
        pygame.draw.rect(screen, OUTPUT_GREY, (0, 400, 540, 100))  # West output lane

        # Draw the lane divider
        pygame.draw.rect(screen, LANE_YELLOW, (40, 348, 500, 5))  # West input lane
        pygame.draw.rect(screen, LANE_YELLOW, (688, 40, 5, 260))  # North input lane
        pygame.draw.rect(screen, LANE_YELLOW, (588, 500, 5, 260))  # South input lane
        pygame.draw.rect(screen, LANE_YELLOW, (740, 448, 500, 5))  # East input lane
        
        # Draw the spawn Points.
        pygame.draw.rect(screen, BLACK, (0, 310, 10, 35))  # West 1 input lane
        pygame.draw.rect(screen, BLACK, (0, 360, 10, 35))  # West 2 input lane
        
        pygame.draw.rect(screen, BLACK, (650, 0, 35, 10))  # North 1 input lane
        pygame.draw.rect(screen, BLACK, (700, 0, 35, 10))  # North 2 input lane
        
        pygame.draw.rect(screen, BLACK, (550, 790, 35, 10))  # South 1 input lane
        pygame.draw.rect(screen, BLACK, (600, 790, 35, 10))  # South 2 input lane
        
        pygame.draw.rect(screen, BLACK, (1270, 410, 10, 35))  # East 1 input lane
        pygame.draw.rect(screen, BLACK, (1270, 460,10, 35))  # East 2 input lane
        
        # Draw the Output  Points.
        pygame.draw.rect(screen, WHITE, (540, 450, 1, 1))  # West  output point
        
        pygame.draw.rect(screen, WHITE, (590, 300, 1, 1))  # North output point
        
        pygame.draw.rect(screen, WHITE, (690, 500, 1, 1))  # South output point

        pygame.draw.rect(screen, WHITE, (740, 350, 1, 1))  # East output point
