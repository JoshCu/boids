from p5 import setup, draw, size, background, run
import numpy as np
from fast_boid import Boid
from datetime import datetime

width = 1400
height = 1200
bird_size = 10
birds = 100
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
    time = datetime.now()
    for boid in flock:
        boid.out_of_bounds()
        boid.apply_behaviour(flock)
        boid.update()
        #boid.show_vision()
        boid.show()
    print(f"\r{1/(datetime.now() - time).total_seconds()}", end="")



run(frame_rate=520)
