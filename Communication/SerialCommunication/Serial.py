import serial
import serial.tools.list_ports
from time import sleep

def Serial_send_list(angles: list, port: str, baud=9600):

    MicroController = serial.Serial(port, baud)
    
    try:
        string = ""

        for angle in angles:
            string = string+angle
        print(string)
        MicroController.write(string.encode())
        
    except serial.SerialException as e:
        print(f"Error opening the serial port: {e}")

def Serial_send(Message, port, baud=9600):

    MicroController = serial.Serial(port, baud)
    
    try:
        # Send the message to the micro controller
        MicroController.write(Message.encode('utf-8'))

        # Close the serial port
        MicroController.close()
        
    except serial.SerialException as e:
        print(f"Error opening the serial port: {e}")

def Serial_read(port: str, baud=9600):

    MicroController = serial.Serial(port, baud)

    try:
        Message = MicroController.readline()

        Message = Message.decode("ascii")

        return Message
    
    except serial.SerialException as e:
        return e

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

def convert2serial(angles: tuple, accuracy=0):
    theta0, theta1, theta2 = angles
    theta0 = round(theta0, accuracy)
    theta1 = round(theta1, accuracy)
    theta2 = round(theta2, accuracy)
    
    theta0 = str(int(theta0)).zfill(3)
    theta1 = str(int(theta1)).zfill(3)
    theta2 = str(int(theta2)).zfill(3)
    
    serial_data = theta0 + theta1 + theta2

    return serial_data
    
print(Serial_devices())
while True:
    theta0 = int(input("Enter theta 0: ").strip())
    theta1 = int(input("Enter theta 1: ").strip())
    theta2 = int(input("Enter theta 2: ").strip())

    Message = f"{theta0}A{theta1}B{theta2}\n"

    print(Message)

    Serial_send(Message, "COM4")

    sleep(1)