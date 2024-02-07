from time import sleep
from numpy import arange, zeros
from MathModule.InverseKinematics.math import *
from Simulation.model import *
from Communication.SerialCommunication.test_OOP import *
from Config.Config import *

'''y = arange(0, 100, 1)
x = full(len(y), 150)#77, 217, 1
z = zeros(len(y))'''

x = arange(77, 217, 1)
y = zeros(len(x))
z = zeros(len(x))

angles = {"Lg0": (45, 45),
          "Lg1": (90, 90),
          "Lg2": (90, 90),
          "Lg3": (90, 90),
          "Lg4": (90, 90),
          "Lg5": (90, 90)}

# Initialize serial communication
com_ports, descriptions = Serial_devices()

for i in descriptions:
    print(i)

chosen_port = int(input("Enter which device to send to: ").strip())

port = com_ports[chosen_port - 1]


Hexapod_serial = Serial("COM4")

# Initialize inverse kinematics
Leg0 = Inverse_kinematics(Lg_lengths)

# Enable interactive mode
plt.ion()

# Initialize Hexapod object
Hex = Hexapod(Lg_lengths)

for i in range(len(x)):
    theta0, theta1, theta2 = Leg0.calculation((x[i], y[i], z[i]))

    print(theta0, theta1, theta2)

    angles["Lg0"] = theta0, theta1

    Hex.plt_bot(angles, (x[i], y[i], z[i]))

    plt.show()

    Message = Hexapod_serial.Generate_message((round(theta0), 90 + round(theta1), 180-round(theta2)))

    print(Message)

    Hexapod_serial.Serial_send(Message)

    sleep(0.2)

print(x)

plt.ioff()
plt.show()

print(angles)

