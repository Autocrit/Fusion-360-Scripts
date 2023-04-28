#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import json

#e.g.
#[
#	{
#		"config": "XS",
#		"active": true,
#		"params": [
#			{ "name": "seat_tube_length", "value": 410, "units": "mm" },
#			{ "name": "head_tube_angle", "value": 70, "units": "deg" },
#			{ "name": "seat_tube_angle", "value": 73.1, "units": "deg" },
#			{ "name": "head_tube_length", "value": 89, "units": "mm" },
#			{ "name": "wheelbase", "value": 1011, "units": "mm" },
#			{ "name": "chain_stay_length", "value": 430, "units": "mm" },
#			{ "name": "bottom_bracket_drop", "value": 75, "units": "mm" },
#			{ "name": "bottom_bracket_height", "value": 284, "units": "mm" },
#			{ "name": "fork_offset", "value": 55, "units": "mm" }
#		]
#	}
#]

def loadConfigParams(ui):
	fileDlg = ui.createFileDialog()
	fileDlg.isMultiSelectEnabled = False
	fileDlg.title = 'Fusion Open File Dialog'
	fileDlg.filter = '*.json'
	dlgResult = fileDlg.showOpen()
	
	if dlgResult == adsk.core.DialogResults.DialogOK:
		with open(fileDlg.filename, "r") as read_file:
			return json.load(read_file)

	return None

def getValueExpression(value, units):
	return str(value) + " " + units

def setActiveConfigParams(userParams, configParams):
	for config in configParams:
		if config.get("active", False) == True:
			for param in config["params"]:
				userParam = userParams.itemByName(param["name"])
				if userParam:
					userParam.expression = getValueExpression(param["value"], param["units"])
				else:
					userParams.add(param["name"], adsk.core.ValueInput.createByString(getValueExpression(param["value"], param["units"])), param["units"], "")
					
def run(context):
	ui = None
	try:
		app = adsk.core.Application.get()

		ui  = app.userInterface
		design = app.activeProduct
		userParams = design.userParameters

		configParams = loadConfigParams(ui)
		if configParams:
			setActiveConfigParams(userParams, configParams)
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
