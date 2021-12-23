from p5 import setup, draw, size, background, run
import numpy as np
from boid import Boid

width = 800
height = 800
bird_size = 10
flock = [
    Boid(*np.random.rand(2) * (width + height / 2), width, height, bird_size)
    for _ in range(10)
]


def setup():
    # this happens just once
    size(width, height)  # instead of create_canvas


def draw():
    # this happens every time
    background(30, 30, 47)

    for boid in flock:
        boid.show()
        boid.out_of_bounds()
        boid.update()


run()
