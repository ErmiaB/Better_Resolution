# Bättre script av Ermia Behzadifar, Te21F
import random
from sys import argv
from tkinter import *
from PIL import Image, ImageTk, ImageFilter
import os
import json



def set_resolution(width, height):
    if width >= 100 and height >= 100:
        print("->set_resolution", width, height)
        cmd = "changeres "+str(width)+" "+str(height)
        os.system(cmd)

class MyApp(object):
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("Sätt upplösning")
        self.cur_row=0
        self.res_object=None
        self.res_file=None

        Label(self.root, text = "Sätt upplösning på fjärrdatorn", font=("Arial", 25)).grid(row=1, column=0)

        self.buttonframe = Frame(self.root)
        self.buttonframe.grid(row=2, column=0, columnspan=2)

        self.res_file = open("/usr/local/berzan/resolutions.json", "r+")
        self.res_object = json.loads(self.res_file.read())
        for res in self.res_object["resolutions"]:
            self.create_resolution_shortcut(res["resX"], res["resY"], res["text"])

        self.custom:Button = Button(self.buttonframe, width = 40, text="Sätt egen upplösning", font=("Arial", 18), command=self.add_custom_resolution)
        self.custom.grid(row=self.cur_row+1, column=0)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        self.res_file.close()
        self.root.destroy()

    def create_resolution_shortcut(self, width: int, height: int, label: str)->None:
        if width != 0 and height != 0 and label != "":
            text = str(width)+ "x"+str(height)+" ("+label+")"
            but:Button = Button(self.buttonframe,width = 40, text=text, font=("Arial", 18),command=lambda: set_resolution(width, height))
            but.grid(row=self.cur_row, column=0)
            cur_id = self.cur_row
            but:Button = Button(self.buttonframe,width = 5, text="Ta bort", font=("Arial", 18),command=lambda: self.remove_resolution(cur_id))
            but.grid(row=self.cur_row, column=1)
            self.cur_row += 1

    def save_file(self):
        self.res_file.seek(0)
        self.res_file.truncate(0)
        info = json.dumps(self.res_object, indent=4, sort_keys=True)
        self.res_file.write(info)

    def remove_resolution(self, index):
        target = (2*(index+1))-1
        self.cur_row -= 1

        self.buttonframe.winfo_children()[target].destroy()
        self.buttonframe.winfo_children()[target].destroy()
        del self.res_object["resolutions"][index]
        self.save_file()

        for widget in self.buttonframe.winfo_children():
            if widget.grid_info()["row"] > index:
                widget.grid(row=widget.grid_info()["row"]-1, column=widget.grid_info()["column"])

        
            

    def save_resolution(self, width: int, height: int, label: str):
        if width >= 100 and height >= 100 and label != "":
            self.create_resolution_shortcut(width, height, label)
            self.custom.grid(row=self.cur_row+1, column=0)
            self.res_object["resolutions"].append({
                "resX": width,
                "resY": height,
                "text": label
            })
            self.save_file()

    def add_custom_resolution(self):
        window = Tk()
        window.title("Sätt egen upplösning")
        inputframe = Frame(window)
        inputframe.grid(row=2, column=0, columnspan=2)
        Label(window, text="Sätt upplösning på fjärrdatorn", font=("Arial", 25)).grid(row=0, column=0)
        Label(inputframe, text="Upplösning X", font=("Arial", 25)).grid(row=1)
        Label(inputframe, text="Upplösning Y", font=("Arial", 25)).grid(row=2)
        Label(inputframe, text="Namn", font=("Arial", 25)).grid(row=3)
        resX = Entry(inputframe)
        resY = Entry(inputframe)
        newTitle = Entry(inputframe)
        resX.grid(row=1, column=1)
        resY.grid(row=2, column=1)
        newTitle.grid(row=3, column=1)
        set_res:Button = Button(inputframe, width=round(inputframe.winfo_width()/2), text="Sätt Upplösning", font=("Arial", 18), command=lambda: set_resolution(int(resX.get()), int(resY.get())))
        set_res.grid(row=4, column=0)
        set_res:Button = Button(inputframe, width=round(inputframe.winfo_width()/2), text="Spara Upplösning", font=("Arial", 18), command=lambda: self.save_resolution(int(resX.get()), int(resY.get()), newTitle.get()))
        set_res.grid(row=4, column=1)

MyApp()
