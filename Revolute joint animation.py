import adsk.core, adsk.fusion, adsk.cam, traceback
import time, math

def run(context):

	ui = None

	try:
		app = adsk.core.Application.get()
		ui  = app.userInterface
		design = app.activeProduct
		root = design.rootComponent
		
		joint = root.joints.itemByName('Rev1')
		revolute = adsk.fusion.RevoluteJointMotion.cast(joint.jointMotion)

		for i in range(0,360,6):
			revolute.rotationValue = -1 * i * (math.pi/180)
			adsk.doEvents()
			app.activeViewport.refresh()
			time.sleep(1)

	except:
		ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
