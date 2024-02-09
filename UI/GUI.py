import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap import Style

'''from numpy import sin, cos, radians
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D'''

class Matplotlib3DPlotApp:
    def __init__(self, root):
        # Initialize root functions
        self.root = root
        self.root.title("Hexapod Control Center")
        self.style = Style(theme="vapor")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        #
        self.communication_options = ["A", "B", "C"]

        # Frame for selecting all settings
        self.buttons_frame = ttk.Frame(self.root, style='warning')
        self.buttons_frame.grid(row=0, column=0, sticky='n', padx=10, pady=10)

        self.button1 = ttk.Button(self.buttons_frame, text="Button 1", command=self.button1_clicked)
        self.button1.pack(pady=5)

        self.button2 = ttk.Button(self.buttons_frame, text="Button 2", command=self.button2_clicked)
        self.button2.pack(pady=5)
        
        self.selected_communication = tk.StringVar()
        self.communication = ttk.Combobox(self.buttons_frame, values=self.communication_options, textvariable=self.selected_communication, state="readonly")
        self.communication.pack(padx=5, pady=5)
        self.communication.set("Communication Type")
        self.communication.bind("<<ComboboxSelected>>", self.communication_init)

        # Create Button 2
        self.my_Button2 = ttk.Button(self.root, text="button!",
            bootstyle="primary, link", command=self.button1_clicked)
        self.my_Button2.grid(row=0, column=2, pady=20)

        # Create a frame for the plot
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.grid(row=0, column=1, sticky='ne', padx=10, pady=10)

    def on_closing(self):
        #self.root.destroy()
        quit()

    def button1_clicked(self):
        print("Button 1 clicked")

    def button2_clicked(self):
        print("Button 2 clicked")
    
    def communication_init(self, event):
        print(str(self.selected_communication.get()))
        
    def generate_3d_plot(self, fig):
        '''# Set dark mode style for the plot
        plt.style.use('dark_background')

        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot name
        #ax.set_title('Hexapod Sim')

        # Define the names for each axis
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Set initial camera angles
        #ax.view_init(elev=45, azim=45, roll=135)
        ax.view_init(elev=45, azim=90, roll=180)

        # Disable the user from changing the camera angle
        #ax.disable_mouse_rotation()

        # Disable all axis
        ax.set_axis_off()

        # Hexapod animation class
        class Hexapod():

            def __init__(self, origins, lengths):
                self.lengths = lengths
                self.origins = origins

                # Initiate each leg
                self.lg0 = self.leg(self.origins["Lg0"], self.lengths)
                self.lg1 = self.leg(self.origins["Lg1"], self.lengths)
                self.lg2 = self.leg(self.origins["Lg2"], self.lengths)
                self.lg3 = self.leg(self.origins["Lg3"], self.lengths)
                self.lg4 = self.leg(self.origins["Lg4"], self.lengths)
                self.lg5 = self.leg(self.origins["Lg5"], self.lengths)

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

            def plt_bot(self, angles, end_points):
                
                # Generate all x, y, z positions for each leg
                self.lg0.plt_Leg(angles["Lg0"], end_points["Lg0"])
                self.lg1.plt_Leg(angles["Lg1"], end_points["Lg1"])
                self.lg2.plt_Leg(angles["Lg2"], end_points["Lg2"])
                self.lg3.plt_Leg(angles["Lg3"], end_points["Lg3"])
                self.lg4.plt_Leg(angles["Lg4"], end_points["Lg4"])
                self.lg5.plt_Leg(angles["Lg5"], end_points["Lg5"])

            class leg():

                def __init__(self, lg_origin, lengths):
                    self.lg_origin = lg_origin
                    self.lengths = lengths

                def calc_end_point(self, angles, end_point, accuracy=2):

                    theta0, theta1 = angles
                    theta0, theta1 = radians(theta0), radians(theta1)

                    x2_end, y2_end, z2_end = end_point

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

                    limb2_x = [x1_end, x2_end]
                    limb2_y = [y1_end, y2_end]
                    limb2_z = [z1_end, z2_end]

                    #print((limb0_x, limb0_y, limb0_z), (limb1_x, limb1_y, limb1_z), (limb2_x, limb2_y, limb2_z))

                    return (limb0_x, limb0_y, limb0_z), (limb1_x, limb1_y, limb1_z), (limb2_x, limb2_y, limb2_z)

                def plt_Leg(self, angles, end_point):
                    
                    limb0, limb1, limb2 = self.calc_end_point(angles, end_point)

                    x0, y0, z0 = limb0
                    x1, y1, z1 = limb1
                    x2, y2, z2 = limb2

                    ax.plot(x0, y0, z0, color="green")
                    ax.plot(x1, y1, z1, color="red")
                    ax.plot(x2, y2, z2, color="blue")'''
        '''
        angles = {"Lg0": (45, 45),
                "Lg1": (90, 90),
                "Lg2": (90, 90),
                "Lg3": (90, 90),
                "Lg4": (90, 90),
                "Lg5": (90, 90)}

        Hex = Hexapod((5, 5, 7))
        Hex.plt_bot(angles, (8,0,8))
        plt.ion()
        plt.show()
        plt.pause(2)
        plt.cla()
        Hex.plt_bot(angles, (20,0,8))
        plt.show()
        plt.pause(1)
        plt.ioff()
        plt.show()
        '''

        '''end_points = {"Lg0": (8,0,8),
                  "Lg1": (8,0,8),
                  "Lg2": (8,0,8),
                  "Lg3": (8,0,8),
                  "Lg4": (8,0,8),
                  "Lg5": (8,0,8)}
        
        origins = {"Lg0": (5, 0, -5),
           "Lg1": (0, 0, -7),
           "Lg2": (-5, 0, -5),
           "Lg3": (-5, 0, 5),
           "Lg4": (0, 0, 7),
           "Lg5": (5, 0, 5)}
        
        angles = {"Lg0": (-45, 45),
          "Lg1": (-90, 45),
          "Lg2": (-135, 45),
          "Lg3": (-225, 45),
          "Lg4": (-270, 45),
          "Lg5": (-315, 45)}
    
        Hex = Hexapod(origins, (5, 5, 7))
        Hex.plt_bot(angles, end_points)'''

        # Embed the plot into the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

'''root = tk.Window(themename="vapor")

app = Matplotlib3DPlotApp(root)

root.mainloop()'''