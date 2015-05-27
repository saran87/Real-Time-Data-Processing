import logging
import numpy as np
from paktrack.common.common import (get_psd,get_grms)

class ConsolidatedReport(object):
	"""docstring for ClassName"""
	def __init__(self, vibration):
		self.vibration = vibration
		self.logger = logging.getLogger(__name__)

	def process_psd(self, events, axis):
		psds = []
		self.logger.info("Started Processing PSD's for %s axis",axis)
		for event in events:
			psds.append(get_psd(event[axis]))
		self.logger.info("Done Processing PSD's for %s axis",axis)
		return psds

	def consolidate_psd(self,psds):
			dArray = np.array(psds)
			vibrationTable = []
			self.logger.info("Started consolidating psd's")
			size = len(psds[0])
			for i in xrange(0,size):
				vibrationTable.append(np.sum(dArray[:,i])/len(psds))
			self.logger.info("Done consolidating psd's")		
			return vibrationTable

	def process_data(self,truck_id,package_id):

		self.logger.info("Started Processing data for truck_id: %s & package_id: %s",truck_id,package_id)
		
		events = self.vibration.get_events(truck_id,package_id)
		self.logger.info("Loaded %d events",len(events))
		
		if(len(events) > 0):
			table = {}
			table['no_of_events'] = len(events)

			table['x'] = self.consolidate_psd(self.process_psd(events,'x'))
			table['x_grms'] = get_grms(table['x'])

			table['y'] = self.consolidate_psd(self.process_psd(events,'y'))
			table['y_grms'] = get_grms(table['y'])

			table['z'] = self.consolidate_psd(self.process_psd(events,'z'))
			table['z_grms'] = get_grms(table['z'])

			table['vector'] = self.consolidate_psd(self.process_psd(events,'vector'))
			table['vector_grms'] = get_grms(table['vector'])

			self.vibration.update_consolidated_report(truck_id,package_id,table)

		return "success"


		
		