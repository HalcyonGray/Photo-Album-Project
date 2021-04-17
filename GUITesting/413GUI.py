from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
import os
#initalize window

window = Tk()
window.title('Photo Album')
window.geometry("500x500")

#create a notebook called tabs to store tabs
tabs = ttk.Notebook(window)
tabs.pack(pady=0)#possible padding we can add from the top
photolist = []
tag_var = StringVar()
photobuttonlist = []
photo_var = [] #true/false stack for tag upload
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

def open_dir():
    """open dir for photos"""
    filepath = askdirectory()
    if not filepath:
        return
    for root, dirs, files in os.walk(filepath): #all .png in folder
        for file in files:
            if file.endswith(".png") | file.endswith(".jpeg"):
                    photolist.append(os.path.join(root, file))


    '''img = Image.open(filepath)
    img.thumbnail((400, 400))
    img = ImageTk.PhotoImage(img)
    panel = Label(photoUpload, image=img)
    panel.image = img'''

    for i,j in enumerate(photolist):
        var = IntVar()
        c = Checkbutton(photoUpload, text=j, variable = var)
        c.grid(row=3+i, column=0, columnspan=100)
        photobuttonlist.append([j.strip(),var,c])
    '''for i in range(len(photolist)):
        panel.grid(row=3+i, column=0, columnspan=100)'''
    if not filepath:
        return
    
def save_Tag():
    """tag input for photo upload to database, etc."""
    tag = tag_var.get()
    #operations here
    '''for i in photobuttonlist:
        if i[1].get()==0:
            # upload to database with tag
            i[2].destroy()'''
    tag_var.set("")

""" Not sure what this is for ~ Grayson
def save_file():
    #Save the current file as a new file.
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
"""
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
btn_dataedit = Button(settings, text="Database Edit", bd=40, font=18).pack(pady=10)
btn_dataselect = Button(settings, text="Database Selection", bd=40, font=18).pack(pady=10)
btn_setbuild = Button(settings, text="Set Album Build Location", bd=40, font=18).pack(pady=10)
#PHOTO UPLOAD TAB:
btn_taglable = Label(photoUpload, text="Enter Tag Below: ",bd=10, font=18, pady=10)
btn_tagentry = Entry(photoUpload, textvariable = tag_var,bd=10, show=None, font=18)
btn_open = Button(photoUpload, text="Choose Photos", bd=10, font=18, pady=10, command=open_dir)
btn_save = Button(photoUpload, text="Save Tag...", bd=10, font=18, pady=10, command=save_Tag)
btn_displayimg = Button(photoUpload, text="Preview Image", bd=10, font=18, pady=130, padx=76)

#somehow change displayimg button to an image
#photo = PhotoImage(file=r"path")
#btn_displayimg = Button(photoUpload, image=photo, bd=40, font=18).pack(pady=10)

btn_taglable.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
btn_tagentry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)
btn_displayimg.grid(row=2, column=1, sticky="ew", padx=5)
#ALBUM CREATOR TAB:
btn_filter = Button(albumCreate, text="Filter By Quality", bd=10, font=18, pady=10)
btn_sharpness = Button(albumCreate, text="Sharpness", bd=10, font=18, pady=10)
btn_contrast = Button(albumCreate, text="Contrast", bd=10, font=18, pady=10)
btn_face = Button(albumCreate, text="Face Present", bd=10, font=18, pady=10)
btn_color = Button(albumCreate, text="Color Composition", bd=10, font=18, pady=10)

#somehow change displayimg button to an image
#photo = PhotoImage(file=r"path")
#btn_displayimg = Button(photoUpload, image=photo, bd=40, font=18).pack(pady=10)


btn_filter.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_sharpness.grid(row=1, column=0, sticky="ew", padx=5)
btn_contrast.grid(row=1, column=1, sticky="ew", padx=5)
btn_face.grid(row=2, column=0, sticky="ew", padx=5)
btn_color.grid(row=2, column=1, sticky="ew", padx=5)





window.mainloop()
