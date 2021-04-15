from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import ImageTk, Image
import os

def on_configure(event):
    window.configure(scrollregion=window.bbox('all'))

root = tk.Tk()
root.title('Electronic Photo Album')
window = tk.Canvas(root, height=1080, width=1920, bg="Purple")
window.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(root, command=window.yview)
scrollbar.pack(side=tk.LEFT, fill='y')

window.configure(yscrollcommand=scrollbar.set)


window.bind('<Configure>', on_configure)

pics = []
save = []
def open_file():
        filepath = askopenfilename(filetypes=(("JPG Files", "*.jpg"), ("All Files", "*.*")))

        pics.append(filepath)
        print(filepath)
        print(len(pics))

        img = Image.open(filepath)
        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)
        panel = Label(photoUpload, image=img)
        panel.image = img
        for i in range(len(pics)):
            panel.grid(row=1+i, column=0, columnspan=100)

        if not filepath:
            return


def save_as():
    filepath = asksaveasfilename(defaultextension="jpg", filetypes=(("JPG Files", "*.jpg"), ("All Files", "*.*")))

    save.append(filepath)

    if not filepath:
        return


tabs = ttk.Notebook(window)
window.create_window((0,0), window=tabs, anchor='nw')


settings = Frame(tabs, height=500, width=500, bg="pink")
photoUpload = Frame(tabs, height=1000, width=1000, bg="black")
albumCreate = Frame(tabs, height=500, width=500, bg="green")

tabs.add(settings, text="Settings")
tabs.add(photoUpload, text="Photo Upload")
tabs.add(albumCreate, text="Album Creator")

openFile = Button(photoUpload, text="Open File", bg="white", command=open_file)
openFile.grid(row=0, column=0, sticky="ew", padx=5, pady=5)


saveAs = Button(photoUpload, text="Save as", bg="white", command=save_as)
saveAs.grid(row=0, column=1, sticky="ew", padx=5)



root.mainloop()