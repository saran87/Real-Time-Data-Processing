import logging
import numpy as np
from bson import ObjectId
from paktrack.common.common import (get_psd, get_grms)


class ConsolidatedReport():
    """docstring for ClassName"""
    def __init__(self, vibration):
        self.vibration = vibration
        self.logger = logging.getLogger(__name__)

    def process_psd(self, events, axis):
        psds = []
        self.logger.info("Started Processing PSD's for %s axis", axis)
        for event in events:
            key = 'psd_' + axis
            if key in event:
                psds.append(event[key])
            else:
                psds.append(get_psd(event[axis]))
        self.logger.info("Done Processing PSD's for %s axis", axis)
        return psds

    def consolidate_psd(self, psds):
            d_array = np.array(psds)
            vibration_table = []
            self.logger.info("Started consolidating psd's")
            size = len(psds[0])
            for i in xrange(0, size):
                vibration_table.append(np.sum(d_array[:, i]) / len(psds))
            self.logger.info("Done consolidating psd's")
            return vibration_table

    def generate_report(self, truck_id, package_id, events):
        if(len(events) > 0):
            table = {}
            table['no_of_events'] = len(events)

            table['x'] = self.consolidate_psd(self.process_psd(events, 'x'))
            table['x_grms'] = get_grms(table['x'])

            table['y'] = self.consolidate_psd(self.process_psd(events, 'y'))
            table['y_grms'] = get_grms(table['y'])

            table['z'] = self.consolidate_psd(self.process_psd(events, 'z'))
            table['z_grms'] = get_grms(table['z'])

            table['vector'] = self.consolidate_psd(
                self.process_psd(events, 'vector'))
            table['vector_grms'] = get_grms(table['vector'])

            self.vibration.update_consolidated_report(
                truck_id, package_id, table)

        return "success"

    def process_data(self, truck_id, package_id):

        self.logger.info(
            "Started Processing data for truck_id: %s & package_id: %s",
            truck_id, package_id)

        events = self.vibration.get_events(truck_id, package_id)

        self.logger.info("Loaded %d events", len(events))

        return self.generate_report(truck_id, package_id, events)

    def gen_custom_report(self, truck_id, package_id, ids):

        self.logger.info("Started Processing for custom report")

        event_ids = []
        for id in ids:
            event_ids.append(ObjectId(str(id)))

        query = {"_id": {"$in": event_ids}}

        vib_cursor = self.vibration.get_cursor(query)
        events = []
        for event in vib_cursor:
            events.append(event)

        self.logger.info("Loaded %d events", len(events))

        return self.generate_report(truck_id, package_id, events)
