import sys
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

def wrapTextTo(text, wrap):
    return "\n".join([text[i:i+wrap] for i in range(0, len(text), wrap)])
    
    

#the title must be id of searched word AAAAAAA or simialrly
def display_image(filename, title="image"):
    image = Image.open(filename)
    root = tk.Tk()
    root.title(title)
    tk_image = ImageTk.PhotoImage(image)
    label = Label(root, image = tk_image)
    label.pack()
    root.mainloop()

#the title must be id of searched word AAAAAAA or simialrly
def display_text(filename,title="text", wrap=0):
    content = open(filename, 'r').read()
    if wrap>0:
        content = wrapTextTo(content, wrap);
    root = tk.Tk()
    root.title(title)
    text_var = tk.StringVar()
    text_var.set(content)
    label = Label(root, textvariable=text_var, )
    label.pack()
    root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("one parameter expected - path to file")
        print("second optional is text wrap for non images")
        sys.exit(1)
    try:
        wrap=0
        if len(sys.argv) > 2:
            wrap=int(sys.argv[2])
        display_image(sys.argv[1], sys.argv[1])
    except Exception:
        display_text(sys.argv[1], sys.argv[1], wrap=wrap)
