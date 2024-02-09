import tkinter as tk
from Config.Config import *
from Simulation.model import *
from UI.GUI import Matplotlib3DPlotApp

def main():
    end_points = {"Lg0": (19.09188309,0,-19.09188309),
                  "Lg1": (0,0,-27),
                  "Lg2": (-19.09188309,0,-19.09188309),
                  "Lg3": (-19.09188309,0,19.09188309),
                  "Lg4": (0,0,27),
                  "Lg5": (19.09188309,0,19.09188309)}
    
    Hex = Hexapod(origins, Lg_lengths)
    Hex.plt_bot(angles, end_points)
    
    root = tk.Tk()

    app = Matplotlib3DPlotApp(root)
    app.generate_3d_plot(fig)

    root.mainloop()

if __name__ == "__main__":
    main()