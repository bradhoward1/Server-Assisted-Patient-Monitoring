# patient_GUI.py

# post request for monitoring GUI-
# sending info to server about which image to download

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import re
from PIL import Image, ImageTk
import base64


def get_available_files():
    import os
    all_files = os.listdir("test_data/")
    files = [f for f in all_files if ".csv" in f]
    files.sort(key=lambda f: int(re.sub('\D', '', f)))
    return files


def load_image_for_display(filename):
    print(filename)
    image_obj = Image.open(filename)
    width, height = image_obj.size
    new_width = int(200)
    new_height = int(150)
    image_obj = image_obj.resize((new_width, new_height))
    tk_image = ImageTk.PhotoImage(image_obj)
    return tk_image

def convert_file_to_b64str(filename):
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def design_window():

    def cancel_cmd():
        root.destroy()

    def ok_button_work():
        # create_window()
        print("Database Entry:")
        name = name_entry.get()
        print("Name is: {} ".format(name))
        print("Patient Medical Record Number is {}".
              format(medical_record_entry.get()))
        print("Selected ECG file is {}".format(ECG_select.get()))
        from ecg_analysis import run_ecg_from_gui
        answers = run_ecg_from_gui(ECG_select.get())
        lst = [answers["duration"],
               answers["voltage_extremes"],
               answers["num_beats"],
               answers["mean_hr_bpm"]]
        HRS = round(answers["mean_hr_bpm"])
        HHR_label = ttk.Label(root, text= "Mean Heart Rate: {} BPM".format(HRS))
        HHR_label.grid(column=0, row=8)

    def get_picture():
        fn = filedialog.askopenfilename()
        file_name.set(fn)
        fn = file_name.get()
        tk_image = load_image_for_display(fn)
        image_label.configure(image=tk_image)
        image_label.image = tk_image

    def upload_img():
        fn = file_name.get()
        b64 = convert_file_to_b64str(fn)
        return_msg = send_b64image_to_server(b64)
        result_label.configure(text=return_msg)

    root = tk.Tk()
    root.title("Patient Interface")


    top_description = ttk.Label(root, text="Patient Interface")
    top_description.grid(column=0, row=0, columnspan=2, sticky="W")

    name_label = ttk.Label(root, text="Name")
    name_label.grid(column=2, row=0)

    name_entry = tk.StringVar()
    name_entry.set("Enter your name")
    name_entry_box = ttk.Entry(root, width=30, textvariable=name_entry)
    name_entry_box.grid(column=2, row=1)
    ttk.Label(root, text="Patient ECG File").grid(column=2, row=3)

    ECG_select = tk.StringVar()
    ECG_select.set("Select file")
    ECG_box = ttk.Combobox(root, width=30, textvariable=ECG_select)
    ECG_box['values'] = get_available_files()
    ECG_box.state(['readonly'])
    ECG_box.grid(column=2, row=4)

    file_name = tk.StringVar()
    # file_name_box = ttk.Entry(root, textvariable=file_name)
    Pic_label = ttk.Label(root, text="Picture Upload")
    Pic_label.grid(column=3, row=3)
    Pic_button = ttk.Button(root, text="Upload", command=get_picture)
    Pic_button.grid(column=3, row=4)

    ok_button = ttk.Button(root, text="Ok", command=ok_button_work)
    ok_button.grid(column=5, row=0)

    cancel_button = ttk.Button(root, text="Cancel", command=cancel_cmd)
    cancel_button.grid(column=5, row=4)

    ttk.Label(root, text="Patient Medical Record").grid(column=3, row=0)
    medical_record_entry = tk.StringVar()
    medical_record_entry.set("Enter medical record #")
    medical_record_entry_box = ttk.Entry(root, width=30,
                                         textvariable=medical_record_entry)
    medical_record_entry_box.grid(column=3, row=1)

    initial_image = load_image_for_display("Winston copy.png")
    image_label = ttk.Label(root, image=initial_image)
    image_label.grid(column=0, row=5)

    root.mainloop()
    print("Finished")


if __name__ == "__main__":
    design_window()
    get_available_files()
