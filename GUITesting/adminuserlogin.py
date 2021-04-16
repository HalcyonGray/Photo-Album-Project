from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
import os
login = Tk()
login.title('Login')
login.geometry("200x200")

#ADMIN WINDOW
#---------------------------------------------
def openAdmin():
    admin = Toplevel(login)
    admin.title('Photo Album')
    admin.geometry("500x500")

    # create a notebook called tabs to store tabs
    tabs = ttk.Notebook(admin)
    tabs.pack(pady=0)  # possible padding we can add from the top
    photolist = []

    # FUNCTION CALLS
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
        admin.title(f"Simple Text Editor - {filepath}")

    def open_dir():
        """open dir for photos"""
        filepath = askdirectory()
        if not filepath:
            return
        for root, dirs, files in os.walk(filepath):  # all .png in folder
            for file in files:
                if file.endswith(".png") | file.endswith(".jpeg"):
                    photolist.append(os.path.join(root, file))
        while photolist:  # for testing
            print(photolist.pop())

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
        admin.title(f"Simple Text Editor - {filepath}")

    txt_edit = tk.Text(admin)  # idk what this does but i put it in cause it was needed

    # Initalize different tabs
    settings = Frame(tabs, width=500, height=500, bg="pink")  # bg=background color
    photoUpload = Frame(tabs, width=500, height=500, bg="purple")
    albumCreate = Frame(tabs, width=500, height=500, bg="green")

    tabs.add(settings, text="Settings")
    tabs.add(photoUpload, text="Photo Upload")
    tabs.add(albumCreate, text="Album Creator")

    # Initalize buttons for each tab

    # SETTINGS TAB:
    btn_dataedit = Button(settings, text="Database Edit", bd=40, font=18).pack(pady=10)
    btn_dataselect = Button(settings, text="Database Selection", bd=40, font=18).pack(pady=10)
    btn_setbuild = Button(settings, text="Set Album Build Location", bd=40, font=18).pack(pady=10)
    # PHOTO UPLOAD TAB:
    btn_open = Button(photoUpload, text="Choose Photos", bd=10, font=18, pady=10, command=open_dir)
    btn_save = Button(photoUpload, text="Save To Database", bd=10, font=18, pady=10, command=save_file)
    btn_displayimg = Button(photoUpload, text="Preview Image", bd=10, font=18, pady=130, padx=76)

    # somehow change displayimg button to an image
    # photo = PhotoImage(file=r"path")
    # btn_displayimg = Button(photoUpload, image=photo, bd=40, font=18).pack(pady=10)

    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5)
    btn_displayimg.grid(row=2, column=1, sticky="ew", padx=5)
    # ALBUM CREATOR TAB:
    btn_quality = Button(albumCreate, text="Filter By Quality", bd=10, font=18, pady=10, command=open_dir)
    btn_tags = Button(albumCreate, text="Filter By Tags", bd=10, font=18, pady=10, command=save_file)
    btn_preview = Button(albumCreate, text="Preview Image", bd=10, font=18, pady=130, padx=76)

    # somehow change displayimg button to an image
    # photo = PhotoImage(file=r"path")
    # btn_displayimg = Button(photoUpload, image=photo, bd=40, font=18).pack(pady=10)

    btn_quality.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_tags.grid(row=1, column=0, sticky="ew", padx=5)
    btn_preview.grid(row=2, column=1, sticky="ew", padx=5)





    # How to write text thats not a button
    #Label(admin,text="Test").pack()

#USER WINDOW
#---------------------------------------------------------------------
def openUser():
    user = Toplevel(login)
    user.title("User")
    user.geometry("500x500")
    Label(user,text="This is what a user will see epic").pack()








#LOGIN WINDOW
#-------------------------------------------------------------------------
label = Label(login,text="Photo Album Creation Tool")
label.pack(pady=10)

#Buttons on login window
btn = Button(login,text="Admin Login",command=openAdmin)
btn.pack(pady=10)
btn2 = Button(login,text="User Login",command=openUser)
btn2.pack(pady=10)

#end main loop
mainloop()