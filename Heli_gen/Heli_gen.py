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
	try:
		app = adsk.core.Application.get()
		ui	= app.userInterface
		design = adsk.fusion.Design.cast(app.activeProduct)
		
		component = design.rootComponent

		points_per_rev = 10 # Resolution

		diameter = 10.7
		length = 30.1
		end_pitch = 1.25
		end_revs = 1
		transition_revs = 0.5
		main_revs = 5

		# Define the spring as an array of revolutions, start and end pitches, start and end radii
		pitch_rev_radius = define_variable_pitch_variable_radius_spring(length, diameter/2, diameter/2, end_pitch, end_revs, transition_revs, main_revs)

		# Definitions are in mm but need cm
		pitch_rev_radius_mm_to_cm(pitch_rev_radius)

		# Get the array of points
		points = get_variable_helix_points(pitch_rev_radius, points_per_rev)

		# Get an adsk points collection
		points_collection = points_to_collection(points)
		
		# Get a plane for the sketch
		plane = component.xYConstructionPlane

		# Add sketch to selected plane
		sketch = component.sketches.add(plane)

		# Create Spline through points
		sketch.sketchCurves.sketchFittedSplines.add(points_collection)

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
