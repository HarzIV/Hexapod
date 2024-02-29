from src.ControllerInputs import get_joystick_pos, button_positions
from src.model import *
from src.math import *
from src.ConI2 import output
from src.Config import *
from src.test_OOP import *

# Initialize serial communication
com_ports, descriptions = Serial_devices()

for i in descriptions:
    print(i)

chosen_port = int(input("Enter which device to send to: ").strip())

port = com_ports[chosen_port - 1]


Hexapod_serial = Serial("COM4")

origin = (0,0,0)

lengths = (27, 70, 120)

Hex = Hexapod((lengths))
plt.ion()
'''
while True:
    if get_joystick_pos(button_positions):
        x, z, force = output(button_positions, 2)
        print(x, z, force)
'''

ax.view_init(0, -45)

Leg0 = Inverse_kinematics(lengths, origin)

while True:

    x = float(input("x: "))
    y = float(input("y: "))
    z = float(input("z: "))

    '''elevation = float(input("elevation: "))
    azimuth = float(input("azimuth: "))
    roll = float(input("roll: "))
    
    ax.view_init(elevation, azimuth, roll)'''

    plt.cla()

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    
    theta0, theta1, theta2 = Leg0.calculation((x, y, z))

    print(theta0, theta1, theta2)

    angles["Lg0"] = theta0, theta1

    ax.scatter(x, y, z)
    ax.scatter(0,0,0)

    Hex.plt_bot(angles, (x, y, z))

    plt.show()


    Message = Hexapod_serial.Generate_message((round(theta0), 90 + round(theta1), 180-round(theta2)))

    print(Message)

    Hexapod_serial.Serial_send(Message)


    #port = Serial_devices()[0]
    #print(port)

    #Serial_send(angles, "COM5")