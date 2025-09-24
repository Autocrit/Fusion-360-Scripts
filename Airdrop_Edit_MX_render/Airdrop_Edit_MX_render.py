# Borrowed from https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-AC5A8134-2634-4077-9BD5-16B2945CBFDD

import adsk.core
import adsk.fusion
import traceback
import threading
import json

app = None
ui = adsk.core.UserInterface.cast(None)
handlers = []
stopFlag = None
checkProgress = 'RenderProgress'
customEvent = None
renderFutures = []

app = adsk.core.Application.get()
ui  = app.userInterface
        
# The event handler that responds to the custom event being fired.
class ThreadEventHandler(adsk.core.CustomEventHandler):
	def __init__(self):
		super().__init__()
	def notify(self, args):
		try:
			# Iterate through the render futures to display the status in the TEXT COMMAND window
			# and check to see if it's finished.
			stillProcessing = False
			future: adsk.fusion.RenderFuture
			for future in renderFutures:
				if future.renderState == adsk.fusion.LocalRenderStates.QueuedLocalRenderState:
					stillProcessing = True
				elif future.renderState == adsk.fusion.LocalRenderStates.ProcessingLocalRenderState:
					stillProcessing = True

			if(not stillProcessing):
				# All jobs have been processed, so terminate the script. This will result
				# in the stop function being called where the final cleanup is done.
				adsk.terminate()
		except:
			if ui:
				ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# The class for the new thread.
class MyThread(threading.Thread):
	def __init__(self, event):
		threading.Thread.__init__(self)
		self.stopped = event

	def run(self):
		# Every five seconds fire a custom event to check the rendering progress.
		while not self.stopped.wait(5):
			app.fireCustomEvent(checkProgress)

def load_json():
	dialog = ui.createFileDialog()
	dialog.isMultiSelectEnabled = False
	dialog.title = "Fusion Open File Dialog"
	dialog.filter = "*.json"
	result = dialog.showOpen()
	
	if result == adsk.core.DialogResults.DialogOK:
		with open(dialog.filename, "r") as read_file:
			return json.load(read_file)

	return None

def run(context):
	try:
		# Get the active Design
		design: adsk.fusion.Design = app.activeProduct

		# Get the RenderManager from the Design and set the resolution of the output image.
		rm = design.renderManager
		render = rm.rendering
		render.resolution = adsk.fusion.RenderResolutions.Video1920x1080RenderResolution
		render.resolutionWidth = 1920 * 2

		# There needs to be an appearance named "Power Coat" already applied
		appearance = design.appearances.itemByName("Powder Coat")

		# Load the colours from a JSON file
		ral_colours = load_json()

		for ral_colour in ral_colours:
			r = ral_colour["colour"]["rgb"]["r"]
			g = ral_colour["colour"]["rgb"]["g"]
			b = ral_colour["colour"]["rgb"]["b"]

			name = f"{ral_colour['code']} {ral_colour['name']['en']}"

			colorProp = adsk.core.ColorProperty.cast(appearance.appearanceProperties.itemByName("Color"))
			colorProp.value = adsk.core.Color.create(r, g, b, 0)

			# Define the filename for this frame.
			filename = f'/Users/tom/Desktop/Temp/Tighter/{name}.jpg'

			# Start the render.
			renderFutures.append(render.startLocalRender(filename))

		# Create a new thread that is used to watch the progress of the renders.
		# This is done in a seperate thread, so the Fusion main thread isn't blocked.
		global stopFlag        
		stopFlag = threading.Event()
		myThread = MyThread(stopFlag)
		myThread.start()

		# Register the custom event and connect the handler.
		# This is done so the monitoring thread can trigger this
		# event to allow work to happen on Fusion's main thread.
		global customEvent
		customEvent = app.registerCustomEvent(checkProgress)
		onThreadEvent = ThreadEventHandler()
		customEvent.add(onThreadEvent)
		handlers.append(onThreadEvent)

		# Don't terminate the script, but allow it to keep running.
		adsk.autoTerminate(False)
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
	try:
		# Clean up the events.
		if handlers.count:
			customEvent.remove(handlers[0])
			stopFlag.set() 
			app.unregisterCustomEvent(checkProgress)

			ui.messageBox('Rendering is complete')
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))