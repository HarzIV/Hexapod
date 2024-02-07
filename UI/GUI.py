import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from ttkbootstrap import Style

class Matplotlib3DPlotApp:
    def __init__(self, root):
        # Initialize root functions
        self.root = root
        self.root.title("Hexapod Control Center")
        self.style = Style(theme="vapor")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        '''# Create a frame for the plot
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)'''

        self.buttons_frame = ttk.Frame(self.root, bootstyle='warning')
        self.buttons_frame.grid(row=0, column=0, sticky='n', padx=10, pady=10)

        self.button1 = ttk.Button(self.buttons_frame, text="Button 1", command=self.button1_clicked)
        self.button1.pack(pady=5)

        self.button2 = ttk.Button(self.buttons_frame, text="Button 2", bootstyle="primary", command=self.button2_clicked)
        self.button2.pack(pady=5)

        # Create Button 2
        self.my_Button2 = ttk.Button(self.root, text="button!",
            bootstyle="primary, link", command=self.button1_clicked)
        self.my_Button2.grid(row=0, column=2, pady=20)

        # Create a frame for the plot
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.grid(row=0, column=1, sticky='ne', padx=10, pady=10)


        
    def generate_3d_plot(self):

        self.x_values = np.linspace(-5, 5, 100)
        self.y_values = np.linspace(-5, 5, 100)
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
    
    def on_closing(self):
        self.root.destroy()
        quit()

    def button1_clicked(self):
        print("Button 1 clicked")

    def button2_clicked(self):
        print("Button 2 clicked")

'''root = tk.Window(themename="vapor")

app = Matplotlib3DPlotApp(root)

root.mainloop()'''