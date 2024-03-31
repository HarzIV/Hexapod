import serial
import serial.tools.list_ports

tags = {"Lg0": {"0": "A", "1": "B", "2": "C",},
        "Lg1": {"0": "D", "1": "E", "2": "F",},
        "Lg2": {"0": "G", "1": "H", "2": "I",},
        "Lg3": {"0": "J", "1": "K", "2": "L",},
        "Lg4": {"0": "M", "1": "N", "2": "O",},
        "Lg5": {"0": "P", "1": "Q", "2": "R",}}

def Serial_devices_get():
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        # If there are no devices connected to any of the com ports
        return None
    else:
        # Lists for all found ports and their description
        com_ports = []
        descriptions = []

        # Finds all ports and their descriptions
        for port, desc, hwid in sorted(ports):
            com_ports.append(port)
            descriptions.append(desc)

        return com_ports, descriptions

class Serial():

    def __init__(self, com_port, baud=115200):
        
        self.com_port = com_port
        self.baud = baud

        self.MicroController = serial.Serial(com_port, baud)

    def Serial_print(self, Message):

        MicroController = self.MicroController

        try:
            # Send the message to the micro controller
            MicroController.write(Message.encode())
            
        except serial.SerialException as e:
            print(f"Error opening the serial port: {e}")

            return e
        
    def Generate_message(self, leg, angle, value):
        # Find tag
        tag = tags[leg][str(angle)]

        # Generate message
        Message = f"{tag}{int(float(value))}X\n"

        return Message

    def Generate_full_message(self, angles: dict[str, list]):
        # Generate empty str
        Message = ""
        
        # Parse through every legs
        for key, value in angles.items():
            # Parse through current legs values
            for i, (angle) in enumerate(value):
                # Find tag
                tag = tags[key][str(i)]
                
                # Generate message
                Message = Message + f"{tag}{angle}"
        
        Message = Message + "X\n\0"
        
        return Message
                

    def Serial_close(self):

        MicroController = self.MicroController

        # Close the serial port
        MicroController.close()

'''com_ports, descriptions = Serial_devices_get()

for i in descriptions:
    print(i)

chosen_port = int(input("Enter which device to send to: ").strip())

port = com_ports[chosen_port - 1]


Hexapod = Serial("COM10")

while True:
    theta0 = int(input("Enter theta 0: ").strip())
    theta1 = int(input("Enter theta 1: ").strip())
    theta2 = 180 - int(input("Enter theta 2: ").strip())

    angles = theta0, theta1, theta2

    Message = Hexapod.Generate_message(angles)

    print(Message)

    Hexapod.Serial_send(Message)'''
    
"""def Generate_full_message(angles: dict[str, list]):
    # Generate empty str
    Message = ""
    
    # Parse through every legs
    for key, value in angles.items():
        # Parse through current legs values
        for angle in value:
            # Find tag
            tag = tags[key][str(value.index(angle))]
            
            # Generate message
            Message = Message + f"{tag}{angle}"
    
    Message = Message + "X\n"
    
    return Message

print(Generate_full_message(angles = {"Lg0": [-45, 45, 90],
                                        "Lg1": [-90, 45, 90],
                                        "Lg2": [-135, 45, 90],
                                        "Lg3": [-225, 45, 90],
                                        "Lg4": [-270, 45, 90],
                                        "Lg5": [-315, 45, 90]}))"""