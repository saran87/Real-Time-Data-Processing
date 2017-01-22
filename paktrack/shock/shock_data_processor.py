import logging
import operator
from numpy import mean, sqrt, square

from paktrack.common.common import (get_average_for_event)
from paktrack.shock.shock_response_spectrum import srs, np

PEEK_DETECTION_THRESHOLD = 3
FACE_DETECTION_THRESHOLD = 1.5
NUMBER_CHUNK_SIZE = 16
AXIS_MAPPING = {0: "x", 1: "y", 2: "z"}


class ShockDataProcessor(object):
    """docstring for ShockDataProcessor"""

    def __init__(self, shock):
        self.shock = shock
        self.logger = logging.getLogger(__name__)

    def pre_process_data(self, id):

        event = self.shock.get_event(id)
        result = "no event"

        if event:
            event = self.__process_max_value(event)
            event['average'] = get_average_for_event(event)
            event['drop_height'] = self.__get_drop_height(event)
            event['orientation'] = self.__get_drop_orientation(event)
            event['g_rms'] = self.__get_grms(event)  # get_normalized_rms(event)
            event['srs'] = self.get_srs(event)
            event['is_processed'] = True
            result = self.shock.update(event)

        return result

    def __process_max_value(self, event):

        chunk_index = self.__get_peak_chunk_index(event['vector'])

        event['max_x'] = self.__get_max_with_index(event['x'], chunk_index)
        event['max_y'] = self.__get_max_with_index(event['y'], chunk_index)
        event['max_z'] = self.__get_max_with_index(event['z'], chunk_index)
        event['max_vector'] = self.__get_max_with_index(
            event['vector'], chunk_index)

        return event

    def __get_peak_chunk_index(self, signal):

        chunks = np.array_split(signal, NUMBER_CHUNK_SIZE)
        max_value = -0.0
        chunk_index = -1
        chunk_count = 0

        for chunk in chunks:
            max_index = np.argmax(np.absolute(chunk))
            if abs(chunk[max_index]) > abs(max_value):
                if (abs(chunk[max_index]) - abs(max_value)) > PEEK_DETECTION_THRESHOLD:
                    max_value = chunk[max_index]
                    chunk_index = chunk_count
            chunk_count += 1

        return chunk_index

    def __get_max_with_index(self, signal, chunk_index):

        chunks = np.array_split(signal, NUMBER_CHUNK_SIZE)
        max_index = np.argmax(np.absolute(chunks[chunk_index]))
        chunk_size = len(signal) / NUMBER_CHUNK_SIZE
        index = (chunk_index * chunk_size) + max_index

        return {'value': chunks[chunk_index][max_index], 'index': index}

    def __normalized_singal(self, signal):

        signal = np.array(signal)
        theta = np.average(signal)
        signal = signal - theta

        return signal

    def __get_drop_height(self, event):
        """

        :param event:
        :return:
        """
        """add 1 for getting correct milliseconds, since array index starts"""
        max_index = event['max_vector']['index'] + 1
        t = (max_index * 0.000625) + (70.0 / 1000.0)
        height = 4.9 * (t ** 2)
        return height

    def __get_drop_orientation(self, event):
        max_axis_values = {'max_x': abs(event['max_x']['value']), 'max_y': abs(event['max_y']['value']),
                           'max_z': abs(event['max_z']['value'])}
        max_axis_values = sorted(max_axis_values.items(), key=operator.itemgetter(1), reverse=True)
        faces = []

        key, value = max_axis_values[0]
        faces.append(self.__get_face(key, event[key]['value']))
        max_value = value
        del max_axis_values[0]

        for key, value in max_axis_values:
            ratio = max(max_value, value) / min(max_value, value) if min(max_value, value) > 0.0 else max(max_value,
                                                                                                          value)
            if abs(ratio) <= FACE_DETECTION_THRESHOLD:
                faces.append(self.__get_face(key, event[key]['value']))

        return faces

    def __get_face(self, axis, value):
        is_negative = False if value >= 0 else True

        if axis is "max_y":
            return 6 if is_negative else 5

        elif axis is "max_x":
            return 4 if is_negative else 2

        elif axis is "max_z":
            return 1 if is_negative else 3

    def __get_grms(self, event):
        """ Calculate the mean root square of the maximum values for each axis
        :param event:
        :return: grms
        """
        x = event['max_x']['value']
        y = event['max_y']['value']
        z = event['max_z']['value']
        return sqrt(mean([square(x), square(y), square(z)]))

    def get_srs(self, event):

        return {'x': srs(event['x']),
                'y': srs(event['y']),
                'z': srs(event['z']),
                'vector': srs(event['vector'])}
