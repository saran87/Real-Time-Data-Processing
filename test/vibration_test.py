import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from paktrack.vibration import vibration,consolidated_report,vibration_data_processor

vib = vibration.Vibration("test.pak-track.com",27017,"paktrackDB")

def test_vibration_object():	
	events = vib.get_events("INTERNATIONAL","WUXI")
	print  "Passed" if len(events) > 0 else "Failed"
	event =  vib.get_event("53a8841d13a850347fcc1a5a")
	print  "Passed" if event  else "Failed"

def test_consolidated_report():
	report = consolidated_report.ConsolidatedReport(vib)
	result = report.process_data("TRIP 1","1")
	print  "Passed consolidated_report" if result is "success"  else "Failed consolidated_report"

def test_vibration_preprocessing():
	data_processor = vibration_data_processor.VibrationDataProcessor(vib)
	result = data_processor.pre_process_data("53a8841d13a850347fcc1a5a")
	#print result
	print  "Passed preprocessing data" if result is "5553e84c43e88deae72988d6"  else "Failed preprocessing vibration data"


if __name__ == "__main__":
    #test_vibration_object()

    #test_consolidated_report()
    
    test_vibration_preprocessing()




