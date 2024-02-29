# Dictionary's to store dynamic variables that have multiple instances

# Dictionary to store the standart leg offset angles
offsets = {"Lg0": -45,
           "Lg1": -90,
           "Lg2": -135,
           "Lg3": -225,
           "Lg4": -270,
           "Lg5": -315}

# Dictionary to store servo angles
angles = {"Lg0": [-45, 45, 270],
          "Lg1": [-90, 45, 270],
          "Lg2": [-135, 45, 270],
          "Lg3": [-225, 45, 90],
          "Lg4": [-270, 45, 90],
          "Lg5": [-315, 45, 90]}

# Dictionary to store all origin's for the individual legs
origins = {"Lg0": (5, -5, 0),
           "Lg1": (0, -7, 0),
           "Lg2": (-5, -5, 0),
           "Lg3": (-5, 5, 0),
           "Lg4": (0, 7, 0),
           "Lg5": (5, 5, 0)}

#___________________________________________________________

# Variables to store predefined constants

# Stores the lengths for each link of the legs
# The lengths for all legs has to be the same
Lg_lengths = (27, 70, 120)

# Stores the origin of the Hexapods center point
Hex_origin = (0, 0, 0)

# Stores the offset for the coxa servo
Coxa_offset = 21

# Stores the offset for the femur servo
Femur_offset = 90

# Stores the offset for the tibia servo
Tibia_offset = 90

# Stores the motion radius of the legs in the x z plane
motion_radius = 5