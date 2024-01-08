#Author-Che-Wei Wang
#Description- zoom screen to full scale

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    
    try:
            app = adsk.core.Application.get()
            ui = app.userInterface


            # Prompt for reference square size (optional)
            referenceSquareSize = ui.inputBox('Enter the desired size of the reference square in mm (leave blank for 50mm):')
            try:
                desiredWidthInMm = float(referenceSquareSize[0])
            except ValueError:
                desiredWidthInMm = 50  # Default value if conversion fails
            
            
            # Create a sketch and a 100mm x 100mm square
            design = app.activeProduct
            rootComp = design.rootComponent
            sketches = rootComp.sketches
            sketch = sketches.add(rootComp.xYConstructionPlane)
            lines = sketch.sketchCurves.sketchLines
            dimensions = sketch.sketchDimensions

            # Calculate center coordinates and half-width
            centerX = 0
            centerY = 0
            halfWidth = desiredWidthInMm *.1 / 2

            # Draw the square with corners offset from the center
            lines.addTwoPointRectangle(
                adsk.core.Point3D.create(centerX - halfWidth, centerY - halfWidth, 0),
                adsk.core.Point3D.create(centerX + halfWidth, centerY + halfWidth, 0)
            )
            
            
            app.activeViewport.refresh()

            viewport = app.activeViewport
            
            # Get the camera's current eye and target points
            camera = viewport.camera         
            
            
            # Prompt the user to measure the square's width on screen
            onScreenWidthMm = ui.inputBox('Measure the width of the square (in mm) and enter the value:')
            
            # try:

            onScreenWidthMm = float(onScreenWidthMm[0])  # Convert string to float

            # Get the current camera extents
            currentExtentsList = camera.getExtents()  # Store as a list
            currentExtentsWidth = currentExtentsList[1]  # Access the first extents object


            # Calculate the zoom factor needed for full scale
            zoomFactor = onScreenWidthMm / desiredWidthInMm
            # zoomFactor = 1/10
            
            # Calculate the new extents based on screen measurement and desired width
            newExtentsWidth = currentExtentsWidth * zoomFactor

            # Set the camera extents to achiev
            camera.setExtents(newExtentsWidth, newExtentsWidth)
            viewport.camera = camera
            app.activeViewport.refresh()

            # Create a new named view with the desired name
            newView = design.namedViews.add(viewport.camera,"FULL SCALE")

    
                    
            # except:
            #     ui.messageBox('failed')
        
 

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))