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
		renderoneframe = False

		# Iterate through the parameter changes
		while frame <= framecount:
			pos = start + (end - start) * ((frame - 1) / (framecount - 1))

			# Set the joint position (in cm)
			slider.slideValue = pos / 10.0
	
			# Allow Fusion to update.
			adsk.doEvents()
			app.activeViewport.refresh()

			# Save the current viewport as an image.
			filename = '/Users/tom/Pictures/Kavenz/kavenz_' + str(frame).zfill(4) + '.png'
			app.activeViewport.saveAsImageFile(filename, 1920*2, 1080*2)
			frame += 1
			if renderoneframe == True:
				break
			time.sleep(.5)

	except:
		ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))