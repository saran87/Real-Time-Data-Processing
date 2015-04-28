import json
import math
import numpy as np
import logging
from pymongo import MongoClient
from scipy.integrate import simps, trapz

class Vibration():
	FREQUENCY  = 1600
	def __init__(self, db_host, db_port, db):
		self.db_client = MongoClient(db_host, db_port)
		self.db = self.db_client[db]
		# create logger
		self.logger = logging.getLogger(__name__)

	def get_cursor(self,truck_id, package_id, is_above_threshold = True):

		vib_collection = self.db["vibration"]

		vib_cursor = vib_collection.find({"truck_id":truck_id,"package_id":package_id,"is_above_threshold": is_above_threshold})

		return vib_cursor

	def splitAndConvert(self,value,splitter = ' '):
		return map(float,value.split(splitter))

	def get_vector_data(self,x,y,z):
		size = len(x)
		return [ math.sqrt((x[i]*x[i])+(y[i]*y[i])+(z[i]*z[i]))  for i in xrange(0,size)]


	def loadEvents(self,truck_id, package_id, is_above_threshold = True):
		events = []
		vib_cursor = self.get_cursor(truck_id,package_id,is_above_threshold)
		self.logger.info("Started loading vibration events from mongodb cursor")
		for line in vib_cursor:
			event = line
			event['x'] =  self.splitAndConvert(event['value']['x']);
			event['y'] =  self.splitAndConvert(event['value']['y']);
			event['z'] =  self.splitAndConvert(event['value']['z']);
			event['vector'] = self.get_vector_data(event['x'],event['y'],event['z'])
			del event['value'];
			events.append(event)
		self.logger.info("Done loading vibration events from mongodb cursor")
		return events


	def processPSD(self, events, axis):
		psds = []
		self.logger.info("Started Processing PSD's for %s axis",axis)
		for event in events:
			signal = np.array(event[axis], dtype=float)
			size = len(event[axis])
			fourier = np.fft.fft(signal*np.hanning(size))
			psd = 2 * ((fourier.real * fourier.real)/(self.FREQUENCY*size)) 
			psds.append(psd)
		self.logger.info("Done Processing PSD's for %s axis",axis)
		return psds


	def consolidatePSD(self,psds):
			dArray = np.array(psds)
			vibrationTable = []
			self.logger.info("Started consolidating psd's")
			size = len(psds[0])
			for i in xrange(0,size):
				vibrationTable.append(np.sum(dArray[:,i])/len(psds))
			self.logger.info("Done consolidating psd's")		
			return vibrationTable

	def get_grms(self,data):
		graph = data[2:len(data)/2-1]
		return simps(graph, dx=5)

	def update_database(self,truck_id,package_id,table):
		table['truck_id'] = truck_id
		table['package_id'] = package_id
		self.logger.info("Started udpating data base with vibration report of truck_id: %s & package_id: %s",truck_id,package_id)
		report_collection = self.db["vibration_reports"]
		write_result = report_collection.insert(table)
		self.logger.info("Done udpating data base with vibration report of truck_id: %s & package_id: %s",truck_id,package_id)

	def process_data(self,truck_id,package_id):

		self.logger.info("Started Processing data for truck_id: %s & package_id: %s",truck_id,package_id)
		
		events = self.loadEvents(truck_id,package_id)
		self.logger.info("Loaded %d events",len(events))
		
		if(len(events) > 0):
			table = {}
			table['no_of_events'] = len(events)

			table['x'] = self.consolidatePSD(self.processPSD(events,'x'))
			table['x_grms'] = self.get_grms(table['x'])

			table['y'] = self.consolidatePSD(self.processPSD(events,'y'))
			table['y_grms'] = self.get_grms(table['y'])

			table['z'] = self.consolidatePSD(self.processPSD(events,'z'))
			table['z_grms'] = self.get_grms(table['z'])

			table['vector'] = self.consolidatePSD(self.processPSD(events,'vector'))
			table['vector_grms'] = self.get_grms(table['vector'])

			self.update_database(truck_id,package_id,table)

		return "success"


		