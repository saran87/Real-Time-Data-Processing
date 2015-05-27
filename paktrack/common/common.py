import sys
import math
import numpy as np
from numpy import mean, sqrt, square
from scipy.integrate import simps
# Frequency of vibration & shock signals
FREQUENCY  = 1600

def get_grms(data):
	return simps(data[2:(len(data)/2)-1], dx=10)

def get_axis_data(event):
	if event:
		if 'value' in event: #To handle old data format
			event['x'] =  string_to_list(event['value']['x']);
			event['y'] =  string_to_list(event['value']['y']);
			event['z'] =  string_to_list(event['value']['z']);
			del event['value'];
			
		if 'x' in event:
			if not isinstance(event['x'], list):
				event['x'] =  string_to_list(event['x']);
		if 'y' in event:
			if not isinstance(event['x'], list):
				event['x'] =  string_to_list(event['x']);
		if 'z' in event:
			if not isinstance(event['x'], list):
				event['x'] =  string_to_list(event['z']);

		event['vector'] = get_vector_data(event['x'],event['y'],event['z'])
		
	return event

def get_psd(signal):
	size = len(signal)
	signal = np.array(signal, dtype=float)
	fourier = np.fft.fft(signal*np.hanning(size))
	psd = (fourier.real  ** 2)/(FREQUENCY*size) 
	psd  = np.array(psd, dtype=float)
	psd[2:size-1] =  2 * psd[2:size-1]
	return psd.tolist()

def get_max_with_index(signal):
	max_index = np.argmax(np.absolute(signal))
	return {"value": signal[max_index],"index":max_index} 

def string_to_list(value,splitter = ' '):
		return map(float,value.split(splitter))

def get_vector_data(x,y,z):
	size = len(x)
	return [ math.sqrt((x[i]*x[i])+(y[i]*y[i])+(z[i]*z[i]))  for i in xrange(0,size)]

def get_normalized_rms(event):
	x = normalized_singal(event['x'])
	y = normalized_singal(event['y'])
	z = normalized_singal(event['z'])
	vector = get_vector_data(x,y,z)
	return sqrt(mean(square(vector)))


def normalized_singal(signal):
	signal = np.array(signal)
	theta = np.average(signal)
	signal = signal - theta
	return signal