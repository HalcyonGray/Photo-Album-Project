import tkinter as tk
from tkinter.filedialog import *
from PIL import Image, ImageTk

filepath = "something"

def open_file():
    """Open an image for upload."""
    filepath = askopenfilename(
        filetypes=[("png", "*.png"), ("jpeg", "*.jpg")]
    )
    if not filepath:
        return
    preview = ImageTk.PhotoImage(Image.open(filepath))
    canvas.create_image(20, 20, anchor="NW", image=preview)



window = tk.Tk()

window.title("Photo Album Tool")

window.rowconfigure(0, minsize=1000, weight=1)

window.columnconfigure(1, minsize=1000, weight=1)

canvas = Canvas(window)



fr_buttons = tk.Frame(window)

btn_select = tk.Button(fr_buttons, text="Select Photo", command=open_file)


btn_settings = tk.Button(fr_buttons, text="Settings")

btn_select.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_settings.grid(row=0, column=1, sticky="nw", padx=5, pady=5)

fr_buttons.grid(row=0, column=0, sticky="ns")



window.mainloop()

