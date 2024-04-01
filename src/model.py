from ProjectMath import Forward_Kinematics

class leg:
    def __init__(self, ax, origin: tuple[float, float, float],
                           lengths: tuple[float, float, float]) -> None:
        self.ax = ax
        self.origin = origin
        self.lengths = lengths

        # Define Plot for each limb
        self.coxa, = self.ax.plot([], [], [], color="green")
        self.femur, = self.ax.plot([], [], [], color="red")
        self.tibia, = self.ax.plot([], [], [], color="blue")

    def update(self, limb, x: tuple[list[float], list[float], list[float]], 
                           y: tuple[list[float], list[float], list[float]],
                           z: tuple[list[float], list[float], list[float]]) -> None:
                           
        # Set 3d data
        limb.set_data(x, y)
        limb.set_3d_properties(z)

    def plt_Leg(self, angles: list[float, float, float]) -> None:
        
        limb0, limb1, limb2 = Forward_Kinematics(angles=angles, origin=self.origin, lengths=self.lengths)

        x0, y0, z0 = limb0
        x1, y1, z1 = limb1
        x2, y2, z2 = limb2
        
        self.update(self.coxa, x0, y0, z0)
        self.update(self.femur, x1, y1, z1)
        self.update(self.tibia, x2, y2, z2)

class Hexapod:
    def __init__(self, ax, origins: dict[str, float],
                           lengths: tuple[float, float, float],
                           start_angels: dict[str, tuple[float, float, float]]) -> None:
        self.ax = ax
        self.lengths = lengths
        self.origins = origins
        self.legs = {}
        
        # Set initial camera angles
        self.ax.view_init(elev=45, azim=35, roll=0)

        # Disable the user from changing the camera angle
        # self.ax.disable_mouse_rotation()

        self.ax.set_xlabel('xlabel', fontsize=18)
        self.ax.set_ylabel('ylabel', fontsize=18)
        self.ax.set_zlabel('zlabel', fontsize=18)
        
        # Find x, y, z limits
        leg_length = sum(self.lengths)
        self.x_lim = leg_length+self.origins["Lg0"][0]
        self.y_lim = leg_length
        self.z_lim = leg_length+self.origins["Lg4"][2]
        
        # Set axis limit to prevent deformation of the plot when rectifying it
        self.ax.set_xlim(-self.x_lim, self.x_lim)
        self.ax.set_ylim(-self.y_lim, self.y_lim)
        self.ax.set_zlim(-self.z_lim, self.z_lim)
        
        # Leg origin wire frame
        x, y, z = [], [], []

        for origin in self.origins:
            x.append(self.origins[origin][0])
            y.append(self.origins[origin][1])
            z.append(self.origins[origin][2])
        
        x.append(self.origins["Lg0"][0])
        y.append(self.origins["Lg0"][1])
        z.append(self.origins["Lg0"][2])

        self.ax.plot(x, y, z)

        # Front indicator
        self.ax.scatter(self.origins["Lg0"][0], 0, 0, color="red")

        # Initialize each leg and set plot its start position
        for key in self.origins.keys():
            self.legs[key] = leg(ax=self.ax,
                                 origin=self.origins[key],
                                 lengths=self.lengths)
            self.legs[key].plt_Leg(start_angels[key])
        
    def plt_bot(self, angles: dict[str, tuple[float, float, float]],
                        changed_legs: list[str]) -> None:
        # Update leg plot
        for changed_leg in changed_legs:
            self.legs[changed_leg].plt_Leg(angles[changed_leg])

class plt_object:
    def __init__(self, ax) -> None:
        self.obj, = ax.plot([], [], [], color="pink")
    
    def plt_any(self, xyz: tuple[list, list, list]) -> None:
        x, y, z = xyz

        self.obj.set_data(x, y)
        self.obj.set_3d_properties(z)
    
    def del_any(self) -> None:
        self.obj.set_data([], [])
        self.obj.set_3d_properties([])