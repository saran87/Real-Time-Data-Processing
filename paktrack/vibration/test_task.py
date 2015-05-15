from vibration import Vibration

vibration = Vibration("database.pak-track.com",27017,"realTimeDataDb");
table = vibration.process_data("INTERNATIONAL","WUXI")
print table