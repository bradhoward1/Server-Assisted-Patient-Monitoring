# project_server.py

from flask import Flask, request, jsonify
from datetime import datetime
from pymodm import connect, MongoModel, fields
import PIL

connect("mongodb+srv://brad_howard:NA@cluster0-lucsp.mongodb.net"
        "/another_rando?retryWrites=true&w=majority")


app = Flask(__name__)


class Patient(MongoModel):
    mr_number = fields.IntegerField(primary_key=True)
    name = fields.CharField()
    heart_rates = fields.ListField()
    medical_images = fields.ListField()
    ECG_images = fields.ListField()
    datetimes = fields.ListField()


def __init__():
    print("Server is on.")


def add_new_patient_to_db(in_dict):
    """Adds a new patient to the database

    Every time the user wants to add a new patient
    to the patient database, this function
    must be called. This function reads in from the user the
    any available information. This information could be
    medical record number, patient name, a medical image,
    an ECG image, and a heart rate. The minimum requirement
    is to have a medical record number within the
    dictionary.

    Parameters
    ----------
    in_dict : dict
        Gives the patient information

    Returns
    -------
    bool
        True if successful
    """
    new_patient = Patient()
    keys_present = check_keys(in_dict)
    for key in keys_present:
        if key == "medical_record_number":
            new_patient.mr_number = in_dict[key]
        elif key == "patient_name":
            new_patient.name = in_dict[key]
        elif key == "medical_image":
            new_patient.medical_images = [in_dict[key]]
        elif key == "heart_rate":
            new_patient.heart_rates = [in_dict[key]]
            recorded_datetime = datetime.now()
            string_recorded_datetime = datetime.strftime(
                    recorded_datetime,  "%Y-%m-%d %H:%M:%S")
            new_patient.datetimes = [string_recorded_datetime]
        elif key == "ECG_image":
            new_patient.ECG_images = [in_dict[key]]
        new_patient.save()
    return True


def edit_existing_patient(in_dict):
    """Edits a patient that already exists in the database

    If the user wants to edit a patient that already exists
    in the database, they must use this function. This
    function searches the database for the patient
    with the medical record number matching the one
    within the input dictionary. Once it finds this
    patient, it updates their information, adding
    whatever is contained within the input dictionary.
    If there is a problem with the information,
    the function will notify the user. Otherwise,
    it will return True.

    Parameters
    ----------
    in_dict : dict
        Gives the patient information

    Returns
    -------
    bool
        True if successful
    """
    keys_present = check_keys(in_dict)
    for key in keys_present:
        if key == "patient_name":
            existing_patient = Patient.objects.raw({"_id": in_dict
                                                    ["medical_record_number"]
                                                    }).first()
            existing_patient.name = in_dict["patient_name"]
            existing_patient.save()
        elif key == "medical_image":
            existing_patient = Patient.objects.raw({"_id": in_dict
                                                    ["medical_record_number"]
                                                    })
            existing_patient.update({"$push": {"medical_images":
                                    in_dict['medical_image']}})
        elif key == "heart_rate":
            existing_patient = Patient.objects.raw({"_id": in_dict
                                                    ["medical_record_number"]
                                                    })
            existing_patient.update({"$push": {"heart_rates":
                                    in_dict['heart_rate']}})
            recorded_datetime = datetime.now()
            string_recorded_datetime = datetime.strftime(
                    recorded_datetime,  "%Y-%m-%d %H:%M:%S")
            existing_patient.update({"$push":
                                    {"datetimes": string_recorded_datetime}})
        elif key == "ECG_image":
            existing_patient = Patient.objects.raw({"_id": in_dict
                                                    ["medical_record_number"]
                                                    })
            existing_patient.update({"$push": {"ECG_images":
                                    in_dict['ECG_image']}})
    return True


def check_keys(in_dict):
    """Checks which keys are present within the input dictionary

    This function looks within the input dictionary and checks
    which keys are contained within it. Then, with these
    keys, it generates a list containing these keys and
    returns this list as output.

    Parameters
    ----------
    in_dict : dict
        Gives the patient information

    Returns
    -------
    list
        Contains the keys within the dictionary
    """
    my_keys = list(in_dict.keys())
    return my_keys


def validate_inputs(in_dict):
    """Validates the inputs of the incoming dictionary

    Once it is known which keys are present within the incoming
    dictionary, it is necessary to check if the key values are
    of the correct type. To make sure that each key value is
    correct, it iterates through the key list, extracts the value,
    then will continue to the next key if the previous one
    is correct. If a key does not contain the correct value
    type, then the function will notify the user. Otherwise,
    the function will return True.

    Parameters
    ----------
    in_dict : dict
        Gives the patient information

    Returns
    -------
    bool
        True if successful
    """
    keys_present = check_keys(in_dict)
    for key in keys_present:
        if key == "medical_record_number":
            if type(in_dict[key]) == str:
                in_dict[key] = int(in_dict[key])
                continue
            elif type(in_dict[key]) == int:
                continue
            else:
                return "There was an unacceptable input, try again"
        if key == "patient_name":
            if type(in_dict[key]) == str:
                continue
            else:
                return "There was an unacceptable input, try again"
        if key == "medical_image":
            if type(in_dict[key]) == str:
                return "There was an unacceptable input, try again"
            elif type(in_dict[key]) == int:
                return "There was an unacceptable input, try again"
            elif type(in_dict[key]) == tuple:
                continue
            elif type(in_dict[key] == list):
                in_dict[key] = tuple(in_dict[key])
            else:
                return "There was an unacceptable input, try again"
        if key == "heart_rate":
            if type(in_dict[key]) == int:
                continue
            else:
                return "There was an unacceptable input, try again"
        if key == "ECG_image":
            if type(in_dict[key]) == str:
                return "There was an unacceptable input, try again"
            elif type(in_dict[key]) == int:
                return "There was an unacceptable input, try again"
            elif type(in_dict[key]) == tuple:
                continue
            elif type(in_dict[key] == list):
                in_dict[key] = tuple(in_dict[key])
            else:
                return "There was an unacceptable input, try again"
    return True


@app.route("/add_new_patient", methods=["POST"])
def post_add_patient_to_db():
    """Posts patient information to the server

    This method generates the new patient's
    dictionary with all of his/her information, then validates
    that all of the information is the correct type. If the
    validation stage is satisfied, then the new patient's
    dictionary is added to the database.

    Parameters
    ----------
    N/A

    Returns
    -------
    String
        result of adding a new patient
    """
    in_dict = request.get_json()
    var = validate_inputs(in_dict)
    print(var)
    if var is True:
        try:
            presence_check = Patient.objects.get({"_id":
                                                 in_dict
                                                 ["medical_record_number"]})
        except Patient.DoesNotExist:
            presence_check = False
        if presence_check is not False:
            edit_existing_patient(in_dict)
            return "Good post made to database", 200
        else:
            add_new_patient_to_db(in_dict)
            return "Good new post made to database", 200
    else:
        return "Not an acceptable post, try again", 400


def patient_list():
    """Creates a list of all medical record numbers in the database

    This method searches through the database to find all of the medical
    record numbers present. Once it is able to find all of them, it
    puts them all in a list, which is then returned.

    Parameters
    ----------
    N/A

    Returns
    -------
    list
        Contains all medical record numbers
    """
    my_patient_list = list()
    for patient in Patient.objects.raw({}):
        my_patient_list.append(patient.mr_number)
    return my_patient_list


@app.route("/patient_list", methods=["GET"])
def get_patient_list():
    """Gets all medical record numbers from the server

    This method asks the server to return all of the
    medical record numbers. Once the list is generated,
    it returns the list as well as a status code.

    Parameters
    ----------
    N/A

    Returns
    -------
    list
        Contains all medical record numbers
    """
    my_patient_list = patient_list()
    print(my_patient_list)
    return jsonify(my_patient_list), 200


def name_latest_hr_and_ECG_image(mr_num):
    """Gets name, heart rate, ECG image, and datetime of a patient

    This method takes in a specific medical record number as input.
    With this medical record number, the function searches through
    the database to find the patient with that matching medical
    record number. Once this patient is found, this function will
    find the patient's name, latest heart rate/ECG image, and
    the datetime at which this heart rate/ECG image was put
    into the database. With this information, the function
    generates a dictionary, which is returned.

    Parameters
    ----------
    mr_num: int or String
        Contains the medical record number of a patient

    Returns
    -------
    dict
        Contains patient information
    """
    mr_num = int(mr_num)
    patient = Patient.objects.raw({"_id": mr_num}).first()
    patient_name = patient.name
    patient_heart_rates = patient.heart_rates
    patient_ECG_images = patient.ECG_images
    patient_datetimes = patient.datetimes
    size_of_hr_list = len(patient_heart_rates)
    size_of_patient_ECG_images = len(patient_ECG_images)
    latest_hr = patient_heart_rates[size_of_hr_list-1]
    latest_ECG_image = patient_ECG_images[size_of_patient_ECG_images-1]
    latest_datetime = patient_datetimes[size_of_hr_list-1]
    out_dict = {"name": patient_name,
                "latest_hr": latest_hr,
                "latest_ECG_image": latest_ECG_image,
                "latest_datetime": latest_datetime}
    return out_dict


@app.route("/name_hr_ecg/<mr_num>", methods=["GET"])
def get_name_latest_hr_and_ECG_image(mr_num):
    """Gets patient information from the server

    This method takes in a medical record number as input
    and uses it to search for the specified patient
    within the database. Once this patient is found,
    it returns a dictionary containing the patient's
    name, latest heart rate/ECG image, and the datetime
    of this. If it is unable to create this dictionary,
    then it will inform the user.

    Parameters
    ----------
    mr_num: int
        Contains the medical record number of a patient

    Returns
    -------
    dict
        Contains patient information
    """
    contents = name_latest_hr_and_ECG_image(mr_num)
    if contents:
        return jsonify(contents), 200
    else:
        return "Unable to return the contents, try again", 400


def timestamps_list(mr_num):
    """Generates a list of timestamps for a given patient

    This function takes in a medical record number as input.
    With this medical record number, this function searches
    through the database for that patient and generates
    a list of timestamps for that patient. This list is then
    returned.

    Parameters
    ----------
    mr_num : int
        Contains the medical record number of a patient

    Returns
    -------
    list
        Contains all timestamps within the database for given patient
    """
    mr_num = int(mr_num)
    patient = Patient.objects.raw({"_id": mr_num}).first()
    patient_timestamp_list = patient.datetimes
    return patient_timestamp_list


def ECG_image_list(mr_num):
    """Generates a list of ECG images for a given patient

    This function takes in a medical record number as input.
    With this medical record number, this function searches
    through the database for that patient and generates
    a list of ECG images for that patient. This list is then
    returned.

    Parameters
    ----------
    mr_num : int
        Contains the medical record number of a patient

    Returns
    -------
    list
        Contains all ECG images within the database for given patient
    """
    patient_list = list()
    mr_num = int(mr_num)
    patient = Patient.objects.raw({"_id": mr_num}).first()
    patient_ECG_list = patient.ECG_images
    for patient in patient_ECG_list:
        patient = patient[0]
        patient_list.append(patient)
    return patient_list


@app.route("/ECG_timestamps/<mr_num>", methods=["GET"])
def get_timestamps_list(mr_num):
    """Gets a list of ECG images from the server

    This function takes in a medical record number as input.
    With this medical record number, this function asks
    the server to generate a list of ECG images for the given
    patient. Once this list is generated, the server returns
    the list. If it is unable to generate the list, it will
    notify the user.

    Parameters
    ----------
    mr_num : int
        Contains the medical record number of a patient

    Returns
    -------
    list
        Contains all ECG images within the database for given patient
    """
    timestamps = timestamps_list(mr_num)
    images = ECG_image_list(mr_num)
    contents = {"timestamps": timestamps,
                "ECG_images": images}
    if contents:
        return jsonify(contents), 200
    else:
        return "Unable to retrieve list of timestamps", 400


def medical_image_list(mr_num):
    """Generates a list of medical images for a given patient

    This function takes in a medical record number as input.
    With this medical record number, this function searches
    through the database for that patient and generates
    a list of medical images for that patient. This list is then
    returned.

    Parameters
    ----------
    mr_num : int
        Contains the medical record number of a patient

    Returns
    -------
    list
        Contains all medical images within the database for given patient
    """
    patient_list = list()
    mr_num = int(mr_num)
    patient = Patient.objects.raw({"_id": mr_num}).first()
    patient_image_list = patient.medical_images
    for patient in patient_image_list:
        patient = patient[0]
        patient_list.append(patient)
    return patient_list


@app.route("/medical_images/<mr_num>", methods=["GET"])
def get_medical_image_list(mr_num):
    """Gets a list of medical images from the server

    This function takes in a medical record number as input.
    With this medical record number, this function asks
    the server to generate a list of medical images for the given
    patient. Once this list is generated, the server returns
    the list. If it is unable to generate the list, it will
    notify the user.

    Parameters
    ----------
    mr_num : int
        Contains the medical record number of a patient

    Returns
    -------
    list
        Contains all medical images within the database for given patient
    """
    contents = medical_image_list(mr_num)
    if contents:
        return jsonify(contents), 200
    else:
        return "Unable to retrieve list of medical images", 400


def validate_ECG_image_timestamp(in_dict):
    """Validates the inputs of the incoming dictionary

    This function receives a dictionary as input. Within this
    dictionary are a patient's medical record number as well
    as a specific timestamp for that patient. This function
    checks to ensure that the medical record number is an int
    and checks to ensure that the timestamp is a string. If
    these are not the case, it will inform the user. Otherwise,
    it will return True

    Parameters
    ----------
    in_dict : dict
        Gives the patient medical record number and timestamp

    Returns
    -------
    bool
        True if successful
    """
    my_keys = list(in_dict.keys())
    for key in my_keys:
        if key == "patient":
            if type(in_dict[key]) == int:
                continue
            else:
                return "A valid patient id was not provided, try again"
        if key == "timestamp":
            if type(in_dict[key]) == str:
                continue
            else:
                return "A valid timestamp was not provided, try again"
        else:
            return "The input dictionary has unusable information, try again"
    return True


def ECG_image_timestamp(in_dict):
    """Finds an ECG image based on a specific patient timestamp

    This function takes in a dictionary containing a patient
    medical record number as well as a specific timestamp as
    input. With this information, it searches through the database
    to find that patient. Once the patient is found, it searches through
    the list of timestamps for that patient and finds the specified one
    within the input dictionary. Once this timestamp is found, its index
    is determined. This index is then used to find the ECG image
    that was inputted at this datetime. Once the image is found,
    it is returned.

    Parameters
    ----------
    in_dict : dict
        Gives the patient medical record number and timestamp

    Returns
    -------
    tuple
        Contains file name and its corresponding base64 string
    """
    patient_id = in_dict["patient"]
    patient_timestamp = in_dict["timestamp"]
    patient = Patient.objects.raw({"_id": patient_id}).first()
    patient_timestamps = patient.datetimes
    patient_ECG_images = patient.ECG_images
    index = patient_timestamps.index(patient_timestamp)
    patient_ECG_output = patient_ECG_images[index]
    return patient_ECG_output


@app.route("/ECG_image_timestamp", methods=["POST"])
def post_ECG_image_timestamp():
    """Gets an ECG image based on a specific patient timestamp from server

    This function generates an ECG image based on a specific timestamp
    for a specific patient. It gets a medical record number and uses it
    to find a patient. Once the patient is found, it searches through
    the list of timestamps for that patient and finds the specified one
    within the input dictionary. Once this timestamp is found, its index
    is determined. This index is then used to find the ECG image
    that was inputted at this datetime. Once the image is found,
    it is returned.

    Parameters
    ----------
    N/A

    Returns
    -------
    tuple
        Contains file name and its corresponding base64 string
    """
    in_dict = request.get_json()
    tester = validate_ECG_image_timestamp(in_dict)
    print(tester)
    if tester is True:
        patient_ECG_output = ECG_image_timestamp(in_dict)
        patient_ECG_output = tuple(patient_ECG_output)
        return jsonify(patient_ECG_output), 200
    else:
        return "Not a valid input, try again", 400


def validate_medical_image_specific(in_dict):
    """Validates the inputs of the incoming dictionary

    This function receives a dictionary as input. Within this
    dictionary are a patient's medical record number as well
    as a specific file name for that patient. This function
    checks to ensure that the medical record number is an int
    and checks to ensure that the file name is a string. If
    these are not the case, it will inform the user. Otherwise,
    it will return True

    Parameters
    ----------
    in_dict : dict
        Gives the patient medical record number and file name

    Returns
    -------
    bool
        True if successful
    """
    my_keys = list(in_dict.keys())
    for key in my_keys:
        if key == "patient":
            if type(in_dict[key]) == int:
                continue
            else:
                return "A valid patient id was not provided, try again"
        if key == "file_name":
            if type(in_dict[key]) == str:
                continue
            else:
                return "A valid filename was not provided, try again"
        else:
            return "The input dictionary has unusable information, try again"
    return True


def medical_image_filename(in_dict):
    """Generates a medical image based on a file name

    This function receives a dictionary as input. Within this
    dictionary are a patient's medical record number as well
    as a file name for a medical image for that patient.
    With this information, it searches through the database
    to find that patient. Once the patient is found, it searches
    through the list of medical images for that patient and finds
    the specified one within the input dictionary.
    Once this medical image is found, its index
    is determined. This index is then used to find the medical image
    that was inputted with this file name. Once the image is found,
    it is returned.

    Parameters
    ----------
    in_dict : dict
        Gives the patient medical record number and file name

    Returns
    -------
    bool
        True if successful
    """
    patient_file_names = list()
    patient_images = list()
    patient_id = in_dict["patient"]
    patient_filename = in_dict["file_name"]
    patient = Patient.objects.raw({"_id": patient_id}).first()
    patient_medical_images = patient.medical_images
    for image in patient_medical_images:
        patient_file_names.append(image[0])
        patient_images.append(image[1])
    index = patient_file_names.index(patient_filename)
    patient_image = patient_medical_images[index]
    return patient_image


@app.route("/get_medical_image", methods=["POST"])
def retrieve_medical_image():
    """Gets a medical image based on a file name

    This function generates a medical image based on a specific file name
    for a specific patient. It gets a medical record number and uses it
    to find a patient. Once the patient is found, it searches through
    the list of medical images for that patient and finds the specified one
    within the input dictionary. Once this file name is found, its index
    is determined. This index is then used to find the medical image
    that was inputted at this datetime. Once the image is found,
    it is returned.

    Parameters
    ----------
    N/A

    Returns
    -------
    String
        Contains name of the medical image
    """
    in_dict = request.get_json()
    var = validate_medical_image_specific(in_dict)
    if var is True:
        patient_image = medical_image_filename(in_dict)
        return jsonify(patient_image), 200
    else:
        return "Unable to retrieve image", 400


if __name__ == '__main__':
    __init__()
    app.run()
    # patient_list()
