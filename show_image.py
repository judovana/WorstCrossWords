import sys
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

def wrapTextTo(text, wrap):
    return "\n".join([text[i:i+wrap] for i in range(0, len(text), wrap)])
    
def display_image(filename, title="image"):
    image = Image.open(filename)
    root = tk.Tk()
    root.title(title)
    tk_image = ImageTk.PhotoImage(image)
    label = Label(root, image = tk_image)
    label.pack()
    root.mainloop()

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

def textOrImage(filename, title="future", wrap=0):
    try:
        display_image(filename, title)
    except Exception:
        display_text(filename, title, wrap)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("one parameter expected - path to file")
        print("second optional is text wrap for non images")
        sys.exit(1)
    wrap=0
    if len(sys.argv) > 2:
        wrap=int(sys.argv[2])
    textOrImage(sys.argv[1], sys.argv[1], wrap=wrap)
