from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
import os
from PIL import ImageTk, Image
import photodatabase
from tkinter import scrolledtext
import shutil
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
    admin.configure(bg='gray')
    # create a notebook called tabs to store tabs
    photolist = []
    tag_var = StringVar()
    photobuttonlist = []

    # FUNCTION CALLS

    def open_dir():
        """open dir for photos"""
        filepath = askdirectory()
        clear(text_area2)
        output_tags()
        if not filepath:
            return
        for root, dirs, files in os.walk(filepath):  # all .png in folder
            for file in files: #try changing this to something using the 'magic' or 'mimetypes' library to allow more image file types, but note that these were the fully compatable image types for pillow as of May 16 2021
                if file.endswith(".png") | file.endswith(".PNG") | file.endswith(".jpg") | file.endswith(".JPG") | file.endswith(".jpeg") | file.endswith(".JPEG")| file.endswith("BMP")| file.endswith("DIB")| file.endswith("EPS")| file.endswith("GIF")| file.endswith("ICNS")| file.endswith("ICO")| file.endswith("IM")| file.endswith("MSP")| file.endswith("PCX")| file.endswith("PPM")| file.endswith("SGI")| file.endswith("SPIDER")| file.endswith("TGA")| file.endswith("TIFF")| file.endswith("WebP")| file.endswith("XBM")| file.endswith("bmp")| file.endswith("dib")| file.endswith("eps")| file.endswith("gif")| file.endswith("icns")| file.endswith("ico")| file.endswith("im")| file.endswith("msp")| file.endswith("pcx")| file.endswith("ppm")| file.endswith("sgi")| file.endswith("spider")| file.endswith("tga")| file.endswith("tiff")| file.endswith("webp")| file.endswith("xbm"):
                    photolist.append(os.path.join(root, file)) 
        clear(text_area)

        popup = tk.Toplevel() #loading bar
        tk.Label(popup, text="Files being downloaded").grid(row=0, column=0)

        progress = 0
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
        progress_bar.grid(row=1, column=0)  # .pack(fill=tk.X, expand=1, side=tk.BOTTOM)
        popup.pack_slaves()

        if not photolist:
            panel = Label(text_area, text="No photos in directory")
            panel.grid(row=3 + 1)
            popup.destroy()
            return
        
        progress_step = float(100.0 / len(photolist))
        for i, j in enumerate(photolist):
            var = IntVar()
            c = Checkbutton(text_area, font=18, variable=var)
            imvar = Image.open(j)
            imvar.thumbnail((300, 300))
            img = ImageTk.PhotoImage(imvar)
            panel = Label(text_area, image=img)
            panel.image = img
            c.grid(row=2 + i, column=0)
            panel.grid(row=2 + i, column=1)
            photobuttonlist.append([j.strip(), var, c])

            popup.update()
            progress += progress_step
            progress_var.set(progress)
            print(j)
            photodatabase.uploadphoto(j) #will crash is image is all ONE color Black

        tag_var.set("")
        popup.destroy()

        canvas.create_window(0, 0, anchor='nw', window=text_area)
        scrollbar = Scrollbar(admin, command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky='ns')

        scrollbar2 = Scrollbar(admin, command=canvas.xview, orient='horizontal')
        canvas.config(xscrollcommand=scrollbar2.set)
        scrollbar2.grid(row=3, column=0, sticky='ew')

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

        taglist = tag.split(';')
        for tag in taglist:
            if (tag == ""):
                return

            for i in photobuttonlist:
                if i[1].get() != 0:
                    photodatabase.insertphoto(i[0], tag)
            tag_var.set("")
        clear(text_area2)
        photobuttonlist.clear()
        output_tags()

    def edit_database():
        stack = photodatabase.outputalldb()
        clear(text_area2)
        output_tags()
        refpic = r""
        clear(text_area)
        for i, j in enumerate(stack):
            if (refpic != j[0]):
                refpic = j[0]
                var = IntVar()
                c = Checkbutton(text_area, font=18, variable=var)
                imvar = Image.open(refpic)
                imvar.thumbnail((100, 100))
                img = ImageTk.PhotoImage(imvar)
                panel2 = Label(text_area, image=img)
                panel2.image = img
                panel3 = Label(text_area, text=j[1], font=18)
                c.grid(row=2 + i, column=0)
                panel2.grid(row=2 + i, column=1)
                panel3.grid(row=2 + i, column=2)
                photobuttonlist.append([refpic, var, c])
                rowtemp = 2 + i
                columntemp = 3
            else:
                panel4 = Label(text_area, text=j[1], font=18)
                panel4.grid(row=rowtemp, column=columntemp)
                columntemp = columntemp + 1
        canvas.create_window(0, 0, anchor='nw', window=text_area)
        scrollbar = Scrollbar(admin, command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky='ns')

        scrollbar2 = Scrollbar(admin, command=canvas.xview, orient=HORIZONTAL)
        canvas.config(xscrollcommand=scrollbar2.set)
        scrollbar2.grid(row=3, column=0, sticky='ew')

        text_area.bind("<Configure>", update_scrollregion)
        canvas.update_idletasks()

    def all_of_tag_database():
        tag = tag_var.get()
        if (tag == ""):
            return
        taglist = tag.split(';')
        taglistcopy = taglist.copy()
        stack = photodatabase.outputalloftag(taglist.pop())
        reftemp = stack.copy()
        for tag in taglist:
            compstack = photodatabase.outputalloftag(tag)
            for refphoto in reftemp:
                n = False
                for compphoto in compstack:
                    if refphoto[0] == compphoto[0]:
                        n = True
                if n == False:
                    stack.remove(refphoto)
        clear(text_area2)
        tag_var.set("")
        output_tags()
        refpic = r""
        clear(text_area)
        if not stack:
            panel = Label(text_area, text="No photos with tag Error")
            panel.grid(row=3 + 1)

        for i, j in enumerate(stack):
            refpic = j[0]
            var = IntVar()
            c = Checkbutton(text_area, font=18, variable=var)
            imvar = Image.open(refpic)
            imvar.thumbnail((100, 100))
            img = ImageTk.PhotoImage(imvar)
            panel2 = Label(text_area, image=img)
            panel2.image = img
            # panel3 = Label(text_area, text=j[1], font=18)
            c.grid(row=2 + i, column=0)
            panel2.grid(row=2 + i, column=1)
            # panel3.grid(row=2 + i, column=2)
            photobuttonlist.append([refpic, var, c])
            rowtemp = 2 + i
            columntemp = 2
            for tags in taglistcopy:
                panel4 = Label(text_area, text=tags, font=18)
                panel4.grid(row=rowtemp, column=columntemp)
                columntemp = columntemp + 1
        canvas.create_window(0, 0, anchor='nw', window=text_area)
        scrollbar = Scrollbar(admin, command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky='ns')

        scrollbar2 = Scrollbar(admin, command=canvas.xview, orient=HORIZONTAL)
        canvas.config(xscrollcommand=scrollbar2.set)
        scrollbar2.grid(row=3, column=0, sticky='ew')

        text_area.bind("<Configure>", update_scrollregion)
        canvas.update_idletasks()

    def delete_img():
        for i in photobuttonlist:
            if i[1].get() != 0:
                photodatabase.deleteimage(i[0])
        clear(text_area)
        photobuttonlist.clear()
        edit_database()

    def delete_tag():
        tag = tag_var.get()
        taglist = tag.split(';')
        for tag in taglist:
            if (tag == ""):
                return
            photodatabase.deletetag(tag)
        tag_var.set("")
        clear(text_area)
        photobuttonlist.clear()
        edit_database()
        clear(text_area2)
        output_tags()

    def delete_ref():
        tag = tag_var.get()
        taglist = tag.split(';')
        for tag in taglist:
            for i in photobuttonlist:
                if i[1].get() != 0:
                    photodatabase.deletereference(i[0], tag)
        photobuttonlist.clear()
        clear(text_area)
        edit_database()
        tag_var.set("")

    def add_ref():
        tag = tag_var.get()
        taglist = tag.split(';')
        for tag in taglist:
            for i in photobuttonlist:
                if i[1].get() != 0:
                    photodatabase.insertphoto(i[0], tag)
        photobuttonlist.clear()
        clear(text_area)
        edit_database()
        tag_var.set("")

    def output_tags():
        taglist = photodatabase.outputalltags()
        for i, j in enumerate(taglist):
            panel = Label(text_area2, text=j)
            panel.grid(row=2 + i)
        canvas2.create_window(0, 0, anchor='nw', window=text_area2)
        scrollbartag = Scrollbar(admin, command=canvas2.yview)
        canvas2.config(yscrollcommand=scrollbartag.set)
        scrollbartag.grid(row=2, column=7, sticky='ns')
        text_area2.bind("<Configure>", update_scrollregion2)
        canvas2.update_idletasks()

    def clear(framename):
        list = framename.grid_slaves()
        for l in list:
            l.destroy()

    # MENU

    uploadMenu = Menu(admin)
    admin.config(menu=uploadMenu)
    file_menu = Menu(uploadMenu)
    # Menu item with command
    file_menu.add_command(label="Photo Upload Mode", command=open_dir)
    file_menu.add_command(label="Save With Tag", command=save_Tag)
    file_menu.add_separator()
    file_menu.add_command(label="Edit Database Mode", command=edit_database)
    file_menu.add_command(label="Filter by tags", command=all_of_tag_database)
    file_menu.add_command(label="Delete Tag", command=delete_tag)
    file_menu.add_command(label="Delete Photo", command=delete_img)
    file_menu.add_command(label="Delete Tag from Photo", command=delete_ref)
    file_menu.add_command(label="Add Tag to Photo", command=add_ref)
    # Creates File in menu
    uploadMenu.add_cascade(label="Commands", menu=file_menu)

    # Initalize buttons for each tab

    # EDIT DATABASE TAB:
    btn_textentry = Entry(admin, textvariable=tag_var, bd=10, show=None, font=18)
    canvas = Canvas(admin)
    canvas2 = Canvas(admin)
    text_area = Frame(canvas, width=10, height=10)
    text_area2 = Frame(canvas2, width=10, height=10)

    canvas.grid(row=2, column=0, pady=1, padx=1, sticky='ns', show=None)
    canvas2.grid(row=2, column=2, pady=1, padx=1, sticky='ns', show=None, columnspan=4)

    textlabel = Label(admin, text="Enter Tag:", bd=10, font=18, pady=10)
    textlabel.grid(row=0, column=0, sticky="e", padx=5, pady=5, columnspan=2)
    btn_textentry.grid(row=0, column=2, sticky="w", padx=5, pady=5)

    edit_database()
    login.wm_state('iconic')


# USER WINDOW
# ---------------------------------------------------------------------
def openUser():
    user = Toplevel(login)
    user.title("User")
    user.geometry("1200x500")
    tag_var = StringVar()
    num_var = IntVar()
    user.configure(bg='gray')
    reftempalbum = []

    # FUNCTION CALLS
    def output_tags():
        taglist = photodatabase.outputalltags()
        for i, j in enumerate(taglist):
            panel = Label(text_area2, text=j)
            panel.grid(row=3 + i)
        canvastagout.create_window(0, 0, anchor='nw', window=text_area2)
        scrollbartag = Scrollbar(user, command=canvas.yview)
        canvastagout.config(yscrollcommand=scrollbartag.set)
        scrollbartag.grid(row=3, column=7, sticky='ns')
        text_area2.bind("<Configure>", update_scrollregion2)
        canvastagout.update_idletasks()

    def build():
        """Build photo Album"""
        clear(text_area)
        tag = tag_var.get()
        taglist = tag.split(';')
        refstack = photodatabase.buildAlbum(taglist.pop())  # gets first tag build
        reftemp = refstack.copy()
        for tag in taglist:
            photolist = photodatabase.buildAlbum(tag)
            for refphoto in reftemp:
                n = False
                for compphoto in photolist:
                    if refphoto == compphoto:
                        n = True
                if n == False:
                    refstack.remove(refphoto)

        if not refstack:
            panel = Label(text_area, text="No photos with tag Error")
            panel.grid(row=3 + 1)
            return

        for i, j in enumerate(refstack):
            if i < num_var.get():
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

        scrollbar2 = Scrollbar(user, command=canvas.xview, orient=HORIZONTAL)
        canvas.config(xscrollcommand=scrollbar2.set)
        scrollbar2.grid(row=4, column=0, sticky='ew')

        text_area.bind("<Configure>", update_scrollregion)
        canvas.update_idletasks()

        album = Toplevel(user)
        album.title('Album')
        album.minsize(width=1000, height=800)
        album.geometry("500x500")
        album.configure(bg='gray')

        
        for i, j in enumerate(refstack):
            if i < num_var.get():
                reftempalbum.append(refstack[i])
        
        imvar = Image.open(reftempalbum[0])
        imvar.thumbnail((700, 900))
        img = ImageTk.PhotoImage(imvar)
        panelalbum = Label(album, image=img)
        panelalbum.image = img
        panelalbum.grid(row=2, column=0, sticky='nw')
        
        def nextimage():
            if reftempalbum:
                panelalbum.grid_remove
                reftempalbum.append(reftempalbum.pop(0))
                imvar = Image.open(reftempalbum[0])
                imvar.thumbnail((700, 900))
                img = ImageTk.PhotoImage(imvar)
                panelalbum.configure(image=img)
                panelalbum.image = img
            else:
                notice = Label(album, text= "End of Album")
                notice.grid(column=2)

        def savealbum():
            directory = tag_var.get()
            parent_dir = os.getcwd()+"/Albums/"
            try:
                os.mkdir(parent_dir)
            except OSError as error: 
                print(error)  
            print(directory)
            print(parent_dir)
            path = os.path.join(parent_dir, directory)
            print(path)
            try:
                os.mkdir(path)
            except OSError as error: 
                print(error)  
            for i, j in enumerate(refstack):
                if i < num_var.get():
                    shutil.copy2(j, path)
            album.wm_state('iconic')



        btn_nextimage = Button(album, text="Next Image", command=nextimage)
        btn_nextimage.grid(row=0, column=0, sticky='nw')
        btn_savealbum = Button(album, text="Save Album", command=savealbum)
        btn_savealbum.grid(row=1, column=0, sticky='nw')

        user.wm_state('iconic')

    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def update_scrollregion2(event):
        canvastagout.configure(scrollregion=canvastagout.bbox("all"))

    def clear(framename):
        list = framename.grid_slaves()
        for l in list:
            l.destroy()

    # USER BUTTONS
    uploadMenu = Menu(user)
    user.config(menu=uploadMenu)
    file_menu = Menu(uploadMenu)
    # Menu item with command
    file_menu.add_command(label="Album Build", command=build)
    # Creates File in menu
    uploadMenu.add_cascade(label="File", menu=file_menu)

    btn_taglable = Label(user, text="Enter tag below: ", bd=10, font=18, pady=10)
    btn_numlable = Label(user, text="Enter number of photos below: ", bd=10, font=18, pady=10)
    btn_tagentry = Entry(user, textvariable=tag_var, bd=10, show=None, font=18)
    btn_spinbox = Spinbox(user, from_=1, to=500, textvariable=num_var)
    canvas = Canvas(user)
    canvastagout = Canvas(user)
    text_area = Frame(canvas, width=10, height=10)
    text_area2 = Frame(canvastagout, width=10, height=10)
    canvas.grid(row=3, column=0, pady=1, padx=1, sticky='ns')
    canvastagout.grid(row=3, column=2, pady=1, padx=1, sticky='ns', columnspan=4)

    btn_taglable.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
    btn_numlable.grid(row=0, column=2, padx=5, pady=5, columnspan=5)
    btn_tagentry.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
    btn_spinbox.grid(row=1, column=2, padx=5, pady=5, columnspan=5)
    output_tags()
    login.wm_state('iconic')


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