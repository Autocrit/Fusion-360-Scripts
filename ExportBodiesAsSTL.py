#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
	ui = None
	try:
		app = adsk.core.Application.get()
		ui  = app.userInterface
		design = app.activeProduct

		folder = '/Users/*user*/Downloads'
		exportMgr = design.exportManager

		selections = ui.activeSelections
		for selection in selections:
			if isinstance(selection.entity, adsk.fusion.BRepBody):
				body = adsk.fusion.BRepBody.cast(selection.entity)
				stlOptions = exportMgr.createSTLExportOptions(body, folder + '/' + body.name + '.stl')
				stlOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
				exportMgr.execute(stlOptions)

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
