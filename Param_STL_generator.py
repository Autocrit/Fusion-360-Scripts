# Generate STL files by modifying a parameter

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
	ui = None
	try:
		paramName = 'spacer_thickness'
		folder = '/Users/tom/Documents/Temp'
		file = 'mid_spacer_'

		start = 0.5
		end = 3.01
		step = 0.1

		app = adsk.core.Application.get()
		ui  = app.userInterface
		design = app.activeProduct
		param = design.userParameters.itemByName(paramName)

		reset_value = param.expression
        
		value = start
		while (value <= end):
			valueStr = "{:.1f}".format(value)
			param.expression = valueStr

			exportMgr = design.exportManager
            
            # Export STL file.
			stlOptions = exportMgr.createSTLExportOptions(design.rootComponent, folder + '/' + file + valueStr + '.stl')
			exportMgr.execute(stlOptions)
			
			value += step

		param.expression = reset_value
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
