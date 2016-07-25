import logging
from paktrack.common.common import (
    get_psd, get_grms, get_max_with_index, get_normalized_rms,
    get_average_for_event, get_rms_for_event)
import numpy as np
from scipy.stats import kurtosis


class VibrationDataProcessor(object):
    """docstring for VibrationDataProcessor"""
    def __init__(self, vibration):
        self.vibration = vibration
        self.logger = logging.getLogger(__name__)

    def pre_process_data(self, id):
        event = self.vibration.get_event(id)
        result = "no_event"

        if event:
            event = self.__process_max_value(event)
            if self.__is_not_proper_event(event):
                result = self.vibration.delete(event)
            else:
                event = self.__process_psd(event)
                # event['average'] = get_average_for_event(event)
                event['rms'] = self.__get_rms(event) #get_rms_for_event(event)
                event['is_processed'] = True
                event['kurtosis'] = self.__get_kurtosis(event)
                result = self.vibration.update(event)

        return result

    def __process_max_value(self, event):
        event['max_x'] = get_max_with_index(event['x'])
        event['max_y'] = get_max_with_index(event['y'])
        event['max_z'] = get_max_with_index(event['z'])
        event['max_vector'] = get_max_with_index(event['vector'])

        return event

    def __is_not_proper_event(self, event):
        ''' Remove vibration event greater than or equal to 4.0 G, also vibration event equal to 3.9687.
         Prof. Changfeng => 3.9687 appear to be shock data)'''
        count = 0
        if (abs(event['max_x']['value']) >= 4.0 or abs(event['max_x']['value']) == 3.9687) :
            count = count + 1

        if (abs(event['max_y']['value']) >= 4.0 or abs(event['max_y']['value']) == 3.9687):
            count = count + 1

        if (abs(event['max_z']['value']) >= 4.0 or abs(event['max_y']['value']) == 3.9687):
            count = count + 1

        if count > 1:
            return True

        return False

    def __process_psd(self, event):
        event['psd_x'] = get_psd(event['x'])
        event['psd_y'] = get_psd(event['y'])
        event['psd_z'] = get_psd(event['z'])
        event['psd_vector'] = get_psd(event['vector'])

        event['x_grms'] = get_grms(event['psd_x'])
        event['y_grms'] = get_grms(event['psd_y'])
        event['z_grms'] = get_grms(event['psd_z'])
        event['vector_grms'] = get_grms(event['psd_vector'])

        return event
    
    def __get_rms(self, event):
        '''Get the RMS per axis for a given vibration event'''
        rms = {}
        rms['x'] = self.__calculate_rms(event['x'])
        rms['y'] = self.__calculate_rms(event['y'])
        rms['z'] = self.__calculate_rms(event['z'])
        return rms

    def __calculate_rms(self, signal):
        '''Calculate the RMS for a given signal'''
        signal = np.array(signal)
        return np.sqrt(np.mean(np.square(signal)))

    def __get_kurtosis(self, event):
        '''Get the kurtosis for each axis'''
        kt = {}
        kt['x'] = kurtosis(event['x'], fisher=False)
        kt['y'] = kurtosis(event['y'], fisher=False)
        kt['z'] = kurtosis(event['z'], fisher=False)
        return kt