# monitoring_GUI.py

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import re
from PIL import Image, ImageTk
import base64
import matplotlib.pyplot as plt

def load_image_for_display(filename):
    print(filename)
    image_obj = Image.open(filename)
    width, height = image_obj.size
    new_width = int(200)
    new_height = int(150)
    image_obj = image_obj.resize((new_width, new_height))
    tk_image = ImageTk.PhotoImage(image_obj)
    return tk_image

def convert_b64str_to_file(filename):
image_bytes = base64.b64decode(b64_string)
with open(new_filename, "wb") as out_file:
    out_file.write(image_bytes)

def design_window():

    def cancel_cmd():
        root.destroy()
