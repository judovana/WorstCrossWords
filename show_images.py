import sys
import tkinter as tk
from tkinter import *
import PIL
from PIL import ImageTk, Image

windowCounter=0  #count the sub windows so we can exit once no more left
root=None

def wrapTextTo(text, wrap):
    return "\n".join([text[i:i+wrap] for i in range(0, len(text), wrap)])
    

class ImgOrNote(Toplevel):
    def __init__(self, master, nid, file, title, wrap):
        Toplevel.__init__(self,master)
        self.nid = nid 
        self.wrap = wrap
        self.title(title) #since toplevel widgets define a method called title you can't store it as an attribute
        self.file = file
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.destroy()
        global windowCounter
        windowCounter=windowCounter-1
        global root
        if (windowCounter==0):
            root.destroy()
            root=None

    def display_gui(self): 
        try:
            image = Image.open(self.file)
            tk_image = ImageTk.PhotoImage(image)
            label = Label(self, image = tk_image)
        except Exception:
            content = open(self.file, 'r').read()
            if wrap>0:
                content = wrapTextTo(content, wrap);
            text_var = tk.StringVar()
            text_var.set(content)
            label = Label(self, textvariable=text_var)
        label.pack()
      

    def run(self):
      self.display_note_gui()

def initialize():
    global root
    root = Tk()
    root.withdraw() #hide the root so that only the notes will be visible

def create(file, wrap):
        global root
        if root == None:
            initialize()
        global windowCounter
        windowCounter+=1   
        return  ImgOrNote(root, windowCounter, file, file, wrap)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("one parameter expected - path to file")
        print("if first parameter is number, then it is textwrap for non images")
        print("then of ocurse second and every other is file to open")
        sys.exit(1)
    wrap=0;
    sliceStart=1
    try:
        wrap=int(sys.argv[1])
        sliceStart=2
    except Exception:
        pass
    for file in (sys.argv[sliceStart:]):
        win=create(file, wrap)
        win.display_gui()
    root.mainloop() #still call mainloop on the root
    sys.exit(0)
