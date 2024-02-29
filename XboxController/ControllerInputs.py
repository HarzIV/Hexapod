import pygame
import time

# Initialize pygame
pygame.init()

# Initialize the joystick subsystem
pygame.joystick.init()

# Check for the number of joysticks
num_joysticks = pygame.joystick.get_count()

# Initialize all detected joysticks
joysticks = [pygame.joystick.Joystick(i) for i in range(num_joysticks)]

#print(joysticks)

# Dictionary to store all button and axis states
button_positions = {"Button 0": 0,
                    "Button 1": 0,
                    "Button 2": 0,
                    "Button 3": 0,
                    "Button 4": 0,
                    "Button 5": 0,
                    "Button 6": 0,
                    "Button 7": 0,
                    "Button 8": 0,
                    "Button 9": 0,
                    "Button 10": 0,
                    "Button 11": 0,
                    "Button 12": 0,
                    "Button 13": 0,
                    "Button 14": 0,
                    "Button 15": 0,
                    "Axis 0": 0.0,
                    "Axis 1": 0.0,
                    "Axis 2": 0.0,
                    "Axis 3": 0.0,
                    "Axis 4": -1.0,
                    "Axis 5": -1.0}

# Finds the type of joystick that is connected
# returns none if the type is unknown
def get_joystick_type():
    # Dictionary for the different controller names
    controller_types = {"Xbox": "Controller (Xbox One For Windows)"}

    # Iterates through all joysticks in joysticks
    for joystick in joysticks:
        stick_name = joystick.get_name() # Current joystick

        # Iterates through all joystick types
        for types in controller_types:

            # Checks if type has been found
            if controller_types[types] == stick_name:
                return types # Returns the type

def check_connection():
    if num_joysticks == 0:
        # If the number of joysticks is 0 theres no found controller
        # and the function return False
        return False
    else:
        # If the number of joysticks is not 0 theres a controller
        # and the function return True
        return True

def get_joystick_pos(button_positions):
    # Variable to store values in
    changed_value = ()

    # Finds the pressed button or axis and their states
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            changed_value = (f"Button {event.button}", joysticks[0].get_button(event.button))
        elif event.type == pygame.JOYBUTTONUP:
            changed_value = (f"Button {event.button}", joysticks[0].get_button(event.button))
        elif event.type == pygame.JOYAXISMOTION:
            changed_value = (f"Axis {event.axis}", joysticks[0].get_axis(event.axis))

    # Try's to changed value for the changed button or axis
    try:
        pressed_button, button_value = changed_value
        #print(changed_value)

        for Button in button_positions:
            if Button == pressed_button:
                button_positions[Button] = button_value

        return True
    except:
        ValueError

def button_states():
    # Update the state of the controller
    pygame.event.pump()

    # Print button states
    for button in range(joysticks[0].get_numbuttons()):
        button_state = joysticks[0].get_button(button)
        print(f"Button {button}: {button_state}")

    # Print axis positions
    for axis in range(joysticks[0].get_numaxes()):
        axis_position = joysticks[0].get_axis(axis)
        print(f"Axis {axis}: {axis_position}")

'''while True:
    get_joystick_pos(button_positions)
    for button in button_positions:
        print(f"{button}: {button_positions[button]}")
    time.sleep(5)'''
    
'''while True:
    # Variable to store values in
    changed_value = ()

    # Finds the pressed button or axis and their states
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            changed_value = (f"Button {event.button}", joysticks[0].get_button(event.button))
            print(changed_value)
        elif event.type == pygame.JOYBUTTONUP:
            changed_value = (f"Button {event.button}", joysticks[0].get_button(event.button))
            print(changed_value)
        elif event.type == pygame.JOYAXISMOTION:
            #changed_value = (f"Axis {event.axis}", joysticks[0].get_axis(event.axis))
            pass'''