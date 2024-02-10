import tkinter as tk
from Config.Config import *
from Simulation.model import *
from UI.GUI import Matplotlib3DPlotApp

end_points = {"Lg0": (19.09188309,0,-19.09188309),
                  "Lg1": (0,0,-27),
                  "Lg2": (-19.09188309,0,-19.09188309),
                  "Lg3": (-19.09188309,0,19.09188309),
                  "Lg4": (0,0,27),
                  "Lg5": (19.09188309,0,19.09188309)}

new_end_points = {"Lg0": (0,0,0),
                  "Lg1": (0,0,0),
                  "Lg2": (0,0,0),
                  "Lg3": (0,0,0),
                  "Lg4": (0,0,0),
                  "Lg5": (0,0,0)}

Hex = Hexapod(origins, Lg_lengths)
Hex.plt_bot(angles, end_points)

plt.ion()

root = tk.Tk()

app = Matplotlib3DPlotApp(root)
app.Simulation_init(fig)
app.update_Simulation()

def next_plot():
    Hex.plt_bot(angles, new_end_points)
    app.update_Simulation()

def main():
    
    root.after(3000, next_plot)

    root.mainloop()

if __name__ == "__main__":
    main()