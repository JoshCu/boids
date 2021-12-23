import math
from p5 import Vector, stroke, circle, triangle
import numpy as np


class Boid:
    def __init__(self, x, y, width, height, boid_size):
        self.position = Vector(x, y)
        vec = (np.random.rand(2) - 0.5) * 10
        self.velocity = Vector(*vec)
        self.bound_x = width
        self.bound_y = height
        vec = (np.random.rand(2) - 0.5) / 2
        self.acceleration = Vector(*vec)
        self.boid_size = boid_size

    def out_of_bounds(self):
        new_position = self.position + self.velocity
        if new_position[0] >= self.bound_x or new_position[0] <= 0:
            self.velocity[0] = 0 - self.velocity[0]
            self.acceleration[0] = 0 - self.acceleration[0]
        if new_position[1] >= self.bound_y or new_position[1] <= 0:
            self.velocity[1] = 0 - self.velocity[1]
            self.acceleration[1] = 0 - self.acceleration[1]

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration

    def show(self):
        stroke(255)
        v = self.velocity
        length = math.sqrt(v.x * v.x + v.y * v.y)
        v.x = v.x / length
        v.y = v.y / length
        x1 = self.position.x + (v.x * self.boid_size * 0.5)
        y1 = self.position.y + (0 - (v.y * self.boid_size * 0.5))
        x2 = self.position.x + (0 - (v.x * self.boid_size * 0.5))
        y2 = self.position.y + (v.y * self.boid_size * 0.5)
        x3 = self.position.x + v.x * (2 * self.boid_size)
        y3 = self.position.y + v.y * (2 * self.boid_size)
        triangle(x1, y1, x2, y2, x3, y3)
        circle(self.position.x, self.position.y, 3)
