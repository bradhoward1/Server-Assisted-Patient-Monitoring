[![Build Status](https://travis-ci.com/BME547-Summer2020/final-project-audibuild.svg?token=EEjxyoKhwHKXwyPzUy4i&branch=master)](https://travis-ci.com/BME547-Summer2020/final-project-audibuild)
# Final Project

This README.md file provides an in depth analysis of the functionality of the final-project-audibuild repository.

## Cloud Server

The server is developed in the `project_server.py` Python file. THE SERVER IS CURRENTLY TURNED ON AND LOCATED ON A SEPARATE VIRTUAL MACHINE. The host for this server is "vcm-15218.vm.duke.edu" and is located on port 5000. Thus, when attempting to run functions on the server, the user must ensure that the following is entered as the base URL:

1. "http://vcm-15218.vm.duke.edu:5000"

Within this server, the following functions have been implemented:

+ `POST /add_new_patient`
+ `GET /patient_list`
+ `GET /name_hr_ecg/<mr_num>`
+ `GET /ECG_timestamps/<mr_num>`
+ `GET /medical_images/mr_num`
+ `POST /ECG_image_timestamp`
+ `POST /get_medical_image`

The server file within the virtual machine is different than the server file within this repository. To actually access this server outside of the virtual machine, the following `host` parameter is passed to the Flask handler command:

app.run(host="vcm-15218.vm.duke.edu")

With this change, it is possible to carry out functions in the server while outside of the virtual machine. If the user wanted to test the functionality of the server without the GUIs, he could run the `client_tests.py` file. This file will be able to make post and get requests to the server, effectively accessing the database as well. In line 6 of this file is the host name. It is currently set to `http://127.0.0.1:5000` because it assumes that the server is being run locally. If the user wants to test this file with the server running on the virtual machine, this host name must be changed to `http://vcm-15218.vm.duke.edu:5000`. Because the server is running on the virtual machine, this change must be made by the user, or else it will not allow any of the requests to be made.

The server relies on a MongoDB database to store information. A fully complete entry in the database will contain the structure shown below.

+ _id: contains the patient's medical record number: allows the server to search for a specific patient
+ name: contains the patient's entered name
+ heart_rates: contains a list of inputted heart rate values
+ medical_images: contains a list of tuples where each tuple contains both a file name and the base 64 string for the given file
+ ECG_images: contains a list of tuples where each tuple contains both a file name and the base 64 string for the given file
+ datetimes: contains a list of strings where each string represents a different timestamp for when a heart rate/ ECG image is entered

This structure allows the Patient-side GUI Client to effectively post new patient information to the database while also allowing the Monitoring Station GUI Client to effectively retrieve information from the database.

## Patient-side GUI Client

The Patient-side GUI Client is focused towards patients looking to enter their information into the database. It first requires that the user at least inputs a medical record number. As long as a medical record number is present, the patient can enter their name, upload a medical image, select an ECG data file, generate a heart rate, and generate an image of the ECG data. To enter a name, the patient should fill in the text box below the `Name` Label. To enter a medical record number, the patient should fill in the text box below the `Patient Medical Record` Label. To select an ECG test file, the patient should select a file from the drop down menu located below the `Patient ECG File` Label. And finally, to select a medical image to upload, the patient should click on the `Upload` button located below the `Picture Upload` Label. Once the user has entered information, the only way to stage the information is through the use of the "Ok" Button located in the GUI. If the user presses the "Ok" Button, then their information is staged and ready to be sent to the server. To actually submit the information to the server, though, it is necessary for the user to use the "Send" Button, as this button employs a command that contains the post request necessary to send information to the server and store it in the MongoDB database. IT IS IMPERATIVE TO NOTE THAT THE PATIENT WILL BE UNABLE TO ENTER DIFFERENT MEDICAL RECORD NUMBERS. Once the patient has queued and sent the medical record number to the server, that window no longer can accept another medical record number. If the patient wishes to change the medical record number being entered, the patient must click on the `Cancel` button to close the window, and they must then reopen it to enter new information for a patient with a different medical record number. 

## Monitoring-Station GUI Client
The Monitoring-Station GUI Client is geared towards the provider and enables him/her to access information that has been uploaded. Note that the server automatically refreshes to capture any recently inputted data. The interface first displays all available medical records and the user has the option to select one. The user should select a patient medical record at this point. After a specific medical record has been selected, the corresponding ECG traces for that patient and corresponding medical images are available for viewing. When either of these image types are selected, they are automatically saved locally. All of this data was inputted to the database via the Patient-side GUI prior to running. The user can choose to view ECG traces or medical images, and each time a new image is selected it refreshes in place. To exit the interface the user needs to simply select the cancel button. To reset the GUI, select the reset button. 
