import math
import numpy as np
from numpy import mean, sqrt, square
from scipy.integrate import simps
# Frequency of vibration & shock signals
FREQUENCY = 1600
DX = 5


def get_grms(data):
    area = simps(data[2:(len(data) / 2) - 1], dx=DX)
    # added as per prof.Changfeng Ge suggestion
    return math.sqrt(area)


def get_axis_data(event):
    ''' dont change the below code without proper impact analysis
        this code handles the old data format and new data format of
        vibration and shock data
    '''

    if event:
        if 'value' in event:  # To handle old data format
            event['x'] = string_to_list(event['value']['x'])
            event['y'] = string_to_list(event['value']['y'])
            event['z'] = string_to_list(event['value']['z'])
            del event['value']

        if 'x' in event:
            if not isinstance(event['x'], list):
                event['x'] = string_to_list(event['x'])
        if 'y' in event:
            if not isinstance(event['y'], list):
                event['y'] = string_to_list(event['y'])
        if 'z' in event:
            if not isinstance(event['z'], list):
                event['z'] = string_to_list(event['z'])

        event['vector'] = get_vector_data(event['x'], event['y'], event['z'])

    return event


def get_psd(signal):
    size = len(signal)
    signal = np.array(signal, dtype=float)
    fourier = np.fft.fft(signal * np.hanning(size))
    psd = (fourier.real ** 2) / (FREQUENCY * size)
    psd = np.array(psd, dtype=float)
    psd[2:size - 1] = 2 * psd[2:size - 1]
    return psd.tolist()


def get_max_with_index(signal):
    max_index = np.argmax(np.absolute(signal))
    return {"value": signal[max_index], "index": max_index}


def string_to_list(value, splitter=' '):
        return map(float, value.split(splitter))


def get_vector_data(x, y, z):
    size = len(x)
    return [math.sqrt((x[i] * x[i]) + (y[i] * y[i]) + (z[i] * z[i]))
            for i in xrange(0, size)]


def get_normalized_rms(event):
    x = normalized_singal(event['x'])
    y = normalized_singal(event['y'])
    z = normalized_singal(event['z'])
    vector = get_vector_data(x, y, z)
    return sqrt(mean(square(vector)))


def normalized_singal(signal):
    signal = np.array(signal)
    theta = np.average(signal)
    signal = signal - theta
    return signal

 
def get_average(signal):
    signal = np.array(signal)
    average = np.average(signal)
    return average


def get_average_for_event(event):
    average = {}
    average['x'] = get_average(event['x'])
    average['y'] = get_average(event['y'])
    average['z'] = get_average(event['z'])
    average['vector'] = get_average(event['vector'])

    return average

def get_rms_for_event(event):
    '''Calculate the RMS for a given vibration event'''
    rms = {}
    rms['x'] = get_rms(event['x'])
    rms['y'] = get_rms(event['y'])
    rms['z'] = get_rms(event['z'])
    return rms

def get_rms(signal):
    '''Calculate the RMS for a given signal'''
    signal = np.array(signal)
    return sqrt(mean(square(a)))


    
