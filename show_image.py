import sys
import tkinter as tk
from tkinter import *
import PIL
from PIL import ImageTk, Image

def display_image(filename):
    image = Image.open(filename)
    root = tk.Tk()
    tk_image = ImageTk.PhotoImage(image)
    label = Label(root, image = tk_image)
    label.pack()
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("one parameter expected - path to img")
        sys.exit(1)
    display_image(sys.argv[1])
