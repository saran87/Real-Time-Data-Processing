import logging
from paktrack.common.common import (
    get_psd, get_grms, get_max_with_index, get_normalized_rms)


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
            if self.__is_proper_event(event):
                result = self.vibration.delete(event)
                print result
            else:
                event = self.__process_psd(event)
                event['g_rms'] = get_normalized_rms(event)
                event['is_processed'] = True
                result = self.vibration.update(event)

        return result

    def __process_max_value(self, event):
        event['max_x'] = get_max_with_index(event['x'])
        event['max_y'] = get_max_with_index(event['y'])
        event['max_z'] = get_max_with_index(event['z'])
        event['max_vector'] = get_max_with_index(event['vector'])

        return event

    def __is_proper_event(self, event):
        count = 0
        if abs(event['max_x']['value']) >= 4.0:
            count = count + 1

        if abs(event['max_y']['value']) >= 4.0:
            count = count + 1

        if abs(event['max_z']['value']) >= 4.0:
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
