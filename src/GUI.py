import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from functools import partial

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import time
import numpy as np

from test_OOP import *
from LegMath import *

class Matplotlib3DPlotApp(tk.Tk):
    def __init__(self, offsets, angles, origins, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Initialize root functions
        self.title("Hexapod Control Center")
        self.style = Style(theme="vapor")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(0, 0)

        # Define variables
        self.start_angles = angles

        # Create empty dictionary's
        self.old_angles = {}
        
        self.create_copy(angles, self.old_angles)

        self.new_angles = {}

        # This copy's the contents of the angles dictionary, this is done because things like
        # Creating a shallow copy through the .copy() method, setting this dictionary equal to angles
        # for some reason seems to interlink self.start_angles and self.new_angles such that a rectification
        # made to self.new_angles also rectifies self.start_angles in the exact same way
        self.create_copy(angles, self.new_angles)

        self.offsets = offsets
        
        self.origins = origins
        
        self.communication_activity = False
        
        # Variable to store initialized serial port in
        self.Hexapod_Serial = None

        # Create a container to hold all the pages
        self.container = ttk.Frame(self)
        self.container.grid(row=1, column=0)

        # Frame for switching between pages
        self.pages_frame = ttk.Frame(self, style="secondary")
        self.pages_frame.grid(row=0, column=0, columnspan=4, sticky='nsew')

        # Frame for plot
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.grid(row=1, column=3, sticky='nsew')

        # Initialize simulation
        self.Simulation_init()

        # Page list
        self.page_list = (main_page, angle_page, gate_page)

        # Page names
        self.page_names = tuple(''.join((class_str[i].capitalize() if i == 0 or not class_str[i - 1].isalpha() else class_str[i]) for i in range(len(class_str))).replace('_', ' ') for class_name in self.page_list for class_str in [class_name.__name__])

        # Page Dictionary
        self.pages = {}

        # Add pages to the dictionary
        for Page in self.page_list:
            page_name = Page.__name__
            page = Page(parent=self.container, style=self.style, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("main_page")

        # Generates all individual buttons for selecting different pages for every page class is self.page_list
        for button_name, page_class in zip(self.page_names, self.page_list):
            # Define a function that captures the current value of page_class
            def create_command(class_name):
                return lambda: self.show_page(class_name)
            
            # Create a command function using the current value of page_class
            command = create_command(page_class.__name__)
            
            # Create the button with the command function
            self.page_button = ttk.Button(self.pages_frame, text=button_name, command=command)
            self.page_button.pack(side=tk.LEFT)

    def on_closing(self):
        #self.root.destroy()
        quit()
    
    def show_page(self, page_name):
        # Show the page with the given page name
        page = self.pages[page_name]
        page.tkraise()
    
    def create_copy(self, dict, copy):
        for key, value in dict.items():
            extracted_angles = []
            for item in value:
                extracted_angles.append(item+0)
            copy[key] = extracted_angles

    def Simulation_init(self):
        # Initialize Dark-Mode
        plt.style.use('dark_background')

        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Set initial camera angles
        ax.view_init(elev=45, azim=35, roll=0)

        # Disable the user from changing the camera angle
        # ax.disable_mouse_rotation()
        
        ax.set_xlabel('xlabel', fontsize=18)
        ax.set_ylabel('ylabel', fontsize=18)
        ax.set_zlabel('zlabel', fontsize=18)
        
        class leg():

            def __init__(self, lg_origin, lengths) -> None:
                self.lg_origin = lg_origin
                self.lengths = lengths

                # Define Plot for each limb
                self.coxa, = ax.plot([], [], [], color="green")
                self.femur, = ax.plot([], [], [], color="red")
                self.tibia, = ax.plot([], [], [], color="blue")

            def update(self, limb, x, y, z):
                limb.set_data(x, y)
                limb.set_3d_properties(z)
            
            def clear_Leg(self):
                self.coxa.remove()
                self.femur.remove()
                self.tibia.remove()

            def plt_Leg(self, angles):
                
                limb0, limb1, limb2 = Forward_Kinematics(angles=angles, origin=self.lg_origin, lengths=self.lengths)

                x0, y0, z0 = limb0
                x1, y1, z1 = limb1
                x2, y2, z2 = limb2
                
                print(x2[1], y2[1], z2[1])
                print('LEG')
                
                self.update(self.coxa, x0, y0, z0)
                self.update(self.femur, x1, y1, z1)
                self.update(self.tibia, x2, y2, z2)
        
        class Hexapod():

            def __init__(self, origins, lengths, start_angels):
                self.lengths = lengths
                self.origins = origins
                self.legs = {}
                
                # Find x, y, z limits
                leg_length = sum(self.lengths)
                self.x_lim = leg_length+self.origins["Lg0"][0]
                self.y_lim = leg_length
                self.z_lim = leg_length+self.origins["Lg4"][2]
                
                # Set axis limit to prevent deformation of the plot when rectifying it
                ax.set_xlim(-self.x_lim, self.x_lim)
                ax.set_ylim(-self.y_lim, self.y_lim)
                ax.set_zlim(-self.z_lim, self.z_lim)
                
                # Leg origin wire frame
                x, y, z = [], [], []

                for origin in self.origins:
                    x.append(self.origins[origin][0])
                    y.append(self.origins[origin][1])
                    z.append(self.origins[origin][2])
                
                x.append(self.origins["Lg0"][0])
                y.append(self.origins["Lg0"][1])
                z.append(self.origins["Lg0"][2])

                ax.plot(x, y, z)

                # Front indicator
                ax.scatter(self.origins["Lg0"][0], 0, 0, color="red")

                # Initialize each leg and set plot its start position
                for key in origins.keys():
                    self.legs[key] = leg(origins[key], self.lengths)
                    self.legs[key].plt_Leg(start_angels[key])
            
            def create_plt(self):
                plot, = ax.plot([], [], [], color="pink")
                
                return plot
            
            def plt_any(self, plot, xyz: tuple[list, list, list]):
                x, y, z = xyz

                plot.set_data(x, y)
                plot.set_3d_properties(z)
            
            def del_any(self, plot) -> None:
                plot.set_data([], [])
                plot.set_3d_properties([])

            def plt_bot(self, angles, changed_legs):
                # Clear plot and generate all necessary standard structures
                # self.clr_plot()

                # Update leg plot
                for changed_leg in changed_legs:
                    self.legs[changed_leg].plt_Leg(angles[changed_leg])
                
        # self.Leg = leg(lg_origin=(0,0,0), lengths=(10, 20, 30))
        self.Hex = Hexapod(self.origins, (27, 70, 120), self.start_angles)
        
        plt.ion()

        # Embed the plot into the Tkinter window
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.update_Simulation()
        
    def update_Simulation(self):
        tstart = time.time()

        is_changed = False
        changed_legs = []

        # Finds out which legs have been altered
        for old_angles, (leg, new_angles) in zip(self.old_angles.values(), self.new_angles.items()):
            # Loop over items inside both values
            for old_angle, new_angle in zip(old_angles, new_angles):
                # Check if angle has been changed
                if not old_angle == new_angle:
                    is_changed = True
            
            # Check if any of the angles for the current leg have been changed
            if is_changed:
                # Append the changed legs id
                changed_legs.append(leg)
                
                # Rectify is_changed to be False
                is_changed = False

        # Set old_angles equal to new_angels to be able to compare the new angles,
        # to the old angles the next time
        # self.old_angles = self.new_angles
        self.create_copy(self.new_angles, self.old_angles)

        self.Hex.plt_bot(angles=self.new_angles, changed_legs=changed_legs)
        
        # Update the canvas
        self.canvas.draw()
        print('FPS: ' ,1/(time.time()-tstart))

class main_page(tk.Frame):
    def __init__(self, parent, style, controller):
        tk.Frame.__init__(self, parent, background=style.colors.primary)
        self.parent = parent
        self.style = style
        self.controller = controller

        # Dropdown menu variables
        self.communication_options = ["Bluetooth", "Wi-Fi", "Serial"]
        
        try:
            self.Serial_ports, self.Serial_devices = Serial_devices_get()
        except:
            self.Serial_ports, self.Serial_devices = (None, None)

        # Frame for selecting all settings
        self.communication_frame = ttk.Frame(self)
        self.communication_frame.grid(row=1, column=0, sticky='nw')
        
        # Dropdown menu to set the communication method between the computer and the hexapod
        self.communication = ttk.Combobox(self.communication_frame, values=self.communication_options, state="readonly")
        self.communication.grid(padx=5, pady=5)
        self.communication.set("Communication Type")
        self.communication.bind("<<ComboboxSelected>>", self.communication_type)

        # Dropdown menu to set the com port to use
        self.devices = ttk.Combobox(self.communication_frame, values=self.Serial_devices, state="readonly")
        self.devices.grid(padx=5, pady=5)
        self.devices.set("Select Device")
        self.devices.bind("<<ComboboxSelected>>", self.communication_init)
        self.devices.config(state=tk.DISABLED)
    
    def communication_type(self, event):
        # Enable devices
        self.devices.config(state="readonly")
        
        # Set communication to active
        self.controller.communication_activity = True
    
    def communication_init(self, event):
        # Check if there is on going communication and stop if
        if not self.controller.communication_activity:
            return

        # Get selected device
        device = str(self.devices.get())
        print(self.Serial_devices, self.Serial_ports)
        
        # Find index of the device in the list of devices
        index = self.Serial_devices.index(device)
        
        # Set port using the index of the selected device because both lists have the same len
        port = self.Serial_ports[index]

        print(device, port)
        
        # Initialize Serial communication
        self.controller.Hexapod_Serial = Serial(port)

class angle_page(tk.Frame):
    def __init__(self, parent, style, controller):
        tk.Frame.__init__(self, parent, background=style.colors.primary)
        self.parent = parent
        self.style = style
        self.controller = controller

        # Define variables
        self.start_angles = self.controller.start_angles
        
        self.joint_angles = {}
        
        for (key, value), offset in zip(self.start_angles.items(), self.controller.offsets.values()):
            extracted_angles = []
            for item in value:
                if value.index(item) == 0:
                    extracted_angles.append(self.joint_angle(offset, item+0))
                else:
                    extracted_angles.append(item)
            self.joint_angles[key] = extracted_angles

        print(self.joint_angles)

        self.offsets = self.controller.offsets

        # Flag to indicate whether the function should execute the update logic
        self.init_flag = True

        # Create frame for the sliders setting the angles
        self.angle_frame = ttk.Frame(self)
        self.angle_frame.grid(row=0, column=0, sticky='ne', padx=(0, 10), pady=(0, 10))

        # Create frame for plot interaction buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=0, column=1, sticky="nw")
        
        self.reset = ttk.Button(self.button_frame, text="Reset", command=self.plot_reset)
        self.reset.grid(sticky="nw")

        # Dictionary for frames for all labels and sliders
        self.Frames = {}

        # Tuple to store limb color options
        self.limb_colors = ("success", "danger", "info")

        # Dictionaries for all angle sliders
        self.sliders = {}

        # Dictionaries for all angle labels
        self.labels = {}

        # Frames for each leg
        for leg_side in range(2):
            for leg in range(3):
                # Create frame
                Frame = ttk.Frame(self.angle_frame)

                # Rectify self.Frames according to Frame
                self.Frames[f"Frame{(leg_side*3)+leg}"] = Frame

                # Configure Frame
                Frame.grid(row=leg, column=leg_side, padx=5, pady=5)

        # Generates all individual sliders and labels for changing all angels individually
        for (leg, angles), Frame in zip(self.start_angles.items(), self.Frames.values()):
            # Generate empty dictionaries to store labels and slider
            label_storage = {}
            slider_storage = {}
            
            for limb, (color, angle) in enumerate(zip(self.limb_colors, angles)):
                # Generate label name
                label_name = f"theta{limb}_label"

                # Generate label
                label = ttk.Label(Frame, bootstyle=color, text=f"Theta{limb}:")

                # Append new label
                label_storage[label_name] = label

                # Configure label
                if not limb:
                    label.config(text=f"Theta{limb}: {self.joint_angle(offset_angle=self.offsets[leg], input_angle=angle)}")
                else:
                    label.config(text=f"Theta{limb}: {angle}")
                label.grid(pady=5)

                # Generate slider name
                slider_name = f"theta{limb}_slider"

                # Generate slider
                slider = ttk.Scale(Frame, bootstyle=color, from_=0, to=180, command=partial(self.change_angles, leg=leg, angle=limb), orient=tk.HORIZONTAL)

                # Append new slider to temporary storage list
                slider_storage[slider_name] = slider

                # Configure slider
                # Check if the slider is for limb 0, if apply perspective rectification
                if not limb:
                    slider.set(self.joint_angle(offset_angle=self.offsets[leg], input_angle=angle))
                else:
                    slider.set(self.start_angles[leg][limb])

                slider.grid(pady=5)

            # Rectify main label with label_storage
            self.labels[leg] = label_storage
            
            # Rectify main sliders with slider_storage
            self.sliders[leg] = slider_storage
    
        # Set the init_flag variable to False to make the change_angles function executable
        self.init_flag = False

    def change_angles(self, value, leg, angle):
        # Check if the function should execute the update logic
        if self.init_flag:
            return

        # Convert the value to an integer
        new_angle = int(float(value))

        # This is only done for the third angle
        if angle == 2:
            value = 180 - new_angle

        # Update the label text with the new angle
        self.labels[leg][f"theta{angle}_label"].config(text=f"Theta{angle}: {new_angle}")

        # Take the offset for the current leg into consideration so the perspective of the angle matches the maths
        # This is only done for the the first angle as this is the only angle with an offset
        if angle == 0:
            new_angle = self.main_angle(offset_angle=self.offsets[leg], input_angle=new_angle)

        # Rectify the angle in the angles dictionary
        self.controller.new_angles[leg][angle] = new_angle

        # Rectify the plot
        self.controller.update_Simulation()
        
        try:
            # Generate serial message
            message = self.controller.Hexapod_Serial.Generate_message(leg, angle, value)
            print(message)

        
            # Send changed angles through serial port
            self.controller.Hexapod_Serial.Serial_print(message)
        except:
            pass
        
    def plot_reset(self):

        message = ""
        
        for name_tags, standard_angles in zip(tags.values(), self.joint_angles.values()):
            for tag, standard_angle in zip(name_tags.values(), standard_angles):
                message = message + tag + str(standard_angle)

        message = message + "X\n"

        print(message)

        try:
            self.controller.Hexapod_Serial.Serial_print(message)
        except:
            pass

        self.init_flag = True

        for leg_label, leg_slider, leg in zip(self.labels.values(), self.sliders.values(), self.joint_angles.values()):
            for angle_num, (label, slider, angle) in enumerate(zip(leg_label.values(), leg_slider.values(), leg)):
                label.config(text=f"Theta{angle_num}: {angle}")

                slider.set(angle)

        # Copy new_angles into old_angles
        self.controller.create_copy(self.controller.new_angles, self.controller.old_angles)

        # Copy start_angles into new_angles
        self.controller.create_copy(self.start_angles, self.controller.new_angles)

        # Update the simulation
        self.controller.update_Simulation()

        self.init_flag = False
        
    def main_angle(self, offset_angle, input_angle):
        return offset_angle + input_angle - 90
    
    def joint_angle(self, offset_angle, input_angle):
        return input_angle - offset_angle + 90

class gate_page(tk.Frame):
    def __init__(self, parent, style, controller) -> None:
        tk.Frame.__init__(self, parent, background=style.colors.primary)
        self.parent = parent
        self.style = style
        self.controller = controller

        # Tuple to store walking gates names
        self.walking_gates = ["Tri Gate"]
        
        # Create plot object for showing walking paths
        self.path_plot = self.controller.Hex.create_plt()

        # Frame to for buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=0, column=0, columnspan=2, sticky="nw")
        
        # Dictionary for path types
        self.path_types = {'Sinusoidal': Sinusoidal_pattern, 'Square': Square_Pattern}
        
        self.path_names = ['Sinusoidal', 'Square']
        
        # Dropdown menu to set the com port to use
        self.path = ttk.Combobox(self.button_frame, values=self.path_names, state="readonly")
        self.path.grid(padx=5)
        self.path.set("Select Path Type")
        self.path.bind("<<ComboboxSelected>>", self.gen_paths)
        
        # Button to enable or disable showing the walking path
        self.path_button = ttk.Button(self.button_frame, text='Show Path', style='success', command=self.show_path)
        self.path_button.grid(row=0, column=1, pady=5)

        # Dictionary to store buttons for each walking gate
        self.gate_buttons = {}

        # Create button for each walking gate
        for walking_gate in self.walking_gates:
            # Create button
            button = ttk.Button(self.button_frame, text=walking_gate, command=partial(self.Init_walk, walking_gate))
            button.grid(padx=5, pady=(0, 5), sticky="nw")
            button.config(state=tk.DISABLED)
            
            # Store button
            self.gate_buttons[walking_gate] = button

        # Dictionary for paths for each gate
        self.gate_paths = {}
        
    def show_path(self) -> None:
        # Switch color to opposite
        current_color = self.path_button.cget('style')
        new_color = "success.TButton" if current_color == "danger.TButton" else "danger.TButton"
        self.path_button.configure(style=new_color)
    
    def gen_paths(self, event) -> None:
        # Generate path for each gait
        for walking_gate in self.walking_gates:
            # Get path type
            path_type = str(self.path.get())

            # Generate x, y, z data
            xy_pos = self.path_types[path_type](distance=80, height=40)
            xyz_pos = convert2_3d(xy_lists=xy_pos, origin=(119.09-60, -119.09, -35.36), angle=0)
            
            self.gate_paths[walking_gate] = xyz_pos
        
        # Enable gate buttons
        for button in self.gate_buttons.values():
            button.config(state='readonly')
    
    def Init_walk(self, gait: str) -> None:
        # Get angles for specific gate
        xyz_pos = self.gate_paths[gait]
        
        # Convert x, y, z data to angles
        angles = Inverse_Kinematics(lengths=(27, 70, 120), origin=self.controller.origins['Lg0'], coordinates=xyz_pos)
        angles = turn2int(angles)

        # Get stop
        self.Stop = len(angles[0])

        # Set counter to 0
        self.counter = 0
        
        # Switch path of or on
        if self.path_button.cget('style') == 'success.TButton':
            # Draw walking path
            self.controller.Hex.plt_any(plot=self.path_plot, xyz=xyz_pos)
        else:
            # Delete path visualization
            self.controller.Hex.del_any(plot=self.path_plot)

        # Call update sim
        self.update_sim(angles)
        
    def update_sim(self, angles) -> None:
        if not self.counter == self.Stop:
            theta0_list, theta1_list, theta2_list = angles

            self.controller.new_angles["Lg0"][0] = theta0_list[self.counter]
            self.controller.new_angles["Lg0"][1] = theta1_list[self.counter]
            self.controller.new_angles["Lg0"][2] = theta2_list[self.counter]
            
            self.controller.update_Simulation()
            
            self.controller.new_angles["Lg0"][0] = theta0_list[self.counter] + 45 + 90
            self.controller.new_angles["Lg0"][2] = 180 - theta2_list[self.counter]
            
            message = self.controller.Hexapod_Serial.Generate_full_message(angles=self.controller.new_angles)
            print(message)

            self.controller.Hexapod_Serial.Serial_print(message)
            
            self.after(20, partial(self.update_sim, angles))
        
        self.counter+=1

def main() -> None:
    app = Matplotlib3DPlotApp(offsets = {"Lg0": -45,
                                         "Lg1": -90,
                                         "Lg2": -135,
                                         "Lg3": -225,
                                         "Lg4": -270,
                                         "Lg5": -315},
                              angles =  {"Lg0": [-45, 45, 90],
                                         "Lg1": [-90, 45, 90],
                                         "Lg2": [-135, 45, 90],
                                         "Lg3": [-225, 45, 90],
                                         "Lg4": [-270, 45, 90],
                                         "Lg5": [-315, 45, 90]},
                              origins = {"Lg0": (5, -5, 0),
                                         "Lg1": (0, -7, 0),
                                         "Lg2": (-5, -5, 0),
                                         "Lg3": (-5, 5, 0),
                                         "Lg4": (0, 7, 0),
                                         "Lg5": (5, 5, 0)})

    app.mainloop()

if __name__ == "__main__":
    main()