
from paktrack.common.base_model import BaseModel

VIBRATION_COLLECTION = "vibration"
VIBRATION_REPORT_COLLECTION = "vibration_reports"

class Vibration(BaseModel):

	def __init__(self, db_host, db_port, db, db_user = "", db_pass = ""):
		super(Vibration, self).__init__(db_host, db_port, db, db_user, db_pass,VIBRATION_COLLECTION)

	def update_consolidated_report(self,truck_id,package_id,table):
		self.logger.info("Started udpating data base with vibration report of truck_id: %s & package_id: %s",truck_id,package_id)
		
		table['truck_id'] = truck_id
		table['package_id'] = package_id
		report_collection = self.db[VIBRATION_REPORT_COLLECTION]
		write_result = report_collection.insert(table)
		
		self.logger.info("Done udpating data base with vibration report of truck_id: %s & package_id: %s",truck_id,package_id)

	
