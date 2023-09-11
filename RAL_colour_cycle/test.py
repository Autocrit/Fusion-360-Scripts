import json, os

def count_ral_colours():
	filename = "~/Documents/GitHub/Fusion-360-Scripts/RAL_colour_cycle/RAL_classic.json"
	filename = os.path.expanduser(filename)
	with open(filename, "r") as read_file:
		ral_colours = json.load(read_file)

		return len(ral_colours)
	
	return -1
	
print(count_ral_colours())