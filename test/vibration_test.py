
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from paktrack.vibration import (
    vibration, consolidated_report, vibration_data_processor)
import time
start_time = time.time()
HOST = "database.pak-track.com"
PORT = 27017
DB = "realTimeDataDb"


def test_vibration_object():
    vib = vibration.Vibration(HOST, PORT, DB)

    events = vib.get_events("INTERNATIONAL", "WUXI")
    print "Passed" if len(events) > 0 else "Failed"
    event = vib.get_event("53a8841d13a850347fcc1a5a")
    print "Passed" if event else "Failed"


def test_consolidated_report():
    vib = vibration.Vibration(HOST, PORT, DB)
    report = consolidated_report.ConsolidatedReport(vib)
    result = report.process_data("NEW TEST1", "001")
    if result is "success":
        print "Passed consolidated_report"
    else:
        print "Failed consolidated_report"
    print("--- %s seconds ---" % (time.time() - start_time))


def test_custom_report():
    vib = vibration.Vibration(HOST, PORT, DB)
    report = consolidated_report.ConsolidatedReport(vib)
    result = report.gen_custom_report("NEW TEST1", "001", ["5579cd1343e88deae72992e0",
        "5579cd1343e88deae72992e1"])
    if result is "success":
        print "Passed consolidated_report"
    else:
        print "Failed consolidated_report"
    print("--- %s seconds ---" % (time.time() - start_time))


def test_vibration_preprocessing():
    vib = vibration.Vibration(HOST, PORT, DB)
    data_processor = vibration_data_processor.VibrationDataProcessor(vib)
    result = data_processor.pre_process_data("559da4b843e88deae7299790")
    print result
    if result:
        print "Passed preprocessing data"
    else:
        print "Failed preprocessing vibration data"


if __name__ == "__main__":
    # test_vibration_object()

    test_consolidated_report()
    test_custom_report()
    # test_vibration_preprocessing()
