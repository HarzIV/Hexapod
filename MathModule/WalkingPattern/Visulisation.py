import matplotlib.pyplot as plt
from WalkingPattern import walking_pattern

def plotMatplotlib(x_data, y_data):
    """
    Plot the given data using Matplotlib.

    Parameters:
    - x_data: List of values for the x-axis.
    - y_data: List of values for the y-axis.
    """
    plt.plot(x_data, y_data)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Matplotlib Plot')
    plt.show()

# Example usage:
x_values, y_values = walking_pattern(5)

# Call the function to plot the data
plotMatplotlib(x_values, y_values)
