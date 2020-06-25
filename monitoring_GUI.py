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
    image_obj = Image.open(filename)
    width, height = image_obj.size
    new_width = int(200)
    new_height = int(150)
    image_obj = image_obj.resize((new_width, new_height))
    tk_image = ImageTk.PhotoImage(image_obj)
    return tk_image


def convert_b64str_to_file(pic_info):
    """Converts encoded image to file

    Processes image for viewing and saves the image.

    Parameters
    ----------
    pic_info : string
        String containing the filename of the designated file

    Returns
    -------
    PhotoImage
    Desired image to be displayed"""
    filename = pic_info[0].split("/")
    length = len(filename)
    filename = filename[length-1]
    print(filename)
    image_bytes = pic_info[1]
    decoded_image = base64.b64decode(image_bytes)
    with open(filename, "wb") as out_file:
        out_file.write(decoded_image)
    return filename


def get_medical_records():
    """Retrieves records

    Obtains stored medical record numbers via the host + "/patient_list"
    get request.

    Parameters
    ----------
    N/A

    Returns
    -------
    List
    String list of medical records to be displayed"""
    r = requests.get(host + "/patient_list")
    r = r.json()
    return r


# Get request for patient medical records

def design_window():
    """Creates Interface

    Creates the GUI to display all necessary information

    Parameters
    ----------
    N/A

    Returns
    -------
    N/A
    """

    def cancel_cmd():
        """Terminates interface

        Closes out interface

        Parameters
        ----------
        N/A

        Returns
        -------
        N/A
        """
        root.destroy()

    def get_select_patient_info(Patient):
        """Retrieves information of designated patient

        Retrieves the personal information of the selected patient.
        Takes in the patient's medical record as a string. Method returns
        one list containing patient average heart rate, patient name,
        and the datetime of this heart rate. A list of the patient's ECG files
        also returned.

        Parameters
        ----------
        Patient : string
            String containing the patient's medical record.

        Returns
        -------
        List
            List containing patient patient data
        List
            List containing ECG metrics"""
        r = requests.get(host + "/name_hr_ecg/" + Patient)
        r = r.json()
        patient_display_list = [r["name"], r["latest_hr"],
                                r["latest_datetime"]]
        ECG_list = r["latest_ECG_image"]
        return patient_display_list, ECG_list

    def get_ECG_trace(Patient):
        """Obtains a specific ECG trace

        Uses the host + "/ECG_timestamps/" get request to obtain
        all the ECG file names and corresponding encoded images for
        that specific patient.

        Parameters
        ----------
        Patient : string
            String containing the patient's medical record.

        Returns
        -------
        List
            List of ECG file timestamps"""
        r = requests.get(host + "/ECG_timestamps/" + Patient)
        my_dict = r.json()
        ECG_images = my_dict["ECG_images"]
        timestamps = my_dict["timestamps"]
        return timestamps

    def get_medical_image_list(Patient):
        """Obtains list of patient Medical Images

        Uses the host + "/medical_images/" get request to obtain
        all the Medical Images associated with a specific patient.

        Parameters
        ----------
        Patient : string
            String containing the patient's medical record.

        Returns
        -------
        List
            List of tuples of Medical image file names
            and the encoded images."""
        r = requests.get(host + "/medical_images/" + Patient)
        r = r.json()
        return r

    def MEDR_button_work():
        """Medical Record Select Button

        Button which confirms which medical record wants to be
        examined. The method also populates the remaining
        drop down menus with options considering the patient has been
        selected.

        Parameters
        ----------
        N/A

        Returns
        -------
        N/A
        """
        global image_label, MEDR_label
        y = MEDR_select.get()
        patient_display_list, ecg_list = get_select_patient_info(y)
        patient_data = patient_display_list
        patient_data[0] = "Patient Name: " + patient_data[0]
        HR = patient_data[1]
        patient_data[1] = "Patient Heart Rate: {}".format(HR)
        patient_data[2] = "Datetime: " + patient_data[2].strip("{}")
        patient_data.append("Medical Record: " + Selected_Medical_Record)
        patient_data[3] = patient_data[3].strip("{}")
        MEDR_label = ttk.Label(root, text=patient_data)
        latest_ECG = convert_b64str_to_file(ecg_list)
        image = load_image_for_display(latest_ECG)
        image_label = ttk.Label(root, image=image)
        image_label.image = image
        image_label.grid(column=0, row=5)
        MEDR_label.grid(column=3, row=8)
        Trace_name_list = get_ECG_trace(Selected_Medical_Record)
        MedIM_list = get_medical_image_list(Selected_Medical_Record)
        Trace_box['values'] = Trace_name_list
        MEDIM_box['values'] = MedIM_list

    def get_ecg_picture(ecg_timestamp):
        """Obtains a specific ECG trace

        Uses the host + "/ECG_image_timestamp" get request to obtain
        a specific ECG trace for a given patient.

        Parameters
        ----------
        ecg_timestamp : string
            String containing the corresponding datetime of the
            desired image.

        Returns
        -------
        List
            Name of the file and the encoded image"""
        Selected_Medical_Record = int(MEDR_select.get())
        ECG_dict = {"patient": Selected_Medical_Record,
                    "timestamp": ecg_timestamp}
        r = requests.post(host + "/ECG_image_timestamp",
                          json=ECG_dict)
        # takes ecg timestamp and returns encoded image
        r = r.json()
        print(r)
        return r

    def get_medical_image(MED_filename):
        """Obtains a specific Medical Image

        Uses the host + "/get_medical_image" get request to obtain
        a specific medical image for a given patient.

        Parameters
        ----------
        MED_filename : string
            String containing the corresponding filename of the
            desired image.

        Returns
        -------
        List
            Name of the file and the encoded image"""
        # takes medical im filename and returns encoded image
        Selected_Medical_Record = int(MEDR_select.get())
        MED_dict = {"patient": Selected_Medical_Record,
                    "file_name": MED_filename}
        r = requests.post(host + "/get_medical_image", json=MED_dict)
        r = r.json()
        print(r)
        return r

    def Trace_select_button():
        """Selects specific trace

        Selection of designated ECG trace. Decodes
        the image and displays in the GUI.

        Parameters
        ----------
        N/A

        Returns
        -------
        N/A
        """
        global image_label1
        Selected_trace = Trace_select.get()
        print(type(Selected_trace))
        Returned_Trace = get_ecg_picture(Selected_trace)
        Side_ECG = convert_b64str_to_file(Returned_Trace)
        image = load_image_for_display(Side_ECG)
        image_label1 = ttk.Label(root, image=image)
        image_label1.image = image
        image_label1.grid(column=3, row=5)

    def MED_IM_select_button():
        """Button for selecting desired medical image

        Selection of desired medical image. Decodes
        the image and displays in the GUI.

        Parameters
        ----------
        N/A

        Returns
        -------
        N/A
        """
        global image_label2
        Selected_image = MEDIM_select.get()
        print(type(Selected_image))
        Returned_image = get_medical_image(Selected_image)
        Medical_Image = convert_b64str_to_file(Returned_image)
        image = load_image_for_display(Medical_Image)
        image_label2 = ttk.Label(root, image=image)
        image_label2.image = image
        image_label2.grid(column=5, row=5)

    def reset_cmd():
        """Resets interface

        Clears all figures and lables in the GUI and
        sets placeholder vals to blank.

        Parameters
        ----------
        N/A

        Returns
        -------
        N/A
        """
        Trace_select.set("")
        MEDIM_select.set("")
        MEDR_select.set("")
        image_label.grid_forget()
        MEDR_label.grid_forget()
        image_label1.grid_forget()
        image_label2.grid_forget()
        Trace_box['values'] = ""
        MEDIM_box['values'] = ""

    root = tk.Tk()
    root.title("Monitoring Interface")

    top_description = ttk.Label(root, text="Monitoring Interface")
    top_description.grid(column=0, row=0, columnspan=2, sticky="W")

    MEDR_button = ttk.Button(root,
                             text="Confirm Medical Record Selection",
                             command=MEDR_button_work)
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

    Trace_button = ttk.Button(root,
                              text="Confirm ECG Trace",
                              command=Trace_select_button)
    Trace_button.grid(column=3, row=2)

    MEDIM_select = tk.StringVar()
    MEDIM_select.set("Select Patient Medical Image")
    MEDIM_box = ttk.Combobox(root, width=30, textvariable=MEDIM_select)
    MEDIM_box.state(['readonly'])
    MEDIM_box.grid(column=4, row=3)

    MEDIM_button = ttk.Button(root,
                              text="Confirm Medical Image",
                              command=MED_IM_select_button)
    MEDIM_button.grid(column=4, row=2)

    reset_button = ttk.Button(root, text="Reset", command=reset_cmd)
    reset_button.grid(column=5, row=2)

    root.after(3000)
    root.mainloop()
    print("Finished")

if __name__ == "__main__":
    design_window()
    get_medical_records()
