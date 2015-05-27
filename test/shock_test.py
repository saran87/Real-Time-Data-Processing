import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from paktrack.shock import shock, shock_data_processor

def test_shock_preprocessing():
	shock_model = shock.Shock("test.pak-track.com",27017,"paktrackDB")
	data_processor = shock_data_processor.ShockDataProcessor(shock_model)
	result = data_processor.pre_process_data("53a882d513a850347fcc1a55")
	print  "Passed preprocessing data" if result is "53a8838f13a850347fcc1a57"  else "Failed preprocessing shock data"


if __name__ == "__main__":
    test_shock_preprocessing()

