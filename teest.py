import tkinter as tk
from tkinter import ttk

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ComboBox Example")
        self.geometry("300x200")

        # Create an instance of MyFrame
        self.my_frame = MyFrame(self)
        self.my_frame.pack(pady=10, padx=10)

class MyFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create a label
        self.label = tk.Label(self, text="Select an option:")
        self.label.pack(pady=5)

        # Create a combo box
        self.combo_box = ttk.Combobox(self, values=["Option 1", "Option 2", "Option 3"])
        self.combo_box.pack(pady=5)

        # Create a button to get the selected option
        self.button = tk.Button(self, text="Get Selected Option", command=self.get_selected_option)
        self.button.pack(pady=5)

    def get_selected_option(self):
        selected_option = self.combo_box.get()
        print("Selected Option:", selected_option)

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
