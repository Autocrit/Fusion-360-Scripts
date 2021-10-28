import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
	ui = None
	try:
		app = adsk.core.Application.get()
		ui  = app.userInterface
		design = app.activeProduct
		rootComp = design.rootComponent

		sketch = rootComp.sketches.itemByName('text')
		sketchText = sketch.sketchTexts.item(0)
		
		em_start = 0.800
		em_end = 1.200
		em_step = 0.005

		folder = '/Users/tom/Documents/Temp/'
		
		em = em_start
		
		em_end = 0.800

		while (em <= em_end):
			text = "{:.3f}".format(em)
			sketchText.text = str(text)
			filename = folder + text + '.stl'

			# Save as STL
			exportMgr = design.exportManager
			stlOptions = exportMgr.createSTLExportOptions(rootComp, filename)
			stlOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
			exportMgr.execute(stlOptions)
			
			em += em_step
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
