import adsk.core, adsk.fusion, adsk.cam, traceback
import time, math

def run(context):

	ui = None

	try:
		app = adsk.core.Application.get()
		ui  = app.userInterface
		design = app.activeProduct
		root = design.rootComponent
		
		joint = root.joints.itemByName('Revolute 1')
		revolute = adsk.fusion.RevoluteJointMotion.cast(joint.jointMotion)

		fps = 24
		duration = 2
		nFrames = duration * fps
		
		startAngle = 0
		endAngle = 360 * (math.pi / 180)
		angleIncr = (endAngle - startAngle) / (nFrames - 1)

		frame = 1
		angle = startAngle
		
		folder_dialog = ui.createFolderDialog()
		folder_dialog.title = 'Select folder for images'
        
		# Show folder dialog
		if folder_dialog.showDialog() == adsk.core.DialogResults.DialogOK:
			folder = folder_dialog.folder
			
			while (frame <= nFrames):
				revolute.rotationValue = angle
				adsk.doEvents()
				app.activeViewport.refresh()
				filename = folder + '/' + str(frame).zfill(4) + '.png'
				app.activeViewport.saveAsImageFile(filename, 1920, 1080)
				frame += 1
				angle += angleIncr
				time.sleep(.5)
			
		revolute.rotationValue = startAngle

	except:
		ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))