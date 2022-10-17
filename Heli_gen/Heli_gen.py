#Author-
#Description-

# Sample spring definition
#pitch_rev_radius = [
#	{'revs':1, 'pitch1':1.25, 'pitch2':1.25, 'radius1':10.7, 'radius2':10.7},
#	{'revs':0.5, 'pitch1':1.25, 'pitch2':main_pitch, 'radius1':10.7, 'radius2':10.7},
#	{'revs':5, 'pitch1':main_pitch, 'pitch2':main_pitch, 'radius1':10.7, 'radius2':10.7},
#	{'revs':0.5, 'pitch1':main_pitch, 'pitch2':1.25, 'radius1':10.7, 'radius2':10.7},
#	{'revs':1, 'pitch1':1.25, 'pitch2':1.25, 'radius1':10.7, 'radius2':10.7},
#]

import adsk.core, adsk.fusion, adsk.cam, traceback
from .Heli_gen_functions import *

def points_to_collection(points):
	# Collection to hold helix points
	points_collection = adsk.core.ObjectCollection.create()
	for point in points:
		points_collection.add(adsk.core.Point3D.create(point['x'], point['y'], point['z']))

	return points_collection

def points_collection_to_string(points):
	string = ''
	for point in points:
		string += str(point.geometry.x) + ',' + str(point.geometry.y) + ',' + str(point.geometry.z) + '\n' 

	return string

def run(context):
	ui = None
	
	create_spring = False
	RENDER = False

	try:
		app = adsk.core.Application.get()
		ui	= app.userInterface
		design = adsk.fusion.Design.cast(app.activeProduct)
		
		component = design.rootComponent
		#component = design.allComponents.itemByName('Animated_spring')

		points_per_rev = 10 # Resolution

		# R122-18rss in mm
		diameter1 = 10.7
		diameter2 = 10.7 
		#wire_diameter = 1.2
		length = 30.1
		end_pitch = 1.25
		end_revs = 1
		transition_revs = 0.5
		main_revs = 5

		# Fox coil spring in mm
		#diameter = 42
		#wire_diameter = 8
		#length = 139.125
		#end_pitch = 9
		#end_revs = 1
		#transition_revs = 0.5
		#main_revs = 4

		sketch = None

		# Check if there are any sketches in this component
		if component.sketches.count < 1:
			create_spring = True
			
			# Get a plane for the sketch
			plane = component.xYConstructionPlane

			# Add sketch to selected plane
			sketch = component.sketches.add(plane)
		else:
			sketch = component.sketches.item(0)

		# Check if there are any SketchFittedSplines in this sketch
		if sketch.sketchCurves.sketchFittedSplines.count < 1:
			create_spring = True

		if create_spring:
			pitch_rev_radius = define_variable_pitch_variable_radius_spring(length, diameter1/2, diameter2/2, end_pitch, end_revs, transition_revs, main_revs)

			pitch_rev_radius_mm_to_cm(pitch_rev_radius)

			#points = make_variable_helix(diameter/10, pitch_rev, points_per_rev)
			points = get_variable_helix_points(pitch_rev_radius, points_per_rev)

			# Get an adsk points collection
			points_collection = points_to_collection(points)
			
			# Get a plane for the sketch
			plane = component.xYConstructionPlane

			# Create Spline through points
			sketch.sketchCurves.sketchFittedSplines.add(points_collection)
		else:
			duration = 1
			fps = 24
			frame_count = fps * duration
			folder = '/Users/[user]/Movies/Fusion 360/Spring/' # Change this
			start_length = length
			end_length = length * 0.6

			for frame in range(1, int(frame_count+1)):
				length = start_length + (end_length - start_length) * ((frame - 1) / (frame_count - 1))

				pitch_rev_radius = define_variable_pitch_variable_radius_spring(length, diameter1/2, diameter2/2, end_pitch, end_revs, transition_revs, main_revs)

				pitch_rev_radius_mm_to_cm(pitch_rev_radius)

				points = get_variable_helix_points(pitch_rev_radius, points_per_rev)

				points_collection = points_to_collection(points)

				fit_points = sketch.sketchCurves.sketchFittedSplines.item(0).fitPoints

				# Update points
				for i in range(0, fit_points.count):
					move_vector = fit_points.item(i).geometry.vectorTo(points_collection.item(i))
					fit_points.item(i).move(move_vector)

				design.computeAll()
				adsk.doEvents()
				app.activeViewport.refresh()

				if RENDER:
					filename = str(frame).zfill(4) + '.png'
					options = adsk.core.SaveImageFileOptions.create(folder + filename)
					options.width = 1920
					options.height = 1080
					options.isAntiAliased = True
					options.isBackgroundTransparent = False
					app.activeViewport.saveAsImageFileWithOptions(options)

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
