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

    def __init__(self, com_port, baud=9600):
        
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
        Message = f"{tag}{value}X\n"

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