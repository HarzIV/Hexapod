import tkinter as tk
from Config.Config import *
from Simulation.model import *
from UI.GUI import Matplotlib3DPlotApp

new_angles = {"Lg0": (0,0,0),
              "Lg1": (0,0,0),
              "Lg2": (0,0,0),
              "Lg3": (0,0,0),
              "Lg4": (0,0,0),
              "Lg5": (0,0,0)}

Hex = Hexapod(origins, Lg_lengths)
Hex.plt_bot(angles)

plt.ion()

#root = tk.Tk()

app = Matplotlib3DPlotApp(angles)
#app.Simulation_init(fig)
#app.update_Simulation()

def next_plot():
    Hex.plt_bot(new_angles)
    app.update_Simulation()
    
def angle():
    Hex.plt_bot(angles=angles)
    app.update_Simulation()
    
    #root.after(100, angle)

def main():
    
    #root.after(3000, next_plot)
    
    #root.after(100, angle)

    #root.mainloop()

    app.mainloop()

if __name__ == "__main__":
    main()