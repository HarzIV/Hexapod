import tkinter as tk

def toggle_fullscreen(event=None):
    # Toggle fullscreen mode
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))

def exit_fullscreen(event=None):
    # Exit fullscreen mode
    root.attributes('-fullscreen', False)

root = tk.Tk()

# Define a function to handle resizing of the window
def resize(event):
    # Update the size of the widget to fill the window
    label.config(width=event.width, height=event.height)

# Bind the resize function to the resizing event of the window
root.bind("<Configure>", resize)

# Create a label widget
label = tk.Label(root, text="This is a fullscreen window")
label.pack(fill=tk.BOTH, expand=True)

# Bind the F11 key to toggle fullscreen mode
root.bind("<F11>", toggle_fullscreen)

# Bind the Escape key to exit fullscreen mode
root.bind("<Escape>", exit_fullscreen)

# Start the Tkinter event loop
root.mainloop()
