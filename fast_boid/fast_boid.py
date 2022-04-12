from recordclass import recordclass
import math
from random import random
#from p5 import Vector
import numpy as np
import p5
from functools import cache

class Vector2D(recordclass('Vector2D', ('x', 'y'))):
    __slots__ = ()

    def __abs__(self):
        return type(self)(abs(self.x), abs(self.y))

    def __int__(self):
        return type(self)(int(self.x), int(self.y))

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return type(self)(self.x * other, self.y * other)

    def __truediv__(self, other):
        return type(self)(self.x / other, self.y / other)

    def __itruediv__(self, other):
        return type(self)(self.x / other, self.y / other)

#@cache
def hashable_length(x, y):
    return math.sqrt(x * x + y * y)

def calc_length(vector):
    return (hashable_length(vector.x, vector.y))

class Boid:
    def __init__(self, x, y, width, height, boid_size):
        self.position = Vector2D(x, y)
        self.velocity = Vector2D((random() - 0.5) * 5, (random() - 0.5) * 5)
        self.bound_x = width
        self.bound_y = height
        self.acceleration = Vector2D(random() *.1, random() *.1)
        self.boid_size = boid_size
        self.max_force = 0.001
        self.max_speed = 1
        self.vision = 200



    def out_of_bounds(self):
        new_position = self.position + self.velocity
        if new_position.x >= self.bound_x or new_position.x <= 0:
            self.velocity.x = 0 - self.velocity.x
            self.acceleration.x = 0 - self.acceleration.x
        if new_position.y >= self.bound_y or new_position.y <= 0:
            self.velocity.y = 0 - self.velocity.y
            self.acceleration.y = 0 - self.acceleration.y

    def align(self, boids):
        steering = Vector2D(0,0)
        total = 0
        avg_vector = Vector2D(0,0)
        for boid in boids:
            if calc_length(boid.position - self.position) < self.vision:
                avg_vector += boid.velocity
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = Vector2D(*avg_vector)
            avg_vector = (avg_vector / calc_length(avg_vector)) * self.max_speed
            steering = avg_vector - self.velocity

        return steering

    def cohesion(self, boids):
        cohesion_force = self.max_force * 0.5
        steering = Vector2D(0,0)
        total = 0
        center_of_mass = Vector2D(0,0)
        for boid in boids:
            if calc_length(boid.position - self.position) < self.vision:
                center_of_mass += boid.position
                total += 1
        if total > 0:
            center_of_mass /= total
            center_of_mass = Vector2D(*center_of_mass)
            vec_to_com = center_of_mass - self.position
            if calc_length(vec_to_com) > 0:
                vec_to_com = (vec_to_com / calc_length(vec_to_com)) * self.max_speed
            steering = vec_to_com - self.velocity
            if calc_length(steering)> cohesion_force:
                steering = (steering /calc_length(steering)) * cohesion_force

        return steering

    def separation(self, boids):
        steering = Vector2D(0,0)
        total = 0
        avg_vector = Vector2D(0,0)
        for boid in boids:
            distance = calc_length(boid.position - self.position)
            if self.position != boid.position and distance < self.vision:
                diff = self.position - boid.position
                diff /= distance
                avg_vector += diff
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = Vector2D(*avg_vector)
            if calc_length(steering) > 0:
                avg_vector = (avg_vector / calc_length(steering)) * self.max_speed
            steering = avg_vector - self.velocity
            if calc_length(steering) > self.max_force:
                steering = (steering /calc_length(steering)) * self.max_force

        return steering
        
    def apply_behaviour(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)

        #self.acceleration += alignment
        self.acceleration += cohesion
        #self.acceleration += separation

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration

    def show(self):
        p5.stroke(255)
        v = self.velocity
        length = math.sqrt(v.x * v.x + v.y * v.y)
        v.x = v.x / length
        v.y = v.y / length
        x1 = self.position.x + (v.y * self.boid_size * 0.5)
        y1 = self.position.y + (0 - (v.x * self.boid_size * 0.5))
        x2 = self.position.x + (0 - (v.y * self.boid_size * 0.5))
        y2 = self.position.y + (v.x * self.boid_size * 0.5)
        x3 = self.position.x + v.x * (2 * self.boid_size)
        y3 = self.position.y + v.y * (2 * self.boid_size)
        p5.triangle(x1, y1, x2, y2, x3, y3)

    def show_vision(self):
        p5.stroke(180)
        p5.no_fill()
        p5.circle(self.position.x, self.position.y, self.vision)

