from environment import Environment
from graphics import Graphics
from time import sleep
from threading import Thread
from passenger import Passenger

ENABLE_GRAPHICS = True
running = True

env = Environment()

import numpy as np
q_table = np.zeros([21952, 4])

"""Training the agent"""

import random

# Hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1

# For plotting metrics
all_epochs = []
all_penalties = []

for i in range(1, 10001):
    state = env.reset()

    epochs, penalties, reward, = 0, 0, 0
    done = False
    
    while not done:
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample() # Explore action space
        else:
            action = np.argmax(q_table[state]) # Exploit learned values

        next_state, reward, done, info = env.step(action) 
        
        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, action] = new_value

        if reward == -10:
            penalties += 1

        state = next_state
        epochs += 1
        
    if i % 100 == 0:
        print(f"Episode: {i}")

print("Training finished.\n")

"""Evaluate agent's performance after Q-learning"""

if ENABLE_GRAPHICS:
    gra = Graphics(env)
    t = Thread(target=gra.start)
    t.start()
    sleep(0.5)

total_epochs, total_penalties = 0, 0
episodes = 100

for _ in range(episodes):
    state = env.reset()
    decoded = env.decode(state)

    print("----- STATE -----")
    print(*env.decode(state))
    print("-----------------")

    for floor in env.floors:
        floor.waiting_queue = []
    env.elevators[0].passenger_in_elevator = []
    next(decoded)
    env.elevators[0].current_floor = next(decoded)
    p = Passenger(env, next(decoded), next(decoded))
    env.floors[p.start_floor].add_person_to_waiting_queue(p)

    epochs, penalties, reward = 0, 0, 0
    
    done = False
    
    while not done:
        action = np.argmax(q_table[state])
        print(action)
        if action == 0:
            if env.elevators[0].current_floor < 6:
                env.elevators[0].go_up()
        elif action == 1:
            if env.elevators[0].current_floor > 0:
                env.elevators[0].go_down()
        elif action == 2:
            if env.elevators[0].is_passenger_waiting_on_current_floor():
                env.elevators[0].add_passenger_from_current_floor_to_elevator()
        elif action == 3:
            env.elevators[0].transfer_passenger_from_elevator_to_current_floor()

        state, reward, done, info = env.step(action)

        if reward == -10:
            penalties += 1

        env.tick()
        gra.tick()
        epochs += 1
        sleep(0.5)

    total_penalties += penalties
    total_epochs += epochs
    
    sleep(0.5)
    print("done")

print(f"Results after {episodes} episodes:")
print(f"Average timesteps per episode: {total_epochs / episodes}")
print(f"Average penalties per episode: {total_penalties / episodes}")

'''
if ENABLE_GRAPHICS:
    gra = Graphics(env)
    t = Thread(target=gra.start)
    t.start()
    sleep(0.5)

try:
    while running:
        env.tick()

        if ENABLE_GRAPHICS:
            if not t.is_alive():
                running = False
                break
            gra.tick()

        sleep(0.5)

except KeyboardInterrupt:
    print("STATISTACS SKR SKR SKAA")
finally:
    print("FIREABEND")
'''
