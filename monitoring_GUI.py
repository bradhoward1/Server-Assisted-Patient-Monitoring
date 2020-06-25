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

    def get_ECG_trace(Patient):
        r = requests.get(host + "/ECG_timestamps/" + Patient)
        my_dict = r.json()
        ECG_images = my_dict["ECG_images"]
        # print(ECG_images)
        timestamps = my_dict["timestamps"]
        return timestamps

    def get_medical_image_list(Patient):
        r = requests.get(host + "/medical_images/" + Patient)
        r = r.json()
        return r

    def MEDR_button_work():
        nonlocal Trace_name_list
        Selected_Medical_Record = MEDR_select.get()
        patient_display_list, ecg_list = get_select_patient_info(Selected_Medical_Record)
        patient_data = patient_display_list
        patient_data[0] = "Patient Name: " + patient_data[0]
        HR = patient_data[1]
        patient_data[1] = "Patient Heart Rate: {}".format(HR)
        patient_data[2] = "Datetime: " + patient_data[2].strip("{}")
        patient_data.append("Medical Record: " + Selected_Medical_Record )
        patient_data[3] = patient_data[3].strip("{}")
        MEDR_label = ttk.Label(root, text=patient_data)
        latest_ECG = convert_b64str_to_file(ecg_list)
        image = load_image_for_display(latest_ECG)
        image_label = ttk.Label(root, image=image)
        image_label.image = image
        image_label.grid(column=0, row=5)
        # print(type(latest_ECG))
        MEDR_label.grid(column=3, row=5)
        Trace_name_list = get_ECG_trace(Selected_Medical_Record)
        MedIM_list = get_medical_image_list(Selected_Medical_Record)
        Trace_box['values'] = Trace_name_list
        MEDIM_box['values'] = MedIM_list
        # print(Trace_name_list)

    def get_ecg_picture(ecg_timestamp):
        Selected_Medical_Record = int(MEDR_select.get())
        ECG_dict = {"patient": Selected_Medical_Record, "timestamp": ecg_timestamp}
        r = requests.post(host + "/ECG_image_timestamp", json=ECG_dict)
        # takes ecg timestamp and returns encoded image
        r = r.text
        return r

    def get_medical_image(MED_filename):
        # takes medical im filename and returns encoded image
        Selected_Medical_Record = int(MEDR_select.get())
        MED_dict = {"patient": Selected_Medical_Record, "file_name": MED_filename}
        r = requests.post(host + "/get_medical_image", json=MED_dict)
        r = r.text
        return r

    def Trace_select_button():
        Selected_trace = Trace_select.get()
        print(Selected_trace)
        Returned_Trace = get_ecg_picture(Selected_trace)
        print(Returned_Trace)


    def MED_IM_select_button():
        Selected_image = MEDIM_select.get()
        Returned_image = get_medical_image(Selected_image)
        print(Returned_image)


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

    Trace_name_list = None
    Trace_select = tk.StringVar()
    Trace_select.set("Select Patient ECG Trace")
    Trace_box = ttk.Combobox(root, width=30, textvariable=Trace_select)
    Trace_box.state(['readonly'])
    Trace_box.grid(column=3, row=3)

    Trace_button = ttk.Button(root, text="Confirm ECG Trace", command=Trace_select_button)
    Trace_button.grid(column=3, row=2)


    MEDIM_select = tk.StringVar()
    MEDIM_select.set("Select Patient Medical Image")
    MEDIM_box = ttk.Combobox(root, width=30, textvariable=MEDIM_select)
    MEDIM_box.state(['readonly'])
    MEDIM_box.grid(column=4, row=3)

    MEDIM_button = ttk.Button(root, text="Confirm Medical Image", command=MED_IM_select_button)
    MEDIM_button.grid(column=4, row=2)

    # root.after(3000)
    root.mainloop()
    print("Finished")

if __name__ == "__main__":
    design_window()
    get_medical_records()
