from numpy import sin, cos, radians, pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

        # Initiate each leg
        self.lg0 = self.leg(self.origins["Lg0"], self.lengths)
        self.lg1 = self.leg(self.origins["Lg1"], self.lengths)
        self.lg2 = self.leg(self.origins["Lg2"], self.lengths)
        self.lg3 = self.leg(self.origins["Lg3"], self.lengths)
        self.lg4 = self.leg(self.origins["Lg4"], self.lengths)
        self.lg5 = self.leg(self.origins["Lg5"], self.lengths)
        
    def clr_plot(self):
        # Clear the plot
        ax.clear()
        
        # Disable Axis
        ax.set_axis_off()
        
        # Regenerate standard structures
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