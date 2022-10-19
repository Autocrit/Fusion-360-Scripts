#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
	ui = None
	try:
		app = adsk.core.Application.get()
		ui  = app.userInterface
		design = app.activeProduct

		exportMgr = design.exportManager

		selections = ui.activeSelections
		if selections.count > 0:
			# Get folder for STL export
			folder_dialog = ui.createFolderDialog()
			folder_dialog.title = 'Select folder for STL export' 
        
			# Show folder dialog
			if folder_dialog.showDialog() == adsk.core.DialogResults.DialogOK:
				folder = folder_dialog.folder
				for selection in selections:
					if isinstance(selection.entity, adsk.fusion.BRepBody):
						body = adsk.fusion.BRepBody.cast(selection.entity)
						stlOptions = exportMgr.createSTLExportOptions(body, folder + '/' + body.name + '.stl')
						stlOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
						exportMgr.execute(stlOptions)
			else:
				return
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
