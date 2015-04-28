from vibration import Vibration

vibration = Vibration();
table = vibration.process_data("TRIP 1","1")
print table['x']