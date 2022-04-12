import numpy as np
from fast_boid import Boid

width = 800
height = 800
bird_size = 10
flock = [
    Boid(np.random.randint(0, width),np.random.randint(0, height), width, height, bird_size)
    for _ in range(50)
]

def loop():
    for boid in flock:
        boid.out_of_bounds()
        boid.apply_behaviour(flock)
        boid.update()
        #boid.show_vision()
        #boid.show()

counter = 0
while counter < 200:
    counter += 1
    loop()
