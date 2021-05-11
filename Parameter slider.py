# Based on https://modthemachine.typepad.com/my_weblog/2020/03/drive-all-revolute-joints.html
# Uses one 0 to 100% slider to drive two parameters

import adsk.core, adsk.fusion, adsk.cam, math, traceback

# Global variable used to maintain a reference to all event handlers.
handlers = []

# Other global variables
joints = None
angleParam1 = None
angleParam2 = None
input1 = None
angle1_min = -76
angle1_max = 0
angle2_min = 76
angle2_max = 166
commandName = "DriveParams"

app = adsk.core.Application.get()
if app:
	ui = app.userInterface
            
# Event handler for the inputChanged event.
class MyInputChangedHandler(adsk.core.InputChangedEventHandler):
	def __init__(self):
		super().__init__()
	def notify(self, args):
		eventArgs = adsk.core.InputChangedEventArgs.cast(args)
		commandInput = eventArgs.input
        
# Event handler for the executePreview event.
class MyExecutePreviewHandler(adsk.core.CommandEventHandler):
	def __init__(self):
		super().__init__()
	def notify(self, args):
		eventArgs = adsk.core.CommandEventArgs.cast(args)

		global angleParam1, angleParam2

		percent = input1.valueOne
		angleParam1.value = (math.pi / 180) * (angle1_min + (percent / 100) * (angle1_max - angle1_min))
		angleParam2.value = (math.pi / 180) * (angle2_min + (percent / 100) * (angle2_max - angle2_min))

		# Make it accept the changes whatever happens
		eventArgs.isValidResult = True
        

class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):    
	def __init__(self):
		super().__init__()        
	def notify(self, args):
		try:
			command = adsk.core.Command.cast(args.command)

			# Subscribe to the various command events
			onInputChanged = MyInputChangedHandler()
			command.inputChanged.add(onInputChanged)
			handlers.append(onInputChanged)

			onExecutePreview = MyExecutePreviewHandler()
			command.executePreview.add(onExecutePreview)
			handlers.append(onExecutePreview)

			onDestroy = MyCommandDestroyHandler()
			command.destroy.add(onDestroy)
			handlers.append(onDestroy)

			inputs = command.commandInputs

			global input1

			input1 = inputs.addIntegerSliderCommandInput(
				commandName + angleParam1.name,
				angleParam1.name,
				0,
				100)
			input1.valueOne = 0

			command.isAutoExecute = True
                
		except:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))              
            
            
class MyCommandDestroyHandler(adsk.core.CommandEventHandler):
	def __init__(self):
		super().__init__()
	def notify(self, args):
		try:
			commandDefinitions = ui.commandDefinitions
			# Check the command exists or not
			cmdDef = commandDefinitions.itemById(commandName)
			if cmdDef:
				cmdDef.deleteMe                

			# When the command is done, terminate the script
			# this will release all globals which will remove all event handlers
			adsk.terminate()

		except:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))        

def run(context):
	try:
		product = app.activeProduct
		design = adsk.fusion.Design.cast(product)
		if not design:
			ui.messageBox('It is not supported in current workspace, please change to MODEL workspace and try again.')
			return

		global angleParam1, angleParam2

		angleParam1 = design.userParameters.itemByName('angle1')
		if not angleParam1:
			ui.messageBox('The parameter angle1 must exist')
			return

		angleParam2 = design.userParameters.itemByName('angle2')
		if not angleParam2:
			ui.messageBox('The parameter angle2 must exist')
			return

		global joints
		#joints = design.rootComponent.joints

		commandDefinitions = ui.commandDefinitions
		# Check the command exists or not
		cmdDef = commandDefinitions.itemById(commandName)
		if not cmdDef:
			cmdDef = commandDefinitions.addButtonDefinition(
				commandName, commandName, commandName, '') 

		# Subscribe to events 
		onCommandCreated = MyCommandCreatedHandler()
		cmdDef.commandCreated.add(onCommandCreated)
		# Keep the handler referenced beyond this function
		handlers.append(onCommandCreated)

		# Run the command
		inputs = adsk.core.NamedValues.create()
		cmdDef.execute(inputs)

		# Prevent this module from being terminated when the script returns, 
		# because we are waiting for event handlers to fire
		adsk.autoTerminate(False)

	except:
		ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))