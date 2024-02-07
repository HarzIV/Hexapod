from numpy import sin, cos, arange, pi

def walking_pattern(distance, resolution=20):

    # determines the size for each step of the resolution to cover the distance
    step = distance / resolution

    adjustment_value = pi / distance

    x_pos = arange(0, distance + step, step)

    y_pos = sin(x_pos * adjustment_value)

    return x_pos, y_pos

def convert2_3d(xy_lists, angle, origin=(0,0,0)):
    # angle has to be in radians

    # Assigning variables to each value in xy_list
    x_pos, y_pos = xy_lists

    # Assigning variables to each value in origin
    xo, yo, zo = origin

    # Generating the list of converted x positions
    x_con_pos = xo + cos(angle) * x_pos

    # Generating the list of converted y positions
    y_con_pos = yo + y_pos

    # Generating the list of converted z positions
    z_con_pos = zo + sin(angle) * x_pos

    return x_con_pos, y_con_pos, z_con_pos

'''
x_pos, y_pos = walking_pattern(5)
print(convert2_3d((x_pos, y_pos), 0))
'''