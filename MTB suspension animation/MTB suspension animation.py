import adsk.core, adsk.fusion, adsk.cam, traceback
import time

def run(context):

	ui = None

	try:
		app = adsk.core.Application.get()
		ui  = app.userInterface
		design = app.activeProduct
		components = design.allComponents
		shock = components.itemByName('Dummy shock')
		
		joint = shock.joints.itemByName('Slider 2')
		slider = joint.jointMotion

		# Define the values that control the animation (in mm).
		start = 65
		end = 0
		framecount = 48
		frame = 1

		folder_dialog = ui.createFolderDialog()
		folder_dialog.title = 'Select folder for images'
        
		# Show folder dialog
		if folder_dialog.showDialog() == adsk.core.DialogResults.DialogOK:
			folder = folder_dialog.folder

			# Iterate through the parameter changes
			while frame <= framecount:
				pos = start + (end - start) * ((frame - 1) / (framecount - 1))

				# Set the joint position (in cm)
				slider.slideValue = pos / 10.0
		
				# Allow Fusion to update.
				adsk.doEvents()
				app.activeViewport.refresh()

				# Save the current viewport as an image.
				filename = folder + '/' + str(frame).zfill(4) + '.png'
				app.activeViewport.saveAsImageFile(filename, 1920*2, 1080*2)
				frame += 1

				time.sleep(.5)

	except:
		ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))