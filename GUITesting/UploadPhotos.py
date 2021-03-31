from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import ImageTk, Image
import os


root = tk.Tk()
root.title('Electronic Photo Album')
window = tk.Canvas(root, height=500, width=500, bg="Purple")
window.pack()

pics = []
save = []
def open_file():
    filepath = askopenfilename(filetypes=(("JPG Files", "*.jpg"), ("All Files", "*.*")))

    pics.append(filepath)
    print(filepath)

    for pic in pics:
        img = ImageTk.PhotoImage(Image.open(filepath))
        panel = Label(photoUpload, image=img)
        panel.image = img
        panel.grid(row=3, column=2, sticky="ew", padx=5)

    if not filepath:
        return


def save_as():
    filepath = asksaveasfilename(defaultextension="jpg", filetypes=(("JPG Files", "*.jpg"), ("All Files", "*.*")))

    save.append(filepath)

    if not filepath:
        return


tabs = ttk.Notebook(window)
tabs.pack(pady=0)

settings = Frame(tabs, width=500, height=500, bg="pink")
photoUpload = Frame(tabs, width=500, height=500, bg="black")
albumCreate = Frame(tabs, width=500, height=500, bg="green")

tabs.add(settings, text="Settings")
tabs.add(photoUpload, text="Photo Upload")
tabs.add(albumCreate, text="Album Creator")

openFile = Button(photoUpload, text="Open File", bg="white", command=open_file)
openFile.grid(row=0, column=0, sticky="ew", padx=5, pady=5)


saveAs = Button(photoUpload, text="Save as", bg="white", command=save_as)
saveAs.grid(row=0, column=1, sticky="ew", padx=5)



root.mainloop()