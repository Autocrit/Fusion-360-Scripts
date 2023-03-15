# This script drives the first sketch in the root component
# Sketch must have just one driven dimension; this is the shock travel
# Wheel travel dimension = 'wheel_travel' user parameter

import adsk.core, adsk.fusion, adsk.cam, traceback

travel_param_name = 'travel_percent'

def run(context):
	ui = None
	try:
		app = adsk.core.Application.get()
		ui  = app.userInterface

		design = app.activeProduct
		root = design.rootComponent
		sketch = root.sketches.item(1)

		# Find first driven dimension
		for dim in sketch.sketchDimensions:
			if not dim.isDriving:
				break

		output = open('~/Documents/leverage_ratio.csv', 'w')
		#output = open('c:/temp/leverage_ratio.csv', 'w')

		travelPercentParam = design.userParameters.itemByName('travel_percent')
		shockTravelParam = design.userParameters.itemByName('shock_travel')
		travelPercent = 1
		
		output.write('Wheel travel,Shock travel\n')

		while (travelPercent <= 100):
			#travelPercentParam.expression = str(travelPercent)
			travelPercentParam.value = travelPercent
			p1 = dim.entityOne.geometry
			p2 = dim.entityTwo.geometry
			distance = p1.distanceTo(p2)
			distance = float(design.unitsManager.formatInternalValue(distance, design.unitsManager.defaultLengthUnits, False))
			#output.write('{:.4f},{:.4f}\n'.format(distance, shockTravelParam.expression))
			output.write(str(distance) + ',' + str(shockTravelParam.value) + '\n')
			travelPercent += 1

		output.close()

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))