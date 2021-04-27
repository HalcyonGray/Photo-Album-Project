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

    def open_dir():
        """open dir for photos"""
        filepath = askdirectory()
        if not filepath:
            return
        for root, dirs, files in os.walk(filepath):  # all .png in folder
            for file in files:
                if file.endswith(".png") | file.endswith(".jpg"):
                    photolist.append(os.path.join(root, file))
        clear(text_area)
        for i, j in enumerate(photolist):
            var = IntVar()
            c = Checkbutton(text_area, font=18, variable=var)
            # im = Button(photoUpload, text="Preview Image", bd=10, font=18, command=prev_click) #if we want to use buttons
            imvar = Image.open(j)
            imvar.thumbnail((300, 300))
            img = ImageTk.PhotoImage(imvar)
            panel = Label(text_area, image=img)
            panel.image = img
            c.grid(row=3 + i, column=0)
            panel.grid(row=3 + i, column=1)
            photobuttonlist.append([j.strip(), var, c])
        canvas.create_window(0, 0, anchor='nw', window=text_area)
        scrollbar = Scrollbar(photoUpload, command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=1, sticky='ns')
        text_area.bind("<Configure>", update_scrollregion)
        canvas.update_idletasks()

    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def update_scrollregion2(event):
        canvas2.configure(scrollregion=canvas2.bbox("all"))
    def update_scrollregion3(event):
        canvas3.configure(scrollregion=canvas3.bbox("all"))    

    def save_Tag():
        """tag input for photo upload to database, etc."""
        tag = tag_var.get()
        if (tag == ""):
            return

        popup = tk.Toplevel()
        tk.Label(popup, text="Files being downloaded").grid(row=0,column=0)

        progress = 0
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
        progress_bar.grid(row=1, column=0)#.pack(fill=tk.X, expand=1, side=tk.BOTTOM)
        popup.pack_slaves()

        progress_step = float(100.0/len(photobuttonlist))
        for i in photobuttonlist:
            popup.update()
            progress += progress_step
            progress_var.set(progress)
            if i[1].get() != 0:
                photodatabase.insertphoto(i[0], tag)
        tag_var.set("")
        popup.destroy()

    def edit_database():
        stack = photodatabase.outputalldb()
        refpic = r""
        for i, j in enumerate(stack):
            if(refpic != j[0]):
                refpic = j[0]
                var = IntVar()
                c = Checkbutton(text_area2, font=18, variable=var)
                imvar = Image.open(refpic)
                imvar.thumbnail((100, 100))
                img = ImageTk.PhotoImage(imvar)
                panel2 = Label(text_area2, image=img)
                panel2.image = img
                panel3 = Label(text_area2, text = j[1], font = 18)
                #panel2 = Label(text_area2, text = j[1], font = 18)
                c.grid(row=3+i, column=0)
                panel2.grid(row=3+i, column=1)
                panel3.grid(row=3+i, column=2)
                photobuttonlist.append([refpic, var, c])
                rowtemp = 3+i
                columntemp = 3
            else:
                panel4 = Label(text_area2, text = j[1], font = 18)
                panel4.grid(row=rowtemp, column=columntemp)
                columntemp = columntemp + 1  
        canvas2.create_window(0, 0, anchor='nw', window=text_area2)
        scrollbar2 = Scrollbar(settings, command=canvas2.yview)
        canvas2.config(yscrollcommand=scrollbar2.set)
        scrollbar2.grid(row=3, column=1, sticky='ns')
        text_area2.bind("<Configure>", update_scrollregion2)
        canvas2.update_idletasks()
    def delete_img():
        for i in photobuttonlist:
            if i[1].get() != 0:
                photodatabase.deleteimage(i[0])
        clear(text_area2)
        edit_database()

    def delete_tag():
        tag = tag_var.get()
        if (tag == ""):
            return
        photodatabase.deletetag(tag)
        tag_var.set("")
        clear(text_area2)
        clear(text_area3)
        edit_database()
        output_tags()
        
        #needs scroll region update
    
    def output_tags():
        taglist = photodatabase.outputalltags()
        for i, j in enumerate(taglist):
            print(j)
            panel = Label(text_area3, text = j)
            panel.grid(row=3 + i)
        canvas3.create_window(0, 0, anchor='nw', window=text_area3)
        scrollbartag = Scrollbar(settings, command=canvas3.yview)
        canvas3.config(yscrollcommand=scrollbartag.set)
        scrollbartag.grid(row=3, column=3, sticky='ns')
        text_area3.bind("<Configure>", update_scrollregion3)
        canvas3.update_idletasks()
    
    def clear(framename):
        list = framename.grid_slaves()
        for l in list:
            l.destroy()

    # Initalize different tabs
    settings = Frame(tabs, width=500, height=500)  # bg=background color
    photoUpload = Frame(tabs, width=500, height=500)

    tabs.add(photoUpload, text="Photo Upload")
    tabs.add(settings, text="Edit Database")

    # Initalize buttons for each tab

    # EDIT DATABASE TAB:   
    btn_datashow = Button(settings, text="Show database", bd=10, font=18, pady=10, command=edit_database)
    btn_tagshow = Button(settings, text="Show all tags", bd=10, font=18, pady=10, command=output_tags)
    btn_deltag = Button(settings, text="Delete Tag", bd=10, font=18, pady=10, command = delete_tag)
    btn_delphoto = Button(settings, text="Delete Selected Photos", bd=10, font=18, pady=10, command = delete_img)
    btn_textentry = Entry(settings, textvariable=tag_var, bd=10, show=None, font=18)
    canvas2 = Canvas(settings)
    text_area2 = Frame(canvas2, width=10, height=10)
    canvas3 = Canvas(settings)
    text_area3 = Frame(canvas3, width=10, height=10)
    
    canvas2.grid(row=3, column=0, pady=1, padx=1, sticky='ns', show=None)
    canvas3.grid(row=3, column=2, pady=1, padx=1, sticky='ns')
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
    text_area = Frame(canvas, width=10, height=10)
    canvas.grid(row=3, pady=1, padx=1, sticky='ns')
    btn_taglable.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    btn_tagentry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5)
    edit_database()
    output_tags()

# USER WINDOW
# ---------------------------------------------------------------------
def openUser():

    user = Toplevel(login)
    user.title("User")
    user.geometry("1200x500")
    tag_var = StringVar()
    num_var = IntVar()

#FUNCTION CALLS
    def output_tags():
        taglist = photodatabase.outputalltags()
        for i, j in enumerate(taglist):
            panel = Label(text_area2, text = j)
            panel.grid(row=3 + i)
        canvastagout.create_window(0, 0, anchor='nw', window=text_area2)
        scrollbartag = Scrollbar(user, command=canvas.yview)
        canvastagout.config(yscrollcommand=scrollbartag.set)
        scrollbartag.grid(row=3, column=3, sticky='ns')
        text_area2.bind("<Configure>", update_scrollregion2)
        canvastagout.update_idletasks()
    def build():
        """Build photo Album"""
        clear(text_area)
        tag = tag_var.get()
        photolist = photodatabase.buildAlbum(tag)

        for i, j in enumerate(photolist):
            if i < num_var.get() or num_var.get()==0:
                imvar = Image.open(j)
                imvar.thumbnail((400, 400))
                img = ImageTk.PhotoImage(imvar)
                panel = Label(text_area, image=img)
                panel.image = img
                panel.grid(row=3 + i)
        canvas.create_window(0, 0, anchor='nw', window=text_area)
        scrollbar = Scrollbar(user, command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=1, sticky='ns')
        text_area.bind("<Configure>", update_scrollregion)
        canvas.update_idletasks()

    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    def update_scrollregion2(event):
        canvastagout.configure(scrollregion=canvastagout.bbox("all"))
    def clear(framename):
        list = framename.grid_slaves()
        for l in list:
            l.destroy()

    #USER BUTTONS
    btn_taglable = Label(user, text="Enter tag below: ", bd=10, font=18, pady=10)
    btn_tagentry = Entry(user, textvariable=tag_var, bd=10, show=None, font=18)
    btn_numlable = Label(user, text="Enter number of photos below: ", bd=10, font=18, pady=10)
    btn_numentry = Entry(user, textvariable=num_var, bd=10, show=None, font=18)
    btn_open = Button(user, text="List tags", bd=10, font=18, pady=10, command=output_tags)
    btn_quality = Button(user, text="Build Album", bd=10, font=18, pady=10, command=build)
    canvas = Canvas(user)
    canvastagout = Canvas(user)
    text_area = Frame(canvas, width=10, height=10)
    text_area2 = Frame(canvastagout, width=10, height=10)
    canvas.grid(row=3, pady=1, padx=1, sticky='ns')
    canvastagout.grid(row=3, column = 2 , pady=1, padx=1, sticky='ns')

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
