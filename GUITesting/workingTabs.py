from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

#initalize window

window = Tk()
window.title('Photo Album')
window.geometry("500x500")

#create a notebook called tabs to store tabs
tabs = ttk.Notebook(window)
tabs.pack(pady=0)#possible padding we can add from the top

#FUNCTION CALLS
def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Simple Text Editor - {filepath}")

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    window.title(f"Simple Text Editor - {filepath}")

txt_edit = tk.Text(window) #idk what this does but i put it in cause it was needed

#Initalize different tabs
settings = Frame(tabs, width=500, height=500, bg="pink")#bg=background color
photoUpload = Frame(tabs, width=500, height=500, bg="purple")
albumCreate = Frame(tabs, width=500, height=500, bg="green")

tabs.add(settings, text="Settings")
tabs.add(photoUpload, text="Photo Upload")
tabs.add(albumCreate, text="Album Creator")


#Initalize buttons for each tab

#SETTINGS TAB:
button1 = Button(settings, text="A Button but in the middle").pack(pady=10)

#PHOTO UPLOAD TAB:
btn_open = Button(photoUpload, text="Open", command=open_file)
btn_save = Button(photoUpload, text="Save As...", command=save_file)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)
#ALBUM CREATOR TAB:





window.mainloop()