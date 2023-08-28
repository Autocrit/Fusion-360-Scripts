#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import json, time, math

rotate = True

def loadRALColours(ui):
	fileDlg = ui.createFileDialog()
	fileDlg.isMultiSelectEnabled = False
	fileDlg.title = 'Fusion Open File Dialog'
	fileDlg.filter = '*.json'
	dlgResult = fileDlg.showOpen()
	
	if dlgResult == adsk.core.DialogResults.DialogOK:
		with open(fileDlg.filename, "r") as read_file:
			return json.load(read_file)

	return None

def run(context):
	ui = None
	try:
		app = adsk.core.Application.get()
		ui  = app.userInterface
		design = app.activeProduct

		# Create progress dialog
		progressDialog = ui.createProgressDialog()
		progressDialog.cancelButtonText = 'Cancel'
		progressDialog.isBackgroundTranslucent = False
		progressDialog.isCancelButtonShown = True
		progress = 0

		root = design.rootComponent

		components = design.allComponents

		#body = root.bRepBodies.item(0)

		componentNames = [
			"Head_tube",
			"Bottom_bracket_shell",
			"Down_tube",
			"Seat_tube_upper",
			"Seat_tube_lower",
			"Top_tube",
			"Seat_tube_gusset",
			"Yoke",
			"Chainstay_tube",
			"Stay_end",
			"Drive_side_dropout",
			"Drive_side_seatstay_tube",
			"Non_drive_side_dropout",
			"Non_drive_side_seatstay_tube"
		]

		bodies = []
		for componentName in componentNames:
			component = components.itemByName(componentName)
			for body in component.bRepBodies:
				bodies.append(body)

		ralColours = loadRALColours(ui)

		designAppearances = design.appearances
		appearance = designAppearances.itemByName('RAL_COLOUR')
		if appearance == None:
			fusionMaterials = app.materialLibraries.itemByName('Fusion 360 Appearance Library')
			appearance = fusionMaterials.appearances.itemByName('Powder Coat (Green)')
			appearance = design.appearances.addByCopy(appearance, 'RAL_COLOUR')

		colorProp = appearance.appearanceProperties.itemByName('Color')

		folder_dialog = ui.createFolderDialog()
		folder_dialog.title = 'Select folder for images'
        
		# Show folder dialog
		if ralColours:
			if folder_dialog.showDialog() == adsk.core.DialogResults.DialogOK:
				folder = folder_dialog.folder

				progressDialog.show('Progress Dialog', 'Percentage: %p, Current Value: %v, Total steps: %m', 0, len(ralColours), 1)

				adsk.doEvents()
	
				for ralColour in ralColours:
					if progressDialog.wasCancelled:
						break
				
					r = ralColour["colour"]["rgb"]["r"]
					g = ralColour["colour"]["rgb"]["g"]
					b = ralColour["colour"]["rgb"]["b"]

					filename = ralColour["code"] + " " + ralColour["name"]["en"]

					colorProp.value = adsk.core.Color.create(r, g, b, 0)

					for body in bodies:
						body.appearance = appearance

					if rotate:
						joint = root.joints.itemByName('Revolute 1')
						revolute = adsk.fusion.RevoluteJointMotion.cast(joint.jointMotion)

						fps = 24
						duration = 3
						nFrames = duration * fps
						
						startAngle = 0
						endAngle = 360 * (math.pi / 180)
						angleIncr = (endAngle - startAngle) / (nFrames - 1)

						frame = 1
						angle = startAngle

						while (frame <= nFrames):
							if progressDialog.wasCancelled:
								break

							revolute.rotationValue = angle
							adsk.doEvents()
							app.activeViewport.refresh()

							path = folder + '/' + filename + " " + str(frame).zfill(4) + '.png'
							app.activeViewport.saveAsImageFile(path, 1920, 1080)
							frame += 1
							angle += angleIncr

							#time.sleep(.5)

					else:
						if progressDialog.wasCancelled:
							break

						adsk.doEvents()
						app.activeViewport.refresh()

						# Save the current viewport as an image.
						path = folder + '/' + filename + '.png'
						app.activeViewport.saveAsImageFile(path, 1920, 1080)

						progress += 1
						progressDialog.progressValue = progress

					progress += 1
					progressDialog.progressValue = progress
		
		# Hide the progress dialog at the end.
		progressDialog.hide()

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
