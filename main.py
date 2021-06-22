import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os


def skip_file(lbl1, lbl2, bt1, bt2):
    lbl1.pack_forget()
    lbl2.pack_forget()
    bt1.pack_forget()
    bt2.pack_forget()
    lbl1.destroy()
    lbl2.destroy()
    bt1.destroy()
    bt2.destroy()


class App(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Clean folder")
        self.geometry("599x400")

        # Create main frame
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create canvas
        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure canvas
        self.create_scroll_bar()

        # Create second frame
        self.frame2 = tk.Frame(self.canvas)
        # Add new frame to a window in the canvas
        self.window = self.canvas.create_window((0, 0), window=self.frame2, anchor="nw", tags='frame')

        # Add Buttons
        self.button = tk.Button(self.canvas, text="Browse", command=self.browse_button)
        self.button.pack(side=tk.BOTTOM, pady=10)
        self.button2 = tk.Button(self.canvas, text="Clean", command=self.clean_button)
        self.button2.pack(side=tk.BOTTOM)

    # Hide the buttons after getting a folder
    def hide_buttons(self):
        self.button.pack_forget()
        self.button2.pack_forget()

    # Function to allow scroll on mousewheel
    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    def canvas_binds(self):
        # self.canvas.itemconfig('frame', height=self.canvas.winfo_height() - 10, width=self.canvas.winfo_width() - 10)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Create Scroll bar, called whenever canvas changes size
    def create_scroll_bar(self):
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas_binds())
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    # Button command to browse a dir to clean
    def browse_button(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        global folder_path
        folder_path = tk.StringVar(self, "Hello")
        filename = tk.filedialog.askdirectory()
        folder_path.set(filename)
        lbl1 = tk.Label(self.frame2, textvariable=folder_path, font=("Arial", 16))
        lbl1.pack()
        print(filename)

    # Function that will print all files to be deleted and allow user to select
    # whether or not to delete the files.
    def delete_button(self, file):
        self.hide_buttons()
        self.create_scroll_bar()
        self.geometry("600x400")
        if os.path.isfile(folder_path.get() + "/" + file):
            label = ttk.Label(self.frame2, text="Do you wish to delete this file? \n\n" + file, font=("Arial", 14))
        else:
            label = ttk.Label(self.frame2, text="Do you wish to delete this folder? \n\n" + file, font=("Arial", 14))
        label.pack(pady=10)
        label2 = ttk.Label(self.frame2, text="-------------------------------", font=("Arial", 14))

        b1 = ttk.Button(self.frame2, text="Yes")
        b2 = ttk.Button(self.frame2, text="No")
        b1.configure(command=lambda: self.remove_items(file, label, label2, b1, b2))
        b2.configure(command=lambda: skip_file(label, label2, b1, b2))
        b1.pack(pady=10)
        b2.pack(pady=10)
        label2.pack()

    # Button command that will list files or dir in dir to be deleted
    def clean_button(self):
        def remove_all():
            shutil.rmtree(folder_path.get())
            os.mkdir(folder_path.get())

        # Check if user wants to delete everything without checking what files are in the folder
        # Check if file or folder
        label = ttk.Label(self.frame2, text="Do you wish to delete everything all at once?", font=("Arial", 14))
        label.pack(pady=10)
        b1 = ttk.Button(self.frame2, text="All At Once", command=remove_all)
        b2 = ttk.Button(self.frame2, text="One at a time", command=self.clean)
        b1.pack(pady=10)
        b2.pack(pady=10)

    def clean(self):
        for item in os.scandir(folder_path.get()):
            if item.is_file():
                print("I am a file named: " + item.name)
                self.delete_button(item.name)
            else:
                print("I am a folder named:" + item.name)
                self.delete_button(item.name)

    # Functions to remove the associated widgets when file is deleted or skipped
    def remove_items(self, file, lbl1, lbl2, bt1, bt2):
        item = folder_path.get() + "/" + file
        if os.path.isfile(item):
            os.remove(item)
        else:
            shutil.rmtree(item)
        skip_file(lbl1, lbl2, bt1, bt2)


app = App()
app.mainloop()
