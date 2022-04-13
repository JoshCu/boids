from p5 import setup, draw, size, background, run
import numpy as np
from boid import Boid

width = 800
height = 800
bird_size = 10
birds = 50
flock = [
    Boid(np.random.randint(0, width),np.random.randint(0, height), width, height, bird_size)
    for _ in range(birds)
]


def setup():
    # this happens just once
    size(width, height)  # instead of create_canvas


def draw():
    # this happens every time
    background(30, 30, 47)

    for boid in flock:
        boid.out_of_bounds()
        boid.apply_behaviour(flock)
        boid.update()
        #boid.show_vision()
        boid.show()


run(frame_rate=120)
