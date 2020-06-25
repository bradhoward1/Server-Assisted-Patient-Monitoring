# monitoring_GUI.py

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import re
from PIL import Image, ImageTk
import base64
import matplotlib.pyplot as plt
import requests


host = "http://vcm-15218.vm.duke.edu:5000"


def load_image_for_display(filename):
    print(filename)
    image_obj = Image.open(filename)
    width, height = image_obj.size
    new_width = int(200)
    new_height = int(150)
    image_obj = image_obj.resize((new_width, new_height))
    tk_image = ImageTk.PhotoImage(image_obj)
    return tk_image

def convert_b64str_to_file(pic_info):
    filename = pic_info[0]
    image_bytes = pic_info[1]
    decoded_image = base64.b64decode(image_bytes)
    with open(filename, "wb") as out_file:
        out_file.write(decoded_image)
    return filename

def get_medical_records():
    r = requests.get(host + "/patient_list")
    r = r.json()
    return r


# Get request for patient medical records

def design_window():

    def cancel_cmd():
        root.destroy()

    def get_select_patient_info(Patient):
        r = requests.get(host + "/name_hr_ecg/" + Patient)
        r = r.json()
        patient_display_list = [r["name"], r["latest_hr"], r["latest_datetime"]]
        ECG_list = r["latest_ECG_image"]
        return patient_display_list, ECG_list

    def get_ECG_trace():
        nonlocal Selected_Medical_Record
        r = requests.get(host + "ECG_timestamps/" + Selected_Medical_Record)
        my_dict = r.json()
        ECG_images = my_dict["ECG_images"]
        timestamps = my_dict["timestamps"]

    def MEDR_button_work():
        Selected_Medical_Record = MEDR_select.get()
        patient_display_list, ecg_list = get_select_patient_info(x)
        patient_data = patient_display_list
        patient_data[0] = "Patient Name: " + patient_data[0]
        HR = patient_data[1]
        patient_data[1] = "Patient Heart Rate: {}".format(HR)
        patient_data[2] = "Datetime: " + patient_data[2].strip("{}")
        patient_data.append("Medical Record: " + x)
        patient_data[3] = patient_data[3].strip("{}")
        MEDR_label = ttk.Label(root, text=patient_data)
        latest_ECG = convert_b64str_to_file(ecg_list)
        image = load_image_for_display(latest_ECG)
        image_label = ttk.Label(root, image=image)
        image_label.image = image
        image_label.grid(column=0, row=5)
        # print(type(latest_ECG))
        MEDR_label.grid(column=3, row=5)
        get_ECG_trace()


    def Trace_select_button():
        nonlocal Selected_Medical_Record



    root = tk.Tk()
    root.title("Monitoring Interface")

    top_description = ttk.Label(root, text="Monitoring Interface")
    top_description.grid(column=0, row=0, columnspan=2, sticky="W")

    MEDR_button = ttk.Button(root, text="Confirm Medical Record Selection", command=MEDR_button_work)
    MEDR_button.grid(column=2, row=2)

    MEDR_select = tk.StringVar()
    MEDR_select.set("Select Medical Record")
    MEDR_box = ttk.Combobox(root, width=30, textvariable=MEDR_select)
    MEDR_box['values'] = get_medical_records()
    MEDR_box.state(['readonly'])
    MEDR_box.grid(column=2, row=3)

    cancel_button = ttk.Button(root, text="Cancel", command=cancel_cmd)
    cancel_button.grid(column=5, row=4)

    Trace_select = tk.StringVar()
    Trace_select.set("Select Patient ECG Trace")
    Trace_box = ttk.Combobox(root, width=30, textvariable=Trace_select)
    Trace_box['values'] = get_ECG_trace()
    Trace_box.state(['readonly'])
    Trace_box.grid(column=3, row=3)

    Trace_button = ttk.Button(root, text="Confirm ECG Trace", command=cancel_cmd)
    Trace_button.grid(column=3, row=2)

    # root.after(3000)
    root.mainloop()
    print("Finished")

if __name__ == "__main__":
    design_window()
    get_medical_records()
