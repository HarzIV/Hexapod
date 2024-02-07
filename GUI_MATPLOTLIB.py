import tkinter as tk
from Config.Config import *
from Simulation.model import *
from UI.GUI import Matplotlib3DPlotApp

def main():
    end_points = {"Lg0": (8,0,8),
                  "Lg1": (8,0,8),
                  "Lg2": (8,0,8),
                  "Lg3": (8,0,8),
                  "Lg4": (8,0,8),
                  "Lg5": (8,0,8)}
    
    Hex = Hexapod(origins, (5, 5, 7))
    Hex.plt_bot(angles, end_points)
    
    root = tk.Tk()

    app = Matplotlib3DPlotApp(root)
    app.generate_3d_plot(fig)

    root.mainloop()

if __name__ == "__main__":
    main()