from numpy import sqrt, arccos, arctan2, degrees
import numpy as np

class Inverse_kinematics():

    def __init__(self, lengths=(), origin=(0, 0, 0)):
        self.lengths = lengths
        self.origin = origin

    def calculation(self, coordinates: tuple):
        # Assigning variables to all element inside the tuples
        x, y, z = coordinates
        xo, yo, zo = self.origin
        L0, L1, L2 = self.lengths

        # Calculating theta0 isn't the same for all quadrants

        if np.all(x >= xo):
            theta0 = degrees(arctan2((y - yo), (x - xo)))
        else:
            theta0 = 180 + degrees(arctan2((y - yo), (x - xo)))
        
        x = sqrt((x-xo)**2+(y-yo)**2) - L0

        G = sqrt((x)**2+(z-zo)**2)

        theta2 = degrees(arccos((L1**2+L2**2-G**2)/(2*L1*L2)))

        ß = arccos((G**2+L1**2-L2**2)/(2*G*L1))
        a = arctan2((z-zo), (x-xo))

        # Calculating theta1 isn't the same for all quadrants

        if np.all(x >= xo): # Quadrants 1 & 4
            theta1 = degrees(ß + a)
        else: # Quadrants 2 & 3
            theta1 = degrees(2*(90 + a) - a + ß)
        
        # Return calculated angles
        return theta0, theta1, theta2
    
    def calculation_as_int(self, angles):
        return angles[0].astype(int), angles[1].astype(int), angles[2].astype(int)

'''lengths = (27, 70, 120)

Leg0 = Inverse_kinematics(lengths, (5, -5, 0))

print(Leg0.calculation((222, -5, 0)))

amount = 114

x_pos = np.linspace(82,190,amount)
y_pos = np.linspace(-5,-5,amount)
z_pos = np.linspace(0,0,amount)

angles = Leg0.calculation(coordinates=(x_pos,y_pos,z_pos))

angles = Leg0.calculation_as_int(angles)

print(angles[0])
print("________________")
print(angles[1])
print("________________")
print(angles[2])
print("________________")
print(angles[2][113])

print(Leg0.calculation((82,-5,0)))'''