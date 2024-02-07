import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Set dark mode style for the plot
plt.style.use('dark_background')

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define the starting point
start = [0, 0, 0]

# Initialize endpoint
end = np.array(start)

# Define a default length for the lines
default_length = 1

angles = []  # List to store angles for each line

# Prompt the user to enter angles for each line
for i in range(3):
    x_z_plane_angle = float(input(f"Enter the X-Z plane angle for line {i + 1} in degrees: "))
    y_rotation_angle = float(input(f"Enter the Y rotation angle for line {i + 1} in degrees: "))
    angles.append((x_z_plane_angle, y_rotation_angle))

# Plot the three connected lines
for x_z_plane_angle, y_rotation_angle in angles:
    radian_x_z_plane_angle = np.deg2rad(x_z_plane_angle)
    radian_y_rotation_angle = np.deg2rad(y_rotation_angle)

    direction = np.array([np.cos(radian_x_z_plane_angle), 0, np.sin(radian_x_z_plane_angle)])
    direction = np.dot(np.array([[np.cos(radian_y_rotation_angle), -np.sin(radian_y_rotation_angle), 0],
                                [np.sin(radian_y_rotation_angle), np.cos(radian_y_rotation_angle), 0],
                                [0, 0, 1]],), direction)

    end = end + default_length * direction
    line = np.vstack((start, end))
    ax.plot(line[:, 0], line[:, 1], line[:, 2], marker='o')

    start = end

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Connected 3D Lines with Variable Angles')

# Show the plot
plt.show()
