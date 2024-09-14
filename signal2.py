import pygame

RED = (255, 38, 40)
YELLOW = (250, 195, 0)
GREEN = (77, 253, 7)

class Signal:
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.colors = [RED, YELLOW, GREEN, YELLOW]
        self.color_index = 0  # Start with red
        self.last_change_time = pygame.time.get_ticks()

    def draw(self, screen):
        pygame.draw.rect(screen, self.colors[self.color_index], self.rect)

    def change_color(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_change_time
        print(f"Signal {self.name} - Elapsed Time: {elapsed_time} ms, Current Color: {self.colors[self.color_index]}")
        if self.color_index == 0 and elapsed_time >= 10000:  # Red signal
            self.color_index = 1  # Switch to yellow
            self.last_change_time = current_time
        elif self.color_index == 1 and elapsed_time >= 5000:  # Yellow signal
            self.color_index = 2  # Switch to green
            self.last_change_time = current_time
        elif self.color_index == 2 and elapsed_time >= 10000:  # Green signal
            self.color_index = 3  # Switch to yellow
            self.last_change_time = current_time
        elif self.color_index == 3 and elapsed_time >= 5000:  # Yellow signal
            self.color_index = 0  # Switch to red
            self.last_change_time = current_time

def change_signal(signals, index):
    for i, signal in enumerate(signals):
        if i == index:
            signal.color_index = 2  # Green
            signal.last_change_time = pygame.time.get_ticks()  # Reset the timer for the green signal
        else:
            signal.color_index = 0  # Red
            signal.last_change_time = pygame.time.get_ticks()  # Reset the timer for the red signal
