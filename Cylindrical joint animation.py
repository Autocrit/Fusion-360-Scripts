import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):

	ui = None

	try:
		app = adsk.core.Application.get()
		ui  = app.userInterface
		design = app.activeProduct
		components = design.allComponents
		shock = components.itemByName('Fox Float DPX2')
		joint = shock.joints.itemByName('Cyl1')
		cylindrical = joint.jointMotion

		# Define the values that control the animation (in mm).
		start = -60
		end = -110

    		framecount = 48
		frame = 1

		# Iterate through
		while frame <= framecount:
			pos = start + (end - start) * ((frame - 1) / (framecount - 1))

			# Set the joint position (in cm)
			cylindrical.slideValue = pos / 10.0
	
			# Allow Fusion to update.
			adsk.doEvents()
			#app.activeViewport.refresh()

			# Save the current viewport as an image.
			filename = '/temp/frame_' + str(frame).zfill(4) + '.jpg'
			app.activeViewport.saveAsImageFile(filename, 1920, 1080)
			frame += 1

	except:
		ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
