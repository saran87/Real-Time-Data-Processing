import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from paktrack.shock import shock, shock_data_processor

def test_shock_preprocessing():
	shock_model = shock.Shock("test.pak-track.com",27017,"paktrackDB")
	data_processor = shock_data_processor.ShockDataProcessor(shock_model)
	result = data_processor.pre_process_data("5588afb88ae5a45f6f2e8097")
	print result
	print  "Passed preprocessing data" if result   else "Failed preprocessing shock data"


if __name__ == "__main__":
    test_shock_preprocessing()

