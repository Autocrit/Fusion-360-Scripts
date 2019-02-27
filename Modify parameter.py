#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        design = app.activeProduct
        offsetParam = design.userParameters.itemByName('offset')
        
		# Creating offsets from 15.0mm to 45.0mm in 1mm increments
        offset = 15.0
        maxOffset = 45.0
        step = 1
        
        while (offset <= maxOffset):
        	# Modify parameter
            offsetParam.expression = str(offset)

            exportMgr = design.exportManager
            
            # Export STL
            stlOptions = exportMgr.createSTLExportOptions(design.rootComponent, 'C:\\temp\\' + 'thing_' + str(offset) + '_1.0.stl')
            exportMgr.execute(stlOptions)

            # Export .f3d
            fusionArchiveOptions = exportMgr.createFusionArchiveExportOptions('C:\\temp\\' + 'thing_' + str(offset) + '_1.0.f3d');
            exportMgr.execute(fusionArchiveOptions);
            
            offset += step
      except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
