from numpy import sqrt, arctan2, pi, radians

def output(button_positions, motion_radius):

    # Assign axis states to x z coordinates
    x = button_positions["Axis 3"]
    z = button_positions["Axis 2"]

    # Translated the controller x & z position into the legs x & z position
    x_translated = x * motion_radius
    z_translated = z * motion_radius

    # Finds the distance between (0, 0)
    # and the translated x & z positions
    distance = sqrt(x_translated**2 + z_translated**2)

    # Finding the angle of the distance
    # relative to the x axis isn't the same in all quadrants
    if x >= 0:
        con_angle = arctan2(z, x)
    elif x >= 0 and z <= 0:
        con_angle = (2 * pi) + arctan2(z, x)
    else:
        con_angle = pi + arctan2(z, x)

    # Returns Calculated data
    return distance, con_angle

def compare_inputs(old_inputs, new_inputs, distance_sensitivity=0.5, angle_sensitivity=5):

    # Assign variables to each element
    old_distance, old_angles = old_inputs
    new_distance, new_angles = new_inputs

    # Check if the new and the old distance deviate by the set amount or more
    if new_distance - old_distance >= distance_sensitivity or new_distance - old_distance <= -distance_sensitivity:
        distance = True
    else:
        distance = False

    # Check if the new and the old distance deviate by the set amount in radians or more
    if new_angles - old_angles >= radians(angle_sensitivity) or new_angles - old_angles <= -radians(angle_sensitivity):
        angles = True
    else:
        angles = False

    if distance or angles:
        return False, distance, angles
    else:
        return True, distance, angles

def compare_inputsV2(considered_value, new_values, threshold=0.08):
    
    # Assign variables to each element
    considered_x, considered_y = considered_value
    new_x, new_y = new_values

    # Finding the distance between the last considered value and the new value
    distance = sqrt((considered_x-new_x)**2 + (considered_y-new_y)**2)

    if distance >= threshold:
        return True
    else:
        return False