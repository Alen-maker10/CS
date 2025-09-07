# Author: Alen-maker10
# Description: Creates a rectangular box based on user input for width, depth, and height.

import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        # Get the application and user interface objects.
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Get the root component of the active design.
        design = app.activeProduct
        rootComp = design.rootComponent

        # --- User Input ---
        # Prompt the user for the box dimensions.
        # The inputBox method returns the user's string and a boolean indicating if they clicked OK.
        (input_width, isCancelled) = ui.inputBox('Enter box width (in cm):', 'Box Width', '10')
        if isCancelled: return

        (input_depth, isCancelled) = ui.inputBox('Enter box depth (in cm):', 'Box Depth', '8')
        if isCancelled: return

        (input_height, isCancelled) = ui.inputBox('Enter box height (in cm):', 'Box Height', '6')
        if isCancelled: return
        
        # Convert the string inputs to numbers (in cm). Fusion 360 works in cm internally.
        try:
            width = float(input_width)
            depth = float(input_depth)
            height = float(input_height)
        except ValueError:
            ui.messageBox('Please enter valid numbers for the dimensions.')
            return

        # --- Sketching the Rectangle ---
        # Create a new sketch on the XY plane.
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        # Draw a rectangle starting from the origin (0,0) to the specified width and depth.
        sketch.sketchCurves.sketchLines.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(width, depth, 0))

        # --- Extruding to 3D ---
        # Get the profile of the rectangle from the sketch.
        prof = sketch.profiles.item(0)

        # Create an extrude feature.
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        # Define the distance for the extrusion using the user-provided height.
        distance = adsk.core.ValueInput.createByReal(height)
        extInput.setDistanceExtent(False, distance)

        # Execute the extrude command.
        extrudes.add(extInput)
        
        ui.messageBox('Box created successfully!')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))