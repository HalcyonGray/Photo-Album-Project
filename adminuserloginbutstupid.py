from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
import os
from PIL import ImageTk, Image
import photodatabase
from tkinter import scrolledtext

login = Tk()
login.title('Login')
login.geometry("200x200")

photodatabase.Createdatabase()


# ADMIN WINDOW
# ---------------------------------------------
def openAdmin():
    admin = Toplevel(login)
    admin.title('Photo Album')
    admin.minsize(width=1000, height=500)
    admin.geometry("500x500")
    # create a notebook called tabs to store tabs
    tabs = ttk.Notebook(admin)
    tabs.pack(pady=0)  # possible padding we can add from the top
    photolist = []
    tag_var = StringVar()
    photobuttonlist = []
    photo_var = []  # true/false stack for tag upload

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
                if file.endswith(".png") | file.endswith(".jpg"):
                    photolist.append(os.path.join(root, file))

        '''img = Image.open(filepath)
        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)
        panel = Label(photoUpload, image=img)
        panel.image = img'''

        for i, j in enumerate(photolist):
            var = IntVar()
            c = Checkbutton(text_area, font=18, variable=var)
            # im = Button(photoUpload, text="Preview Image", bd=10, font=18, command=prev_click) #if we want to use buttons
            imvar = Image.open(j)
            imvar.thumbnail((100, 100))
            img = ImageTk.PhotoImage(imvar)
            panel = Label(text_area, image=img)
            panel.image = img
            c.grid(row=3 + i, column=0)
            panel.grid(row=3 + i, column=1)
            photobuttonlist.append([j.strip(), var, c])
        canvas.create_window(0, 0, anchor='nw', window=text_area)
        scrollbar = Scrollbar(photoUpload, command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=3, sticky='ns')
        text_area.bind("<Configure>", update_scrollregion)
        canvas.update_idletasks()

    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def update_scrollregion2(event):
        canvas2.configure(scrollregion=canvas2.bbox("all"))

    def save_Tag():
        """tag input for photo upload to database, etc."""
        tag = tag_var.get()
        if (tag == ""):
            return
        # operations here
        '''for i in photobuttonlist:
            if i[1].get()==0:
                # upload to database with tag
                i[2].destroy()'''
        for i in photobuttonlist:
            if i[1].get() != 0:
                photodatabase.insertphoto(i[0], tag)
        tag_var.set("")

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

    def edit_database():
        stack = photodatabase.outputalldb()
        #print(stack[0][0])
        refpic = r""
        for i, j in enumerate(stack):
            if(refpic != j[0]):
                '''rownum = 3
                columnnum = 2
                rownum = rownum + 1'''
                refpic = j[0]
                print(refpic)
                var = IntVar()
                c = Checkbutton(text_area2, font=18, variable=var)
                imvar = Image.open(refpic)
                imvar.thumbnail((100, 100))
                img = ImageTk.PhotoImage(imvar)
                panel2 = Label(text_area2, image=img)
                panel2.image = img
                #panel2 = Label(text_area2, text = j[0], font = 18)
                c.grid(row=3+i, column=0)
                panel2.grid(row=3+i, column=1)
                photobuttonlist.append([refpic, var, c])
        canvas2.create_window(0, 0, anchor='nw', window=text_area2)
        scrollbar2 = Scrollbar(settings, command=canvas2.yview)
        canvas2.config(yscrollcommand=scrollbar2.set)
        scrollbar2.grid(row=3, column=3, sticky='ns')
        text_area2.bind("<Configure>", update_scrollregion2)
        canvas2.update_idletasks()


    '''def prev_click():
        global img
        window = Toplevel()
        window.title("Image Preview")
        window.geometry("1280x720")
        window.configure(background='white')
        path = variable
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(window, image = img)
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        window.mainloop()'''

    txt_edit = tk.Text(admin)  # idk what this does but i put it in cause it was needed

    # Initalize different tabs
    settings = Frame(tabs, width=500, height=500, bg="pink")  # bg=background color
    photoUpload = Frame(tabs, width=500, height=500, bg="purple")

    tabs.add(photoUpload, text="Photo Upload")
    tabs.add(settings, text="Edit Database")

    # Initalize buttons for each tab

    # EDIT DATABASE TAB:
    # needs commands, just empty buttons        
    btn_datashow = Button(settings, text="Show database", bd=10, font=18, pady=10, command=edit_database)
    btn_tagshow = Button(settings, text="Show all tags", bd=10, font=18, pady=10)
    btn_deltag = Button(settings, text="Delete Tag", bd=10, font=18, pady=10)
    btn_delphoto = Button(settings, text="Delete Photo", bd=10, font=18, pady=10)
    btn_textentry = Entry(settings, textvariable=tag_var, bd=10, show=None, font=18)
    text_area2 = Frame(settings, width=10, height=10)
    canvas2 = Canvas(settings)
    
    canvas2.grid(row=3, pady=1, padx=1, sticky='ns')
    btn_textentry.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
    btn_datashow.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_tagshow.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    btn_deltag.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    btn_delphoto.grid(row=1, column=0, sticky="ew", padx=5)


    # PHOTO UPLOAD TAB:
    btn_taglable = Label(photoUpload, text="Enter Tag Below: ", bd=10, font=18, pady=10)
    btn_tagentry = Entry(photoUpload, textvariable=tag_var, bd=10, show=None, font=18)
    btn_open = Button(photoUpload, text="Choose Photos", bd=10, font=18, pady=10, command=open_dir)
    btn_save = Button(photoUpload, text="Save Tag...", bd=10, font=18, pady=10, command=save_Tag)
    canvas = Canvas(photoUpload)
    text_area = Frame(photoUpload, width=10, height=10)
    canvas.grid(row=3, pady=1, padx=1, sticky='ns')
    btn_taglable.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    btn_tagentry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5)

# USER WINDOW
# ---------------------------------------------------------------------
def openUser():

    user = Toplevel(login)
    user.title("User")
    user.geometry("1200x500")
    user.configure(bg='blue')
    photolist = []
    taglist = []
    tag_var = StringVar()
    num_var = IntVar()
    photobuttonlist = []
    tagbuttonlist = []

#FUNCTION CALLS
    def output_tags():
        taglist = photodatabase.outputalltags()
        for i, j in enumerate(taglist):
            print(i)
            print(j)
            var = IntVar()
            c = Checkbutton(text_area, font=18, variable=var)
            panel = Label(text_area, text = j)
            c.grid(row=3 + i, column=1)
            panel.grid(row=3 + i, column=2)
            photobuttonlist.append([j.strip(), var, c])
        canvastagout.create_window(0, 0, anchor='nw', window=text_area)
        scrollbartag = Scrollbar(user, command=canvas.yview)
        canvastagout.config(yscrollcommand=scrollbar.set)
        scrollbartag.grid(row=3, column=3, sticky='ns')
        text_area.bind("<Configure>", update_scrollregion)
        canvastagout.update_idletasks()
    def build():
        """Build photo Album"""
        tag = tag_var.get()
        photolist = photodatabase.buildAlbum(tag)
        '''filepath = askdirectory()
        if not filepath:
            return
        for root, dirs, files in os.walk(filepath):  # all .png in folder
            for file in files:
                if file.endswith(".png") | file.endswith(".jpg"):
                    photolist.append(os.path.join(root, file))'''

        '''img = Image.open(filepath)
        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)
        panel = Label(photoUpload, image=img)
        panel.image = img'''

        for i, j in enumerate(photolist):
            if i < num_var.get() or num_var.get()==0:
                var = IntVar()
                c = Checkbutton(text_area, font=18, variable=var)
                imvar = Image.open(j)
                imvar.thumbnail((500, 500))
                img = ImageTk.PhotoImage(imvar)
                panel = Label(text_area, image=img)
                panel.image = img
                c.grid(row=3 + i, column=0)
                panel.grid(row=3 + i, column=1)
                photobuttonlist.append([j.strip(), var, c])
        canvas.create_window(0, 0, anchor='nw', window=text_area)
        scrollbar = Scrollbar(user, command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=3, sticky='ns')
        text_area.bind("<Configure>", update_scrollregion)
        canvas.update_idletasks()

    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    #USER BUTTONS
    btn_taglable = Label(user, text="Enter tag below: ", bd=10, font=18, pady=10)
    btn_tagentry = Entry(user, textvariable=tag_var, bd=10, show=None, font=18)
    btn_numlable = Label(user, text="Enter number of photos below: ", bd=10, font=18, pady=10)
    btn_numentry = Entry(user, textvariable=num_var, bd=10, show=None, font=18)
    btn_open = Button(user, text="List tags", bd=10, font=18, pady=10, command=output_tags)
    btn_quality = Button(user, text="Build Album", bd=10, font=18, pady=10, command=build)
    canvas = Canvas(user)
    canvastagout = Canvas(user)
    text_area = Frame(user, width=10, height=10)
    canvas.grid(row=3, pady=1, padx=1, sticky='ns')
    canvastagout.grid(row=3, column = 1 , pady=1, padx=1, sticky='ns')

    btn_taglable.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    btn_tagentry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    btn_numlable.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
    btn_numentry.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_quality.grid(row=1, column=0, sticky="ew", padx=5)


# LOGIN WINDOW
# -------------------------------------------------------------------------
label = Label(login, text="Photo Album Creation Tool")
label.pack(pady=10)

# Buttons on login window
btn = Button(login, text="Admin Login", command=openAdmin)
btn.pack(pady=10)
btn2 = Button(login, text="User Login", command=openUser)
btn2.pack(pady=10)

# end main loop
mainloop()
