import json

with open("cannondale_topstone_1.json", "r") as read_file:
	configs = json.load(read_file)

	data = []
	for config in configs:
		dataConfig = {}
		dataConfig["config"] = config["config"]
		dataParams = []
		for key in config:
			if key != "config" and key != "active":
				dataParam = {}
				part = config[key].split(" ")
				value = float(part[0])
				units = part[1]
				dataParam["name"] = key
				dataParam["value"] = value
				dataParam["units"] = units
				dataParams.append(dataParam)
		dataConfig["params"] = dataParams

		data.append(dataConfig)

	print(json.dumps(data))

	with open("cannondale_topstone_1_reformat.json", "w") as outfile:
		outfile.write(json.dumps(data))