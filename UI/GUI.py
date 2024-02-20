import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap import Style
from functools import partial

from numpy import sin, cos, radians, pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Matplotlib3DPlotApp(tk.Tk):
    def __init__(self, angles, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Initialize root functions
        self.title("Hexapod Control Center")
        self.style = Style(theme="vapor")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Define variables
        self.angles = angles

        # Create a container to hold all the pages
        self.container = ttk.Frame(self)
        self.container.grid(row=1, column=0)

        # Frame for switching between pages
        self.pages_frame = ttk.Frame(self, style="warning")
        self.pages_frame.grid(row=0, column=0, columnspan=3, sticky='nw')

        # Frame for plot
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.grid(row=1, column=3)

        # Initialize simulation
        self.Simulation_init()

        # Page list
        self.page_list = (main_page, angle_page)

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
    
    def communication_init(self, event):
        print(str(self.communication.get()))
        
    def Simulation_init(self):
        # Initialize Dark-Mode
        plt.style.use('dark_background')

        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Set initial camera angles
        ax.view_init(elev=45, azim=90, roll=180)

        # Disable the user from changing the camera angle
        #ax.disable_mouse_rotation()

        # Hexapod animation class
        class Hexapod():

            def __init__(self, origins, lengths):
                self.lengths = lengths
                self.origins = origins
                
                # Find x, y, z limits
                leg_length = sum(self.lengths)
                self.x_lim = leg_length+self.origins["Lg0"][0]
                self.y_lim = leg_length
                self.z_lim = leg_length+self.origins["Lg4"][2]
                
                print(self.x_lim, self.y_lim, self.z_lim)

                # Initialize each leg
                self.lg0 = self.leg(self.origins["Lg0"], self.lengths)
                self.lg1 = self.leg(self.origins["Lg1"], self.lengths)
                self.lg2 = self.leg(self.origins["Lg2"], self.lengths)
                self.lg3 = self.leg(self.origins["Lg3"], self.lengths)
                self.lg4 = self.leg(self.origins["Lg4"], self.lengths)
                self.lg5 = self.leg(self.origins["Lg5"], self.lengths)
                
            def clr_plot(self):
                # Clear the plot
                ax.clear()

                # Regenerate everything that was falsely deleted
                # Disable Axis
                ax.set_axis_off()
                
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
                ax.scatter(self.origins[origin][0], self.origins[origin][1], 0, color="red")

            def plt_bot(self, angles):
                # Clear plot and generate all necessary standard structures
                self.clr_plot()
                
                # Generate all x, y, z positions for each leg
                self.lg0.plt_Leg(angles["Lg0"])
                self.lg1.plt_Leg(angles["Lg1"])
                self.lg2.plt_Leg(angles["Lg2"])
                self.lg3.plt_Leg(angles["Lg3"])
                self.lg4.plt_Leg(angles["Lg4"])
                self.lg5.plt_Leg(angles["Lg5"])

            class leg():

                def __init__(self, lg_origin, lengths):
                    self.lg_origin = lg_origin
                    self.lengths = lengths

                def calc_end_point(self, angles, accuracy=2):

                    theta0, theta1, theta2 = angles
                    theta0, theta1, theta2 = radians(theta0), radians(theta1), radians(theta2)

                    xo, yo, zo = self.lg_origin
                    L0, L1, L2 = self.lengths

                    x0_end = round((xo + cos(theta0) * L0), accuracy)
                    y0_end = yo
                    z0_end = round((zo + sin(theta0) * L0), accuracy)

                    limb0_x = [xo, x0_end]
                    limb0_y = [yo, y0_end]
                    limb0_z = [zo, z0_end]

                    x1_end = round((x0_end + cos(theta0) * cos(theta1) * L1), accuracy)
                    y1_end = round((yo + sin(theta1) * L1), accuracy)
                    z1_end = round((z0_end + sin(theta0) * cos(theta1) * L1), accuracy)

                    limb1_x = [x0_end, x1_end]
                    limb1_y = [y0_end, y1_end]
                    limb1_z = [z0_end, z1_end]
                    
                    x2_end = round((x0_end + cos(theta0) * ((cos(theta2 + pi) * L2 + L1) * cos(theta1) - (sin(theta2 + pi) * L2) * sin(theta1))), accuracy)
                    y2_end = round((yo + ((cos(theta2 + pi) * L2 + L1) * sin(theta1)) + ((sin(theta2 + pi) * L2) * cos(theta1))), accuracy)
                    z2_end = round((z0_end + sin(theta1) * ((cos(theta2 + pi) * L2 + L1) * cos(theta1) - (sin(theta2 + pi) * L2) * sin(theta1))), accuracy)

                    limb2_x = [x1_end, x2_end]
                    limb2_y = [y1_end, y2_end]
                    limb2_z = [z1_end, z2_end]

                    #print((limb0_x, limb0_y, limb0_z), (limb1_x, limb1_y, limb1_z), (limb2_x, limb2_y, limb2_z))

                    return (limb0_x, limb0_y, limb0_z), (limb1_x, limb1_y, limb1_z), (limb2_x, limb2_y, limb2_z)

                def plt_Leg(self, angles):
                    
                    limb0, limb1, limb2 = self.calc_end_point(angles)

                    x0, y0, z0 = limb0
                    x1, y1, z1 = limb1
                    x2, y2, z2 = limb2

                    ax.plot(x0, y0, z0, color="green")
                    ax.plot(x1, y1, z1, color="red")
                    ax.plot(x2, y2, z2, color="blue")
        
        origins = {"Lg0": (5, 0, -5),
                   "Lg1": (0, 0, -7),
                   "Lg2": (-5, 0, -5),
                   "Lg3": (-5, 0, 5),
                   "Lg4": (0, 0, 7),
                   "Lg5": (5, 0, 5)}

        self.Hex = Hexapod(origins, (27, 70, 120))
        self.Hex.plt_bot(self.angles)

        plt.ion()

        # Embed the plot into the Tkinter window
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.update_Simulation()
        
    def update_Simulation(self):
        self.Hex.plt_bot(angles=self.angles)
        self.canvas.draw()

class main_page(tk.Frame):
    def __init__(self, parent, style, controller):
        tk.Frame.__init__(self, parent, background=style.colors.primary)
        self.parent = parent
        self.style = style
        self.controller = controller

        # Dropdown menu variables
        self.communication_options = ["A", "B", "C"]

        # Frame for selecting all settings
        self.buttons_frame = ttk.Frame(self, style='warning')
        self.buttons_frame.grid(row=1, column=0, sticky='n', padx=(0, 10), pady=(0, 10))
        
        # Dropdown menu to set the communication method between the computer and the hexapod
        self.communication = ttk.Combobox(self.buttons_frame, values=self.communication_options, state="readonly")
        self.communication.grid(padx=5, pady=5)
        self.communication.set("Communication Type")
        self.communication.bind("<<ComboboxSelected>>", self.communication_init)

        # Create a frame for the plot
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.grid(row=1, column=1, sticky='ne', padx=10, pady=(0, 10))
    
    def communication_init(self, event):
        print(str(self.communication.get()))

class angle_page(tk.Frame):
    def __init__(self, parent, style, controller):
        tk.Frame.__init__(self, parent, background=style.colors.primary)
        self.parent = parent
        self.style = style
        self.controller = controller

        # Define variables
        self.angles = self.controller.angles

        # Remove all negative sign from the angles for a nicer visualization
        self.angles = {key: [(angle + 360) if angle < 0 else angle for angle in value] for key, value in self.angles.items()}
        
        self.angles_theta = 0 + self.angles["Lg0"][0], 0 + self.angles["Lg0"][1], 0 + self.angles["Lg0"][2]

        # Flag to indicate whether the function should execute the update logic
        self.init_flag = True

        # Create frame for the sliders setting the angles
        self.angle_frame = ttk.Frame(self)
        self.angle_frame.grid(row=0, column=0, sticky='ne', padx=(0, 10), pady=(0, 10))

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
        for (leg, angles), Frame in zip(self.angles.items(), self.Frames.values()):
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
                label.config(text=f"Theta{limb}: {angle}")
                label.grid(pady=5)

                # Generate slider name
                slider_name = f"theta{limb}_slider"

                # Generate slider
                slider = ttk.Scale(Frame, bootstyle=color, from_=0, to=360, command=partial(self.change_angles, leg=leg, angle=limb), orient=tk.HORIZONTAL)

                # Append new slider to temporary storage list
                slider_storage[slider_name] = slider

                # Configure slider
                slider.set(self.angles_theta[limb])
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

        # Update the label text with the new angle
        self.labels[leg][f"theta{angle}_label"].config(text=f"Theta{angle}: {new_angle}")

        # Rectify the angle in the angles dictionary
        self.controller.angles[leg][angle] = new_angle

        # Rectify the plot
        self.controller.update_Simulation()

    def set_init_flag(self, value):
        self.init_flag = value


def main():
    app = Matplotlib3DPlotApp(angles = {
    "Lg0": [-45, 45, 270],
    "Lg1": [-90, 45, 270],
    "Lg2": [-135, 45, 270],
    "Lg3": [-225, 45, 90],
    "Lg4": [-270, 45, 90],
    "Lg5": [-315, 45, 90]})

    app.mainloop()

if __name__ == "__main__":
    main()