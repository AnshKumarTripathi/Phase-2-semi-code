import pygame
import random
from signal2 import RED,YELLOW
from ui import UI

LIGHT_BLUE = (173, 216, 230)
LIGHT_RED = (204, 89, 89)

class Car:
    def __init__(self, x, y, lane, spawn_point, vehicle_type):
        self.x = x
        self.y = y
        self.radius = 15
        self.vehicle_type = vehicle_type
        self.color = LIGHT_BLUE if vehicle_type == 'car' else LIGHT_RED
        self.collider = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.lane = lane
        self.spawn_point = spawn_point
        self.path = None  # Path is initially None
        self.speed = 100  # Adjusted speed to 100 pixels per second
        self.target_x = None
        self.target_y = None
        self.crossed_target = False  # Flag to check if the car has crossed the target
        self.stopped = False  # Flag to check if the car is stopped
        self.waiting_time = 0  # Initialize waiting time
        self.counted_as_stopped = False  # Flag to check if the car has been counted as stopped

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def update_collider(self):
        self.collider = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def move_to_intersection(self, delta_time):
        distance = self.speed * delta_time
        if self.lane == 'north':
            self.y += distance
        elif self.lane == 'south':
            self.y -= distance
        elif self.lane == 'east':
            self.x -= distance
        elif self.lane == 'west':
            self.x += distance

    def choose_path(self):
        if self.lane == 'north':
            self.path = random.choices(['u_turn', 'straight', 'right'], [0.2, 0.4, 0.4])[0] if self.spawn_point == 1 else random.choices(['straight', 'left'], [0.5, 0.5])[0]
        elif self.lane == 'south':
            self.path = random.choices(['u_turn', 'straight', 'right'], [0.2, 0.4, 0.4])[0] if self.spawn_point == 2 else random.choices(['straight', 'left'], [0.5, 0.5])[0]
        elif self.lane == 'east':
            self.path = random.choices(['u_turn', 'straight', 'right'], [0.2, 0.4, 0.4])[0] if self.spawn_point == 1 else random.choices(['straight', 'left'], [0.5, 0.5])[0]
        elif self.lane == 'west':
            self.path = random.choices(['u_turn', 'straight', 'right'], [0.2, 0.4, 0.4])[0] if self.spawn_point == 1 else random.choices(['straight', 'left'], [0.5, 0.5])[0]
        self.set_target()

    def set_target(self):
        targets = {
            'north': {'straight': (690, 500), 'right': (740, 350), 'left': (540, 450), 'u_turn': (590, 300)},
            'south': {'straight': (590, 300), 'right': (540, 450), 'left': (740, 350), 'u_turn': (690, 500)},
            'east': {'straight': (540, 450), 'right': (590, 300), 'left': (690, 500), 'u_turn': (740, 350)},
            'west': {'straight': (740, 350), 'right': (690, 500), 'left': (590, 300), 'u_turn': (540, 450)}
        }
        self.target_x, self.target_y = targets[self.lane][self.path]

    def move(self, delta_time):
        if not self.stopped:
            self.waiting_time = 0  # Reset waiting time when the car is moving
            distance = self.speed * delta_time
            if self.path is None:
                if self.is_at_intersection():
                    self.choose_path()
                else:
                    self.move_to_intersection(delta_time)
            else:
                if not self.crossed_target:
                    if self.target_x is not None and self.target_y is not None:
                        direction_x = self.target_x - self.x
                        direction_y = self.target_y - self.y
                        distance_to_target = (direction_x**2 + direction_y**2)**0.5
                        if distance_to_target > distance:
                            self.x += distance * direction_x / distance_to_target
                            self.y += distance * direction_y / distance_to_target
                        else:
                            self.x, self.y = self.target_x, self.target_y
                            self.crossed_target = True
                else:
                    self.continue_moving(delta_time)
        else:
            self.waiting_time += delta_time  # Increment waiting time when the car is stopped

    def continue_moving(self, delta_time):
        distance = self.speed * delta_time
        if self.path == 'straight':
            if self.lane == 'north':
                self.y += distance
            elif self.lane == 'south':
                self.y -= distance
            elif self.lane == 'east':
                self.x -= distance
            elif self.lane == 'west':
                self.x += distance
        elif self.path == 'right':
            if self.lane == 'north':
                self.x += distance
            elif self.lane == 'south':
                self.x -= distance
            elif self.lane == 'east':
                self.y -= distance
            elif self.lane == 'west':
                self.y += distance
        elif self.path == 'left':
            if self.lane == 'north':
                self.x -= distance
            elif self.lane == 'south':
                self.x += distance
            elif self.lane == 'east':
                self.y += distance
            elif self.lane == 'west':
                self.y -= distance
        elif self.path == 'u_turn':
            if self.lane == 'north':
                self.y -= distance
            elif self.lane == 'south':
                self.y += distance
            elif self.lane == 'east':
                self.x += distance
            elif self.lane == 'west':
                self.x -= distance

    def is_at_intersection(self):
        return (540 <= self.x <= 740) and (300 <= self.y <= 500)
    
    def is_off_screen(self):
        return (self.x < 0 or self.x > 1280 or self.y < 0 or self.y > 800)

    def check_signal(self, signals, ui):
        for signal in signals:
            if signal.rect.collidepoint(self.x, self.y):
                if signal.colors[signal.color_index] == RED or signal.colors[signal.color_index] == YELLOW:  # Red or Yellow signal
                    if not self.stopped:
                        self.stopped = True
                        if not self.counted_as_stopped:
                            # ui.increment_cars_stopped(self.lane)  # Increment stopped cars counter only once
                            self.counted_as_stopped = True
                        return True  # Car has just stopped
                else:
                    self.stopped = False
                    self.counted_as_stopped = False  # Reset the flag when the car starts moving
        return False  # Car is not stopped

