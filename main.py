import pygame
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
import threading
import os

from car import Car
from signal2 import Signal, change_signal
from intersection import Intersection  # Import the Intersection class
from ui import UI  # Import the UI class
from dqn_agent import DQNAgent

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Screen dimensions
screen_width = 1280
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Traffic Simulation")

# Colors
FIELD_GREEN = (1, 131, 42)

# Create signals
signals = [
    Signal("West Signal", 540, 300, 20, 100),
    Signal("North Signal", 640, 300, 100, 20),
    Signal("East Signal", 720, 400, 20, 100),
    Signal("South Signal", 540, 480, 100, 20)
]

# Create an instance of the Intersection class
intersection = Intersection()

# Create an instance of the UI class
ui = UI()

# List to hold cars
cars = []

# Initialize the DQN agent
state_size = 8  # Example state size (number of cars in each lane + traffic light status)
action_size = 4  # Example action size (number of possible actions)
agent = DQNAgent(state_size, action_size)
batch_size = 32

# Check if the model file exists before loading
model_file = "dqn_model.weights.h5"
if os.path.exists(model_file):
    agent.load(model_file)
else:
    print(f"Model file {model_file} not found. Starting with a new model.")

# Initialize the start time
start_time = pygame.time.get_ticks()

def get_state(cars, signals):
    state = np.array([len([car for car in cars if car.lane == 'north']),
                      len([car for car in cars if car.lane == 'south']),
                      len([car for car in cars if car.lane == 'east']),
                      len([car for car in cars if car.lane == 'west']),
                      signals[0].color_index,
                      signals[1].color_index,
                      signals[2].color_index,
                      signals[3].color_index])
    return np.reshape(state, [1, state_size])

def get_reward(cars):
    total_waiting_time = sum([car.waiting_time for car in cars if car.stopped])
    return -total_waiting_time  # Negative reward for the total waiting time of stopped cars

def update_signals(signals, action):
    change_signal(signals, action)
    # pass

# def update_cars(cars, signals, delta_time, ui):
#     for car in cars[:]:
#         if car.check_signal(signals, ui):  # Check the signal for each car and update stopped status
#             if not car.stopped:
#                 ui.increment_cars_stopped(car.lane)  # Increment stopped cars counter only when the car stops
#         car.move(delta_time)  # Move the car based on the signal
#         car.draw(screen)
#         car.update_collider()
#         if car.is_off_screen():
#             cars.remove(car)
#             ui.increment_cars_passed()
#             cars_passed.append(1)  # Increment cars_passed counter only when a car leaves the screen
#             print(f"Car passed! Total cars passed: {sum(cars_passed)}")

def update_cars(cars, signals, delta_time, ui):
    for car in cars[:]:
        car.check_signal(signals, ui)  # Check the signal for each car and update stopped status
        car.move(delta_time)  # Move the car based on the signal
        car.draw(screen)
        car.update_collider()
        if car.is_off_screen():
            cars.remove(car)
            ui.increment_cars_passed()
            cars_passed.append(1)  # Increment cars_passed counter only when a car leaves the screen
            print(f"Car passed! Total cars passed: {sum(cars_passed)}")


def spawn_car():
    lane = random.choice(['north', 'south', 'east', 'west'])
    vehicle_type = random.choices(['car', 'emergency'], [0.98, 0.02])[0]
    if lane == 'north':
        spawn_point = random.choice([1, 2])
        if spawn_point == 1:
            return Car(665, 10, lane, spawn_point, vehicle_type)
        else:
            return Car(720, 10, lane, spawn_point, vehicle_type)
    elif lane == 'south':
        spawn_point = random.choice([1, 2])
        if spawn_point == 1:
            return Car(560, 790, lane, spawn_point, vehicle_type)
        else:
            return Car(615, 790, lane, spawn_point, vehicle_type)
    elif lane == 'east':
        spawn_point = random.choice([1, 2])
        if spawn_point == 1:
            return Car(1270, 420, lane, spawn_point, vehicle_type)
        else:
            return Car(1270, 475, lane, spawn_point, vehicle_type)
    elif lane == 'west':
        spawn_point = random.choice([1, 2])
        if spawn_point == 1:
            return Car(10, 320, lane, spawn_point, vehicle_type)
        else:
            return Car(10, 375, lane, spawn_point, vehicle_type)

max_cars_passed = 50  # Define the maximum number of cars that should pass to end the episode

def check_done():
    total_cars_passed = sum(cars_passed)  # Calculate the total number of cars passed
    return total_cars_passed >= max_cars_passed

# Data for plotting
waiting_times = []
cars_passed = []
total_rewards = []
generation_waiting_times = []
generation_cars_passed = []
generation_total_rewards = []

# Initialize generation counter
generation = 0

# Main loop
running = True
simulation_started = False
step_count = 0  # Initialize step counter

def train_agent():
    while running:
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)

# Start the training thread
training_thread = threading.Thread(target=train_agent)
training_thread.start()

while running:
    delta_time = clock.tick(60) / 1000.0  # 60 FPS target

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if ui.start_button.collidepoint(mouse_pos):
                simulation_started = True
                start_time = pygame.time.get_ticks()  # Reset start time when simulation starts
            if ui.save_button.collidepoint(mouse_pos):
                agent.save(model_file)
                running = False
            for signal in signals:
                if signal.rect.collidepoint(mouse_pos):
                    signal.change_color()

    screen.fill(FIELD_GREEN)
    intersection.draw(screen)
    for signal in signals:
        signal.draw(screen)
    ui.draw(screen)
    ui.draw_generation(screen, generation)  # Draw the generation
    ui.draw_save_button(screen)  # Draw the save button

    if simulation_started:
        if random.random() < 0.9:
            new_car = spawn_car()
            cars.append(new_car)
            ui.increment_cars_spawned(new_car.vehicle_type)

        # Update cars function call
        update_cars(cars, signals, delta_time, ui)
        state = get_state(cars, signals)
        action = agent.act(state)
        update_signals(signals, action)
        next_state = get_state(cars, signals)
        reward = get_reward(cars)

        waiting_times.append(np.mean([car.waiting_time for car in cars]))
        cars_passed.append(len([car for car in cars if car.is_off_screen()]))
        total_rewards.append(reward)

        done = check_done()
        if done:
            generation_waiting_times.append(np.mean(waiting_times))
            generation_cars_passed.append(sum(cars_passed))
            generation_total_rewards.append(sum(total_rewards))
            generation += 1  # Increment generation after each episode
            cars_passed.clear()  # Reset cars_passed for the next generation
            waiting_times.clear()  # Reset waiting_times for the next generation
            total_rewards.clear()  # Reset total_rewards for the next generation

        agent.remember(state, action, reward, next_state, done)

    pygame.display.flip()

pygame.quit()
training_thread.join()  # Ensure the training thread finishes

# Save the model after training
agent.save(model_file)

# Plotting the data
plt.figure(figsize=(12, 6))
plt.subplot(4, 1, 1)
plt.plot(waiting_times, label='Average Waiting Time')
plt.xlabel('Time')
plt.ylabel('Waiting Time')
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(cars_passed, label='Cars Passed')
plt.xlabel('Time')
plt.ylabel('Number of Cars')
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(total_rewards, label='Total Reward')
plt.xlabel('Time')
plt.ylabel('Reward')
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(generation_waiting_times, label='Generation Waiting Time')
plt.plot(generation_cars_passed, label='Generation Cars Passed')
plt.plot(generation_total_rewards, label='Generation Total Reward')
plt.xlabel('Generation')
plt.ylabel('Value')
plt.legend()

plt.tight_layout()
plt.show()