from MathModule.Controller_Input_Interpretation.ConI2 import *
from Config.Config import *
from XboxController.ControllerInputs import *
from time import sleep

get_joystick_pos(button_positions)
considered = (button_positions["Axis 3"], button_positions["Axis 2"])

while True:
    get_joystick_pos(button_positions)

    new = (button_positions["Axis 3"], button_positions["Axis 2"])

    comparison_state = compare_inputsV2(considered, new)

    if comparison_state:
        considered = new
        print("---------")
        print(new)
        print("---------")


    sleep(0.02)