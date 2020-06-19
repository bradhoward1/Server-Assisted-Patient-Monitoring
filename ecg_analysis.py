# ecg_analysis.py


import json
import sys
import logging
import math
from scipy.signal import find_peaks


def import_name():
    """Extract the name of the desired test file using command line arguments

    When running the ecg_analysis.py program, the user is asked to provide
    the name of the desired test file in the command line. This function
    extracts the name of the file from the command line, returning this name
    as a string.

    Parameters
    ----------

    Returns
    -------
    string
        Name of the file
    """
    filename = sys.argv[1]
    return filename


def import_data(filename):
    """Import data from a given file name

    This function reads in a file name as a parameter and creates a list
    of strings. The strings are first separated by line, and then each string
    is stripped of its '\n' at the end of each string. This allows for
    better/ easier manipulation of the contents of the file.

    Parameters
    ----------
    filename : string
        Name of the desired test file

    Returns
    -------
    list
        List of strings, each one a different line from the file
    """
    contents = list()
    with open(filename, 'r') as input_file:
        file = input_file.readlines()
        for line in file:
            contents.append(line.strip("\n"))
        return contents


def string_split(input_string):
    """Split a string based on the presence of commas

    Each line of the file is read in as a single string, so it is necessary
    to separate this string into two categories: time and voltage. Given that
    the file is comma separated, this function is used to split each string
    into the two categories mentioned above. The input_string will have the
    following format:
    input_string = "0.#####,1.#####"
    Once the string is split, the function returns a list, where the
    first element in the list is the time, and the second element
    in the list is the voltage. This output list has the following format:
    output = ["0.#####". "1.#####"]

    Parameters
    ----------
    input_string : string
        Contains the time and voltage combined as a single string

    Returns
    -------
    list
        List containing two strings
    """
    output = input_string.split(",")
    return output


def str_to_float(input_results):
    """Convert a list of strings into a list of floats

    To actually utilize the time and voltage data points, they both must
    be converted from strings to floats. In order to do this, this function
    reads in a list of two strings, one being the time as a string and the
    other being the voltage as a string. From here, it tries to convert each
    string into the type float. If it is not possible because the string
    contains letters or incorrect punctuation, then the function will log
    the following error: "This line of data is not usable: line skipped".
    It will add any data type (float or string) to the output list,
    so if the input list of two strings contains only one string that could
    be converted to a float, then it will return a list of size two containing
    the float value and a string.

    Parameters
    ----------
    input_results : list
        List containing two strings

    Returns
    -------
    list
        Contains two elements, where each could be a string or a float
    """
    data = list()
    for i in input_results:
        try:
            i = float(i)
        except ValueError:
            logging.error("This line of data is not usable: line skipped")
        data.append(i)
    return data


def float_check(nums):
    """Check to see if input list contains only float values

    Given that the list containing the time and the voltage values could
    contain floats or strings, it is necessary to check to see if the list
    actually is only comprised of floats. Strings are not usable for math
    purposes, so it is necessary to ensure that only floats are present.
    This function reads in a list of two elements, where each could be a
    string or a float. If both of the elements in the list are floats,
    then the function returns True. But, if this is not the case, then the
    function returns False.

    Parameters
    ----------
    nums : list
        Contains two elements, where each could be a string or a float

    Returns
    -------
    bool
        True if successful, False otherwise
    """
    result = all(isinstance(n, float) for n in nums)
    return result


def line_manip(contents):
    """Generate a list of times and a list of voltages

    To properly manipulate the data, it is necessary to separate each list
    of the time and voltage values into two lists, where one list contains
    solely time values and the other list contains solely voltage values.
    This function completes this by running many of the previously defined
    functions. It reads in a list of strings, splits each string into
    two strings, converts the strings into floats, checks to ensure that
    both values are indeed floats, makes sure that the new list actually
    contains two values, and finally checks to see that no NaN values are
    present. Once these conditions have all been satisfied, each value
    is appended to its respective list (time or voltage).

    Parameters
    ----------
    contents : list
        List of strings, each one a different line from the file

    Returns
    -------
    list
        List of floats containing time values
    list
        List of floats containing voltage values
    """
    time = list()
    voltage = list()
    for line in contents:
        line = string_split(line)
        data = str_to_float(line)
        if float_check(data) is False:
            continue
        elif len(data) != 2:
            continue
        elif math.isnan(data[1]) is True or math.isnan(data[0]) is True:
            logging.error("This line of data is not usable: line skipped")
            continue
        else:
            time.append(data[0])
            voltage.append(data[1])
    return time, voltage


def norm_range(voltage):
    """Check to see if the voltage values are within the acceptable normal range

    The normal range for the voltage readings is +/- 300 mV. Within the
    assignment, it was asked that if a voltage reading were found to be outside
    of this range, then add a warning entry to the log file indicating the name
    of the file. This function reads in all of the voltage values and checks to
    see that each one is in fact within the acceptable range. If any of the
    voltage readings are outside of this range, a warning entry is made.

    Parameters
    ----------
    voltage : list
        List of floats containing the voltage values

    Returns
    -------
    bool
        True if successful, False if otherwise
    """
    result = all(elem >= -300.0 and elem <= 300.0 for elem in voltage)
    if result is False:
        logging.warning('The voltage data contains an element outside'
                        ' of the normal range of +/- 300 mV')
    return result


def duration(time):
    """Calculate the duration of the ECG strip

    One of the calculated data was the time duration of the ECG
    strip. To determine this, this function reads in the list of floats
    that make up the time values. The length of the list is determined,
    then the difference between the last time value and the first time value
    is found. This resulting time difference is then returned as a float.

    Parameters
    ----------
    time : list
        List of floats containing the time values

    Returns
    -------
    float
        duration of ECG strip in seconds
    """
    logging.info("Determining duration of the ECG strip")
    length_list = len(time)
    answer = time[length_list-1] - time[0]
    return answer


def voltage_ex(voltage):
    """Determine the minimum and maximum voltages within the voltage data

    Another of the calculated data were the minimum and maximum voltage
    values within the list of voltages. This function reads in the list of
    voltage values and determines the minimum and maximum voltages using the
    min() and max() functions of Python. Once these values are determined,
    they are placed into a tuple in the form (min, max), which is then
    returned.

    Parameters
    ----------
    voltage : list
        List of floats containing the voltage values

    Returns
    -------
    tuple
        Contains the minimum and maximum voltages from the ECG strip
    """
    logging.info("Determining the voltage extremes")
    max_vol = max(voltage)
    min_vol = min(voltage)
    extremes = (min_vol, max_vol)
    return extremes


def counting_peaks(voltage):
    """Count the total number of peaks in the file

    Another of the calculated data was the number of detected beats in the
    strip. To determine this, the scipy package must be installed, and from
    this package import the package "find_peaks". This package is able to
    find the peaks of an incoming signal. This function utilizes this
    package to create a list of integers containing the indices of all
    of the peaks within the voltage list. The voltage list is inputted,
    then using this package, the length of the resulting list is found.
    This length is equivalent to the number of peaks present, so this
    value is returned.

    Parameters
    ----------
    voltage : list
        List of floats containing the voltage values

    Returns
    -------
    int
        Value containing the number of peaks present
    """
    logging.info("Determining the number of beats in the ECG strip")
    peaks, _ = find_peaks(voltage, distance=190)
    count = len(peaks)
    return count


def heart_rate(length_of_strip, count):
    """Determine the average heart rate from the ECG strip

    Another of the calculated data was the estimated average heart rate
    over the length of the ECG strip. To determine this, two values are
    necessary, the duration of the ECG strip and the number of peaks present.
    With these two values, the following formula was utilized to calculate
    the estimated average heart rate:
    Heart Rate = (# beats / duration of ECG strip) * (60 seconds / minute)
    With this formula, the average heart rate is found and returned by
    this function.

    Parameters
    ----------
    length_of_strip : float
        Contains duration of ECG strip in seconds
    count : int
        Value containing the number of peaks present

    Returns
    -------
    float
        Contains the average heart rate (beats per minute)
    """
    logging.info("Determining the estimated average heart rate")
    mean_hr = count/length_of_strip * 60     # 60 sec / min
    return mean_hr


def beats(time, voltage):
    """Determine the list of times when a beat occurred

    Another of the calculated data was the list of times when a beat actually
    occurred. This function takes in two lists as parameters, the time list
    and the voltage list. For this function the "find_peaks" package from scipy
    is necessary. This package is used to generate a list of the indices at
    which peak voltages are found. Using this list of indices, instead apply
    it to the time list. By determining the indices at which the voltage peaks
    are, we also know the times at which these voltage peaks occurred. By
    using a for loop to generate a list containing only the times with the
    specified indices, a list of floats containing specific times at which
    peaks occurred is generated and returned.

    Parameters
    ----------
    time : list
        List of floats containing time values
    voltage : list
        List of floats containing time values

    Returns
    -------
    list
        Contains floats that match the times at which peaks occurred
    """
    logging.info("Determining the time stamps for each beat")
    list_of_times = list()
    peaks, _ = find_peaks(voltage, distance=190)
    for peak in peaks:
        list_of_times.append(time[peak])
    return list_of_times


def metrics(time_dur, extremes, count, mean_hr, list_of_times):
    """Create a dictionary with the specified metrics

    Once all of the metrics have been determined, it is necessary to compile
    them all together. This is done through the generation of a dictionary.
    In the assignment, it is specified that the dictionary should contain
    the following information:
        duration: time duration of the ECG strip
        voltage_extremes: tuple in the form (min, max) where min and max are
            the minimum and maximum lead voltages found in the data file.
        num_beats: number of detected beats in the strip, as a numeric
            variable type.
        mean_hr_bpm: estimated average heart rate over the length of the strip
        beats: list of times when a beat occurred
    This function reads in each of these metrics and places each one into their
    respective keys as mentioned above. Then, once all of the information
    has been added to the dictionary, it is returned.


    Parameters
    ----------
    time_dur : float
        Contains duration of ECG strip in seconds
    extremes : tuple
        Contains the minimum and maximum voltages from the ECG strip
    count : int
        Value containing the number of peaks present
    mean_hr : float
        Contains the average heart rate (beats per minute)
    list_of_times : list
        Contains floats that match the times at which peaks occurred

    Returns
    -------
    dictionary
        Contains all of the metrics necessary
    """
    logging.info("Dictionary being established")
    metrics_dict = {"duration": time_dur,
                    "voltage_extremes": extremes,
                    "num_beats": count,
                    "mean_hr_bpm": mean_hr,
                    "beats": list_of_times}
    logging.info("Dictionary filled")
    return metrics_dict


def json_output(metrics_dict):
    """Output a JSON file of the metrics dictionary

    Once all of the metrics have been compiled into a dictionary, it is
    necessary to put this dictionary into a JSON file that can be accessed
    by the user. This function reads in the metrics dictionary, opens a JSON
    file named after the input test file, fills the file with the dictionary
    containing all of the metrics, then closes the file, generating it in
    the process.

    Parameters
    ----------
    metrics_dict : dictionary
        Contains all of the metrics separated into keys

    Returns
    -------
    N/A
    """
    filename = import_name().split(".")[0] + '.json'
    out_file = open(filename, "w")
    json.dump(metrics_dict, out_file)
    out_file.close()


if __name__ == '__main__':
    logging.basicConfig(filename="my_code.log", filemode='w',
                        level=logging.DEBUG)
    logging.info("--------New Run--------\n")
    filename = import_name()
    contents = import_data(filename)
    time, voltage = line_manip(contents)
    norm_range(voltage)
    time_dur = duration(time)
    extremes = voltage_ex(voltage)
    count = counting_peaks(voltage)
    mean_hr = heart_rate(time_dur, count)
    list_of_times = beats(time, voltage)
    metrics_dict = metrics(time_dur, extremes, count, mean_hr, list_of_times)
    json_output(metrics_dict)
    logging.info("********End of Run********\n")
