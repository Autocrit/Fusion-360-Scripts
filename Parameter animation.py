#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import math, time

def run(context):
	ui = None
	try:
		app = adsk.core.Application.get()
		ui  = app.userInterface
		#ui.messageBox('Kicker animation')

		design = app.activeProduct

		angleParam1 = design.userParameters.itemByName('angle1')
		if not angleParam1:
			ui.messageBox('The parameter angle1 must exist')
			return
			
		angleParam2 = design.userParameters.itemByName('angle2')
		if not angleParam2:
			ui.messageBox('The parameter angle2 must exist')
			return

		fps = 24
		duration = 2
		nFrames = duration * fps

		startAngle1 = -76 * (math.pi / 180)
		angleRange1 = 76 * (math.pi / 180)
		endAngle1 = startAngle1 + angleRange1
		angleIncr1 = (endAngle1 - startAngle1) / (nFrames - 1)
		
		startAngle2 = 76 * (math.pi / 180)
		angleRange2 = (166 + 76) * (math.pi / 180)
		endAngle2 = startAngle1 + angleRange2
		angleIncr2 = (endAngle2 - startAngle2) / (nFrames - 1)
		
		angle1 = startAngle1
		angle2 = startAngle2

		folder = '~/Pictures/Screenshots/'
		
		frame = 1
		while (frame <= nFrames):
			angleParam1.value = angle1
			angleParam2.value = angle2
			angle1 += angleIncr1
			angle2 += angleIncr2
			adsk.doEvents()
			app.activeViewport.refresh()
			
			# Save the current viewport as an image
			#filename = str(frame).zfill(4) + '.jpg'
			#app.activeViewport.saveAsImageFile(folder + filename, 1920, 1080)
			
			# Or play animation
			frame += 1
			time.sleep(1 / fps)
			
		"""
		# Reverse
		angle1 = endAngle1
		angle2 = endAngle2
		
		frame = 1
		while (frame <= nFrames):
			angleParam1.value = angle1
			angleParam2.value = angle2
			angle1 -= angleIncr1
			angle2 -= angleIncr2
			adsk.doEvents()
			app.activeViewport.refresh()
			
			# Save the current viewport as an image
			#filename = str(frame).zfill(4) + '.jpg'
			#app.activeViewport.saveAsImageFile(folder + filename, 1920, 1080)
			
			# Or play animation
			frame += 1
			time.sleep(1 / fps)
		"""

		angleParam1.value = startAngle1
		angleParam2.value = startAngle2

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
