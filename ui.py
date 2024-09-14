import pygame

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
RED = (255, 0, 0)
TRANSPARENT_BLACK = (0, 0, 0, 128)  # Semi-transparent black

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 25)
        self.font_button = pygame.font.Font(None, 36)
        self.custom_font = pygame.font.SysFont('Comic Sans MS', 90, bold=True)  # Custom font for project name
        self.start_button = pygame.Rect(990, 30, 250, 40)
        self.cars_spawned = 0
        self.cars_passed = 0
        self.emergency_cars_spawned = 0
        self.cars_stopped_north = 0
        self.cars_stopped_east = 0
        self.cars_stopped_south = 0
        self.cars_stopped_west = 0

    def draw(self, screen):
        # Draw the start button
        pygame.draw.rect(screen, LIGHT_BLUE, self.start_button)
        start_text = self.font_button.render("Start", True, BLACK)
        screen.blit(start_text, (self.start_button.x + 100, self.start_button.y + 10))

        # Draw the semi-transparent background for counters
        self.draw_transparent_background(screen, 990, 90, 250, 130)  # Top right counters
        self.draw_transparent_background(screen, 990, 630, 250, 140)  # Bottom right counters

        # Draw the counters
        cars_spawned_text = self.font.render(f"Cars Spawned: {self.cars_spawned}", True, WHITE)
        screen.blit(cars_spawned_text, (1000, 100))

        cars_passed_text = self.font.render(f"Cars Passed: {self.cars_passed}", True, WHITE)
        screen.blit(cars_passed_text, (1000, 140))

        emergency_cars_spawned_text = self.font.render(f"Emergency Cars: {self.emergency_cars_spawned}", True, WHITE)
        screen.blit(emergency_cars_spawned_text, (1000, 180))

        # Draw the project name with custom font
        project_name_text = self.custom_font.render("Pravāhīti", True, WHITE)
        screen.blit(project_name_text, (70, 80))

        # Draw the lane stop counters at the bottom right
        # cars_stopped_north_text = self.font.render(f"North Lane Stopped: {self.cars_stopped_north}", True, WHITE)
        # screen.blit(cars_stopped_north_text, (1000, 650))

        # cars_stopped_east_text = self.font.render(f"East Lane Stopped: {self.cars_stopped_east}", True, WHITE)
        # screen.blit(cars_stopped_east_text, (1000, 680))

        # cars_stopped_south_text = self.font.render(f"South Lane Stopped: {self.cars_stopped_south}", True, WHITE)
        # screen.blit(cars_stopped_south_text, (1000, 710))

        # cars_stopped_west_text = self.font.render(f"West Lane Stopped: {self.cars_stopped_west}", True, WHITE)
        # screen.blit(cars_stopped_west_text, (1000, 740))

    def draw_transparent_background(self, screen, x, y, width, height):
        s = pygame.Surface((width, height))  # Create a surface
        s.set_alpha(128)  # Set transparency level (0-255)
        s.fill(BLACK)  # Fill the surface with black color
        screen.blit(s, (x, y))  # Blit the surface onto the screen
    
    def draw_save_button(self, screen):
        self.save_button = pygame.Rect(screen.get_width() - 290, screen.get_height() - 570, 250, 40)
        pygame.draw.rect(screen, (8, 70, 48), self.save_button)
        save_text = self.font.render("Save & Quit", True, (255, 255, 255))
        screen.blit(save_text, (screen.get_width() - 220, screen.get_height() - 560))

    def increment_cars_spawned(self, vehicle_type):
        self.cars_spawned += 1
        if vehicle_type == 'emergency':
            self.emergency_cars_spawned += 1

    def increment_cars_passed(self):
        self.cars_passed += 1

    def increment_cars_stopped(self, lane):
        if lane == 'north':
            self.cars_stopped_north += 1
        elif lane == 'east':
            self.cars_stopped_east += 1
        elif lane == 'south':
            self.cars_stopped_south += 1
        elif lane == 'west':
            self.cars_stopped_west += 1
            
    def draw_generation(self, screen, generation):
        generation_text = self.font.render(f"Generation: {generation}", True, WHITE)
        screen.blit(generation_text, (10, screen.get_height() - 30))