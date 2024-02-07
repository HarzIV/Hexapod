import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Set dark mode style for the plot
plt.style.use('dark_background')

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def plot_Leg(lengths, angles, start = [0, 0, 0]): # lengths = [0, 0, 0] angles = [(0, 0), (0, 0), (0, 0)]
    # Initialize endpoint
    end = np.array(start)

    # Plot the three connected lines
    for i, (x_z_plane_angle, y_rotation_angle) in enumerate(angles):
        radian_x_z_plane_angle = np.deg2rad(x_z_plane_angle)
        radian_y_rotation_angle = np.deg2rad(y_rotation_angle)

        direction = np.array([np.cos(radian_x_z_plane_angle), 0, np.sin(radian_x_z_plane_angle)])
        direction = np.dot(np.array([[np.cos(radian_y_rotation_angle), -np.sin(radian_y_rotation_angle), 0],
                                    [np.sin(radian_y_rotation_angle), np.cos(radian_y_rotation_angle), 0],
                                    [0, 0, 1]],), direction)

        end = end + lengths[i] * direction
        line = np.vstack((start, end))
        ax.plot(line[:, 0], line[:, 1], line[:, 2], marker='o')

        start = end

"""plot_Leg(lengths, angles, start = [3, 5, 0])

angles = [(0, 0), (45, 0), (-45, 0)]
lengths = [3.0, 3.0, 6.0]

plot_Leg(lengths, angles, start = [5, 0, 0])

angles = [(0, -45), (45, -45), (-45, -45)]
lengths = [3.0, 3.0, 6.0]

plot_Leg(lengths, angles, start = [3, -5, 0])

# Left Side

angles = [(0, 135), (45, 135), (-45, 135)]

plot_Leg(lengths, angles, start = [-3, 5, 0])

angles = [(0, 180), (45, 180), (-45, 180)]
lengths = [3.0, 3.0, 6.0]

plot_Leg(lengths, angles, start = [-5, 0, 0])

angles = [(0, 225), (45, 225), (-45, 225)]
lengths = [3.0, 3.0, 6.0]

plot_Leg(lengths, angles, start = [-3, -5, 0])"""

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Connected 3D Lines with Variable Angles and Lengths')