#!/usr/bin/env python3

"""
This script allows you to manually control the simulator
using the keyboard arrows.
"""

import sys
import argparse
import pyglet
import math
from pyglet.window import key
from pyglet import clock
import numpy as np
import gym
import gym_miniworld
import time
import os

parser = argparse.ArgumentParser()
parser.add_argument('--env-name', default='MiniWorld-Hallway-v0')
parser.add_argument('--domain-rand', action='store_true', help='enable domain randomization')
parser.add_argument('--no-time-limit', action='store_true', help='ignore time step limits')
parser.add_argument('--top_view', action='store_true', help='show the top view instead of the agent view')
args = parser.parse_args()

env = gym.make("MiniWorld-Clarendon-v0")

env.max_episode_steps = math.inf
env.domain_rand = False

view_mode = 'top' if args.top_view else 'agent'

#env.reset()

# capture start time for reporting
start_time = time.time()

# Create the display window
env.render('pyglet', view=view_mode)

def step(action):
    print('step {}/{}: {}'.format(env.step_count+1, env.max_episode_steps, env.actions(action).name))

    obs, reward, done, info = env.step(action)

    if done:
        print('done!')
        end_time = time.time()
        save_results(reward, end_time)
        print('results saved.')
        pyglet.app.exit()
        env.close()
        #env.reset()

    env.render('pyglet', view=view_mode)

def save_results(reward, end_time):
    course, pos, g = reward
    distance = round(dist(pos,g),1)
    steps = env.step_count - 1
    duration_seconds = round(end_time - start_time)

    results = f"course: {course}\n"
    results += f"distance: {distance}\n"
    results += f"steps: {steps}\n"
    results += f"time: {duration_seconds}"

    fname = time.strftime("%d_%H:%M:%S.txt",time.localtime())
    save_as = os.path.join("results",fname)

    with open(save_as,'w') as f:
        f.write(results)

def dist(a,b):
    # manhattan distance
    x0,y0 = a
    x1,y1 = b
    return abs(x0-x1) + abs(y0-y1)

@env.unwrapped.window.event
def on_key_press(symbol, modifiers):
    """
    This handler processes keyboard commands that
    control the simulation
    """

    if symbol == key.BACKSPACE or symbol == key.SLASH:
        print('RESET')
        env.reset()
        env.render('pyglet', view=view_mode)
        return

    if symbol == key.ESCAPE:
        env.close()
        sys.exit(0)

    if symbol == key.UP:
        step(env.actions.move_forward)
    elif symbol == key.DOWN:
        step(env.actions.move_back)

    elif symbol == key.LEFT:
        step(env.actions.turn_left)
    elif symbol == key.RIGHT:
        step(env.actions.turn_right)

    elif symbol == key.PAGEUP or symbol == key.P:
        step(env.actions.pickup)
    elif symbol == key.PAGEDOWN or symbol == key.D:
        step(env.actions.drop)

    elif symbol == key.ENTER:
        step(env.actions.done)

@env.unwrapped.window.event
def on_key_release(symbol, modifiers):
    pass

@env.unwrapped.window.event
def on_draw():
    env.render('pyglet', view=view_mode)

@env.unwrapped.window.event
def on_close():
    pyglet.app.exit()

# Enter main event loop
pyglet.app.run()

env.close()
