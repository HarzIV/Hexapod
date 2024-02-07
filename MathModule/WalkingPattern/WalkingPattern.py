from numpy import sin, arange, pi
import numpy as np

generate_zeros = lambda x: [0] * x

def walking_pattern(distance, resolution=20):
    step = distance/resolution

    wp_x = arange(0, distance+step, step)

    A = pi/distance

    wp_y = sin(wp_x * A)

    wp_x = wp_x.tolist() + arange(distance, -step, -step).tolist()

    wp_y = wp_y.tolist() + generate_zeros(resolution+1)

    return wp_x, wp_y