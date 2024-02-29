from src.ConI2 import *
from src.Config import *
from src.ControllerInputs import *
from time import sleep

get_joystick_pos(button_positions)
old = output(button_positions, motion_radius)

while True:
    get_joystick_pos(button_positions)

    new = output(button_positions, motion_radius)

    comparison_state = compare_inputs(old, new)

    if not comparison_state[0]:
        print(comparison_state)
        print("______________")

    old = new

    sleep(0.02)