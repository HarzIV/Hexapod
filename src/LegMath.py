from numpy import sqrt, sin, cos, arccos, arctan2, degrees, radians, pi, all, arange, array

# Inverse Kinematics For Hexapod Leg
def Inverse_Kinematics(origin: tuple[float, float, float], lengths: tuple[float, float, float], coordinates: tuple[float, float, float]) -> tuple[float, float, float]:
    # Assigning variables to all element inside the tuples
    x, y, z = coordinates
    xo, yo, zo = origin
    L0, L1, L2 = lengths

    # Calculating theta0 isn't the same for all quadrants

    if all(x >= xo):
        theta0 = degrees(arctan2((y - yo), (x - xo)))
    else:
        theta0 = 180 + degrees(arctan2((y - yo), (x - xo)))
    
    x = sqrt((x-xo)**2+(y-yo)**2) - L0

    G = sqrt((x)**2+(z-zo)**2)

    theta2 = degrees(arccos((L1**2+L2**2-G**2)/(2*L1*L2)))

    ß = arccos((G**2+L1**2-L2**2)/(2*G*L1))
    a = arctan2((z-zo), (x-xo))

    # Calculating theta1 isn't the same for all quadrants

    if all(x >= xo): # Quadrants 1 & 4
        theta1 = degrees(ß + a)
    else: # Quadrants 2 & 3
        theta1 = degrees(2*(90 + a) - a + ß)

    return theta0, theta1, theta2

def Forward_Kinematics(origin: tuple[float, float, float], lengths: tuple[float, float, float], angles: list[float], accuracy: int=2) -> tuple[list[float], list[float], list[float]]:

    theta0, theta1, theta2 = angles
    theta0, theta1, theta2 = radians(theta0), radians(theta1), radians(theta2)

    xo, yo, zo = origin
    L0, L1, L2 = lengths

    x0_end = round((xo + cos(theta0) * L0), accuracy)
    y0_end = round((yo + sin(theta0) * L0), accuracy)
    z0_end = zo

    limb0_x = [xo, x0_end]
    limb0_y = [yo, y0_end]
    limb0_z = [zo, z0_end]

    x1_end = round((x0_end + cos(theta0) * cos(theta1) * L1), accuracy)
    y1_end = round((y0_end + sin(theta0) * cos(theta1) * L1), accuracy)
    z1_end = round((zo + sin(theta1) * L1), accuracy)

    limb1_x = [x0_end, x1_end]
    limb1_y = [y0_end, y1_end]
    limb1_z = [z0_end, z1_end]
    
    x2_end = round((x0_end + cos(theta0) * ((cos(theta2 - pi) * L2 + L1) * cos(theta1) - (sin(theta2 - pi) * L2) * sin(theta1))), accuracy)
    y2_end = round((y0_end + sin(theta0) * ((cos(theta2 - pi) * L2 + L1) * cos(theta1) - (sin(theta2 - pi) * L2) * sin(theta1))), accuracy)
    z2_end = round((zo + ((cos(theta2 - pi) * L2 + L1) * sin(theta1)) + ((sin(theta2 - pi) * L2) * cos(theta1))), accuracy)

    limb2_x = [x1_end, x2_end]
    limb2_y = [y1_end, y2_end]
    limb2_z = [z1_end, z2_end]

    return (limb0_x, limb0_y, limb0_z), (limb1_x, limb1_y, limb1_z), (limb2_x, limb2_y, limb2_z)

def turn2int(angles):
    return angles[0].astype(int), angles[1].astype(int), angles[2].astype(int)

# Generate Sinusoidal Walking Pattern
def Sinusoidal_pattern(distance: float, resolution: int=20) -> tuple[float, float]:
    # determines the size for each step of the resolution to cover the distance
    step = distance / resolution

    adjustment_value = pi / distance

    x_pos = arange(0, distance + step, step)

    y_pos = sin(x_pos * adjustment_value)

    return x_pos, y_pos

def Square_Pattern(distance: float, height: float=10) -> tuple[float, float]:

    x_pos = array([0, 0, distance, distance])
    y_pos = array([0, height, height, 0])

    return x_pos, y_pos

# Rotate And Position Walking Pattern
def convert2_3d(xy_lists, angle: float, origin=(0,0,0)) -> tuple[float, float, float]:
    # Angle has to be in radians
    angle = radians(angle)

    # Assigning variables to each value in xy_list
    x_pos, y_pos = xy_lists

    # Assigning variables to each value in origin
    xo, yo, zo = origin

    # Generating x, y, z values
    x = xo + cos(angle) * x_pos
    y = yo + sin(angle) * x_pos
    z = zo + y_pos

    return x, y, z
