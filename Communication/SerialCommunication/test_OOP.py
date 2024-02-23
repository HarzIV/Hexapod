import serial
import serial.tools.list_ports

def Serial_devices():
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

    def Serial_send(self, Message):

        MicroController = self.MicroController

        try:
            # Send the message to the micro controller
            MicroController.write(Message.encode())
            
        except serial.SerialException as e:
            print(f"Error opening the serial port: {e}")

            return e
        
    def Generate_message(self, angles):

        Message = f"{(angles[0])}A{angles[1]}B{angles[2]}\n"

        return Message

    def Serial_close(self):

        MicroController = self.MicroController

        # Close the serial port
        MicroController.close()

com_ports, descriptions = Serial_devices()

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

    Hexapod.Serial_send(Message)