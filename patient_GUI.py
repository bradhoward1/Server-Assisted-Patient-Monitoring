# patient_GUI.py

# post request for monitoring GUI-
# sending info to server about which image to download

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import re
from PIL import Image, ImageTk
import base64
import matplotlib.pyplot as plt
import requests


host = "http://vcm-15218.vm.duke.edu:5000"


def posting_method(name, HRS, Fig_name, ECG_to_server, med_record,
                   Med_Image_FN, Conv_MedI):
    """Prepares data for extraction and and upload to the server

    Retrieves all parameters necessary for the monitoring GUI
    and prepares them for extraction in a dictionary. Verifies that
    these parameters satisfy the imposed constraints such that
    they do not interfere with the server's functioning.

    Parameters
    ----------
    name : string
        patient name
    HRS : int
        patient average heart rate
    Fig_name : string
        name of generated ECG plot
    ECG_to_server : string
        encoded ECG plot
    med_record : string
        patient medical record number
    Med_Image_FN : string
        filename of selected medical image
    Conv_MedI : string
        encoded medical image

    Returns
    -------
    Dictionary
        Output information to server"""
    # Post request to server, create dictionary here
    out_dict = {}
    list_parameters = [name, HRS, Fig_name, ECG_to_server, med_record,
                       Med_Image_FN, Conv_MedI]
    # print(list_parameters)
    for parameter in list_parameters:
        if parameter == med_record:
            if med_record is None or med_record == "":
                continue
            else:
                out_dict["medical_record_number"] = med_record
        elif parameter == name:
            if name is None or name == "":
                continue
            else:
                out_dict["patient_name"] = name
        elif parameter == HRS:
            if HRS is None or HRS == "":
                continue
            else:
                out_dict["heart_rate"] = HRS
        elif parameter == Med_Image_FN:
            if Med_Image_FN is None or Med_Image_FN == "":
                continue
            else:
                out_dict["medical_image"] = [Med_Image_FN]
        elif parameter == Conv_MedI:
            if Conv_MedI is None or Conv_MedI == "":
                continue
            else:
                out_dict["medical_image"].append(Conv_MedI)
        elif parameter == Fig_name:
            if Fig_name is None or Fig_name == "":
                continue
            else:
                out_dict["ECG_image"] = [Fig_name]
        elif parameter == ECG_to_server:
            if ECG_to_server is None or ECG_to_server == "":
                continue
            else:
                out_dict["ECG_image"].append(ECG_to_server)
    return out_dict


def get_available_files():
    """Retrieves existing patient data files

    Retrieves all files in the test_data folder.

    Parameters
    ----------
    N/A

    Returns
    -------
    List
        List of file names as strings"""
    import os
    all_files = os.listdir("test_data/")
    files = [f for f in all_files if ".csv" in f]
    files.sort(key=lambda f: int(re.sub('\D', '', f)))
    return files


def load_image_for_display(filename):
    """Loads image for viewing

    Processes image for viewing and resizes appropriately
    to conform to the dimensions of the GUI.

    Parameters
    ----------
    filename : string
        String containing the filename of the designated file

    Returns
    -------
    PhotoImage
    Desired image to be displayed"""
    print(filename)
    image_obj = Image.open(filename)
    width, height = image_obj.size
    new_width = int(200)
    new_height = int(150)
    image_obj = image_obj.resize((new_width, new_height))
    tk_image = ImageTk.PhotoImage(image_obj)
    return tk_image


def convert_file_to_b64str(filename):
    """Converts file to encoded image

    Processes image for upload to server and saves the image.

    Parameters
    ----------
    filename : string
        String with name of file

    Returns
    -------
    String
        Decoded image"""
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def design_window():
    """Creates Interface

    Creates the GUI to display all necessary information

    Parameters
    ----------
    N/A

    Returns
    -------
    N/A"""

    def cancel_cmd():
        """Terminates interface

        Closes out interface

        Parameters
        ----------
        N/A

        Returns
        -------
        N/A"""
        root.destroy()

    def ok_button_work():
        """Ok button method

        Obtains data from designated patient medical record
        such as patient name, calculates average heart rate
        data, and grabs appropriate timestamp. Generates
        corresponding plots with input data.

        Parameters
        ----------
        N/A

        Returns
        -------
        N/A"""
        nonlocal name, HRS, Fig_name, ECG_to_server, med_record
        nonlocal Converted_IM, output
        fn = file_name.get()
        print("Patient Medical Record Number is {}".
              format(medical_record_entry.get()))
        print("Selected ECG file is {}".format(ECG_select.get()))
        from ecg_analysis import run_ecg_from_gui
        if ECG_select.get() == "Select file":
            answers = {"mean_hr_bpm": None, "times": None, "voltages": None}
        else:
            answers = run_ecg_from_gui(ECG_select.get())
        HRS = answers["mean_hr_bpm"]
        if HRS is not None:
            HRS = round(HRS)
        name = name_entry.get()
        Time = answers["times"]
        Voltage = answers["voltages"]
        HHR_label = ttk.Label(root, text="Mean Heart Rate: {} BPM".
                              format(HRS))
        HHR_label.grid(column=0, row=8)
        Fig_name = None
        ECG_to_server = None
        if Time is not None:
            plt.clf()
            plt.plot(Time, Voltage)
            plt.xlabel("Time (seconds)")
            plt.ylabel("Voltage (V)")
            plt.title("Voltage as a function of time")
            Fig_name = ECG_select.get().split(".")[0] + ".jpg"
            plt.savefig(Fig_name)
            ECG_trace = load_image_for_display(Fig_name)
            image_label = ttk.Label(root, image=ECG_trace)
            image_label.grid(column=5, row=5)
            image_label.image = ECG_trace
            ECG_to_server = convert_file_to_b64str(Fig_name)
        med_record = medical_record_entry.get()
        output = posting_method(name, HRS, Fig_name, ECG_to_server,
                                med_record, fn, Converted_IM)

    def post_cmd():
        """Posts new patient info to the server

        Completes the post request of patient information
        to the server.

        Parameters
        ----------
        N/A

        Returns
        -------
        N/A"""
        print("Running post command")
        fn = file_name.get()
        r = requests.post(host + "/add_new_patient", json=output)
        print("{}, {}".format(r.text, r.status_code))

    def upload_img():
        """Converts image

        Method encodes image from PhotoImage
        to string.

        Parameters
        ----------
        N/A

        Returns
        -------
        N/A"""
        fn = file_name.get()
        b64 = convert_file_to_b64str(fn)
        return b64

    def get_picture():
        """Grabs designated picture for display

        Displays selected image in the GUI

        Parameters
        ----------
        N/A

        Returns
        -------
        N/A"""
        nonlocal Converted_IM
        fn = filedialog.askopenfilename()
        file_name.set(fn)
        fn = file_name.get()
        tk_image = load_image_for_display(fn)
        image_label.configure(image=tk_image)
        image_label.image = tk_image
        Converted_IM = upload_img()

    root = tk.Tk()
    root.title("Patient Interface")

    top_description = ttk.Label(root, text="Patient Interface")
    top_description.grid(column=0, row=0, columnspan=2, sticky="W")

    name_label = ttk.Label(root, text="Name")
    name_label.grid(column=2, row=0)

    name_entry = tk.StringVar()
    name_entry_box = ttk.Entry(root, width=30, text=name_entry)
    name_entry_box.grid(column=2, row=1)
    ttk.Label(root, text="Patient ECG File").grid(column=2, row=3)

    ECG_select = tk.StringVar()
    ECG_select.set("Select file")
    ECG_box = ttk.Combobox(root, width=30, textvariable=ECG_select)
    ECG_box['values'] = get_available_files()
    ECG_box.state(['readonly'])
    ECG_box.grid(column=2, row=4)

    file_name = tk.StringVar()
    Converted_IM = None
    HRS = None
    Fig_name = None
    ECG_to_server = None
    med_record = None
    name = None
    output = None
    Pic_label = ttk.Label(root, text="Picture Upload")
    Pic_label.grid(column=3, row=3)
    Pic_button = ttk.Button(root, text="Upload", command=get_picture)
    Pic_button.grid(column=3, row=4)

    ok_button = ttk.Button(root, text="Ok", command=ok_button_work)
    ok_button.grid(column=5, row=0)

    cancel_button = ttk.Button(root, text="Cancel", command=cancel_cmd)
    cancel_button.grid(column=5, row=4)

    send_button = ttk.Button(root, text="Send", command=post_cmd)
    send_button.grid(column=5, row=2)

    ttk.Label(root, text="Patient Medical Record").grid(column=3, row=0)
    medical_record_entry = tk.StringVar()
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
