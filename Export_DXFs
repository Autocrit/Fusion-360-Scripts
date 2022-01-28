# Description - Export selected (active) sketch(es) as DXF, whilst modifying parameter

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
	ui = None

	folder = '/Users/tom/Documents/Temp'
	buildVolumes = [250, 300, 350]

	try:
		app = adsk.core.Application.get()
		ui  = app.userInterface
		design = app.activeProduct

		buildVolumeParam = design.userParameters.itemByName('build_volume')

		for selection in ui.activeSelections.asArray():
			sketch = adsk.fusion.Sketch.cast(selection.entity)

			for buildVolume in buildVolumes:
				buildVolumeParam.expression = str(buildVolume)
				sketch.saveAsDXF(folder + '/' + sketch.name + '_' + str(buildVolume) + '.dxf')

	except:
		if ui:
		 ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
