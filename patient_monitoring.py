# patient_monitoring.py

# blood_gui.py

# Be aware of non_local variables
import tkinter as tk
from tkinter import ttk
import re


def get_available_files():
    import os
    all_files = os.listdir("test_data/")
    files = [f for f in all_files if ".csv" in f]
    files.sort(key=lambda f: int(re.sub('\D', '', f)))
    return files


def design_window():

    def cancel_cmd():
        root.destroy()

    def ok_button_work():
        print("Database Entry:")
        name = name_entry.get()
        print("Name is: {} ".format(name))
        print("Patient Medical Record Number is {}{}".
              format(medical_record_entry.get()))
        print("Selected ECG file is {}".format(ECG_select.get()))
        # from ecg file import run_ecg_from_gui
        # answers = run_ecg_from_gui(file_choice.get())
        # this line below should return the output from the method
        # ttk.Label(root, text=answers).grid(column=0, row=10)

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
    root.mainloop()
    print("Finished")

    # move to brad's ecg file once obtained
    # def run_ecg_from_gui(filename):
    # import json
    # fn = filename.split('.')
    # in_file = open("{}".format)fn[0])), 'r')
    # metrics = json.load(in_file)
    # return metrics

if __name__ == "__main__":
    design_window()
    get_available_files()
