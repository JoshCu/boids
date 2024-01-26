import math
import random
import p5
from numba import jit, float32, njit
from numba.experimental import jitclass

spec = [
    ('position_x', float32),
    ('position_y', float32),
    ('velocity_x', float32),
    ('velocity_y', float32),
    ('acceleration_x', float32),
    ('acceleration_y', float32),
    ('bound_x', float32),
    ('bound_y', float32),
    ('boid_size', float32),
    ('max_force', float32),
    ('max_speed', float32),
    ('vision', float32),
]

@njit
def calc_length(x, y):
    return math.sqrt(x * x + y * y)

@njit
def limit(x, y, max_value):
    length = calc_length(x, y)
    if length > max_value:
        return x / length * max_value, y / length * max_value
    return x, y

@njit
def align(boid, flock):
    steering_x, steering_y = 0.0, 0.0
    total = 0
    avg_velocity_x, avg_velocity_y = 0.0, 0.0
    for boid in flock:
        distance = calc_length(boid.position_x - boid.position_x, boid.position_y - boid.position_y)
        if distance < boid.vision:
            avg_velocity_x += boid.velocity_x
            avg_velocity_y += boid.velocity_y
            total += 1
    if total > 0:
        avg_velocity_x /= total
        avg_velocity_y /= total
        desired_x, desired_y = limit(avg_velocity_x, avg_velocity_y, boid.max_speed)
        steering_x = desired_x - boid.velocity_x
        steering_y = desired_y - boid.velocity_y
        steering_x, steering_y = limit(steering_x, steering_y, boid.max_force)
    return steering_x, steering_y

@njit
def cohesion(boid, flock):
    steering_x, steering_y = 0.0, 0.0
    total = 0
    center_of_mass_x, center_of_mass_y = 0.0, 0.0
    for boid in flock:
        distance = calc_length(boid.position_x - boid.position_x, boid.position_y - boid.position_y)
        if distance < boid.vision:
            center_of_mass_x += boid.position_x
            center_of_mass_y += boid.position_y
            total += 1
    if total > 0:
        center_of_mass_x /= total
        center_of_mass_y /= total
        vec_to_com_x = center_of_mass_x - boid.position_x
        vec_to_com_y = center_of_mass_y - boid.position_y
        desired_x, desired_y = limit(vec_to_com_x, vec_to_com_y, boid.max_speed)
        steering_x = desired_x - boid.velocity_x
        steering_y = desired_y - boid.velocity_y
        steering_x, steering_y = limit(steering_x, steering_y, boid.max_force)
    return steering_x, steering_y

@njit
def separation(boid, flock):
    steering_x, steering_y = 0.0, 0.0
    total = 0
    for boid in flock:
        distance = calc_length(boid.position_x - boid.position_x, boid.position_y - boid.position_y)
        if distance < boid.vision and distance > 0:
            diff_x = boid.position_x - boid.position_x
            diff_y = boid.position_y - boid.position_y
            diff_x /= distance
            diff_y /= distance
            steering_x += diff_x
            steering_y += diff_y
            total += 1
    if total > 0:
        steering_x /= total
        steering_y /= total
        steering_x, steering_y = limit(steering_x, steering_y, boid.max_speed)
        steering_x, steering_y = limit(steering_x, steering_y, boid.max_force)
    return steering_x, steering_y


@jitclass(spec)
class Boid:
    def __init__(self, x, y, width, height, boid_size):
        self.position_x = x
        self.position_y = y
        self.velocity_x = (random.random() - 0.5) * 10
        self.velocity_y = (random.random() - 0.5) * 10
        self.acceleration_x = (random.random() - 0.5) / 2
        self.acceleration_y = (random.random() - 0.5) / 2
        self.bound_x = width
        self.bound_y = height
        self.boid_size = boid_size
        self.max_force = 0.5
        self.max_speed = 5
        self.vision = 200


    def out_of_bounds(self):
        new_position_x = self.position_x + self.velocity_x
        new_position_y = self.position_y + self.velocity_y
        if new_position_x >= self.bound_x or new_position_x <= 0:
            self.velocity_x *= -1
            self.acceleration_x *= -1
        if new_position_y >= self.bound_y or new_position_y <= 0:
            self.velocity_y *= -1
            self.acceleration_y *= -1

    def apply_behaviour(self, flock):
        align_x, align_y = align(self,flock)
        cohesion_x, cohesion_y = cohesion(self,flock)
        separation_x, separation_y = separation(self,flock)

        self.acceleration_x += align_x + cohesion_x + separation_x
        self.acceleration_y += align_y + cohesion_y + separation_y

    
    def update(self):
        self.velocity_x += self.acceleration_x
        self.velocity_y += self.acceleration_y
        self.velocity_x, self.velocity_y = limit(self.velocity_x, self.velocity_y, self.max_speed)

        self.position_x += self.velocity_x
        self.position_y += self.velocity_y

        self.acceleration_x = 0
        self.acceleration_y = 0


def show(boid):
    p5.stroke(255)
    length = calc_length(boid.velocity_x, boid.velocity_y)
    X = boid.velocity_x / length
    Y = boid.velocity_y / length
    x1 = boid.position_x + (Y * boid.boid_size * 0.5)
    y1 = boid.position_y - (X * boid.boid_size * 0.5)
    x2 = boid.position_x - (Y * boid.boid_size * 0.5)
    y2 = boid.position_y + (X * boid.boid_size * 0.5)
    x3 = boid.position_x + X * (2 * boid.boid_size)
    y3 = boid.position_y + Y * (2 * boid.boid_size)
    p5.triangle(x1, y1, x2, y2, x3, y3)


