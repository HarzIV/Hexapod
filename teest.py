import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from ttkbootstrap import Style

class Matplotlib3DPlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Plot in Tkinter with Bootstrap")
        
        # Apply Bootstrap style
        self.style = Style(theme='vapor')
        
        # Create a frame for buttons in column 0
        self.buttons_frame = ttk.Frame(self.root, style='warning')
        self.buttons_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        
        # Create buttons
        self.plot_button = ttk.Button(self.buttons_frame, text="Generate 3D Plot", command=self.generate_3d_plot)
        self.plot_button.pack(pady=5)

        self.button1 = ttk.Button(self.buttons_frame, text="Button 1", command=self.button1_clicked)
        self.button1.pack(pady=5)

        self.button2 = ttk.Button(self.buttons_frame, text="Button 2", command=self.button2_clicked)
        self.button2.pack(pady=5)

        # Create a frame for the plot in column 1, row 0
        self.plot_frame = ttk.Frame(self.root, style='primary.TFrame')
        self.plot_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        # Initialize variables for plot data
        self.x_values = np.linspace(-5, 5, 100)
        self.y_values = np.linspace(-5, 5, 100)

    def generate_3d_plot(self):
        # Clear any existing plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        plt.style.use('dark_background')
        
        # Create a new 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        X, Y = np.meshgrid(self.x_values, self.y_values)
        Z = np.sin(np.sqrt(X**2 + Y**2))
        ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Surface Plot')
        
        # Embed the plot into the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def button1_clicked(self):
        print("Button 1 clicked")

    def button2_clicked(self):
        print("Button 2 clicked")


def main():
    root = tk.Tk()
    app = Matplotlib3DPlotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
