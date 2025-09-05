import sys
import tkinter as tk
from tkinter import *
import PIL
from PIL import ImageTk, Image

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
def display_text(filename,title="text"):
    content = open(filename, 'r').read()
    root = tk.Tk()
    root.title(title)
    text_var = tk.StringVar()
    text_var.set(content)
    label = Label(root, textvariable=text_var, )
    label.pack()
    root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("one parameter expected - path to img")
        sys.exit(1)
    try:
        display_image(sys.argv[1])
    except Exception:
        display_text(sys.argv[1])
