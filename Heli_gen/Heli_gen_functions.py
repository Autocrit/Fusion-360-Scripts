import math

def get_variable_helix_points(pitch_rev_radius, points_per_rev):
	# Sample spring definition
#pitch_rev_radius = [
#	{'revs':1, 'pitch1':1.25, 'pitch2':1.25, 'radius1':10.7, 'radius2':10.7},
#	{'revs':0.5, 'pitch1':1.25, 'pitch2':main_pitch, 'radius1':10.7, 'radius2':10.7},
#	{'revs':5, 'pitch1':main_pitch, 'pitch2':main_pitch, 'radius1':10.7, 'radius2':10.7},
#	{'revs':0.5, 'pitch1':main_pitch, 'pitch2':1.25, 'radius1':10.7, 'radius2':10.7},
#	{'revs':1, 'pitch1':1.25, 'pitch2':1.25, 'radius1':10.7, 'radius2':10.7},
#]

	# Array to hold helix points
	points = []

	t = t_start = z_start = z = 0

	for item in pitch_rev_radius:
		revs = item['revs']
		pitch1 = item['pitch1']
		pitch2 = item['pitch2']
		radius1 = item['radius1']
		radius2 = item['radius2']
		avg_pitch = (pitch1 + pitch2) / 2
		t_end = t_start + int(revs * points_per_rev)
		while t <= t_end:
			# t0 is progress along this section
			t0 = t - t_start

			# Get pitch and radius at this point
			pitch = pitch1 + (t0 * (pitch2 - pitch1)) / (revs * points_per_rev)
			radius = radius1 + (t0 * (radius2 - radius1)) / (revs * points_per_rev)

			# Get the helix point
			x = radius * math.cos(math.radians(360) * t / points_per_rev)
			y = radius * math.sin(math.radians(360) * t / points_per_rev)
			z = z_start + (pitch + pitch1) / 2 * (t0 / points_per_rev)

			# Create point
			point = {'x':x, 'y':y, 'z':z}
			
			# Add Point to array
			points.append(point)
			t += 1
		t_start = t - 1
		z_start += revs * avg_pitch

	return points

def print_point(point):
	print(str(point['x']) + ',' + str(point['y']) + ',' + str(point['z']))

def print_points(points):
	for point in points:
		print_point(point)

def point_to_string(point):
	return (str(point['x']) + ',' + str(point['y']) + ',' + str(point['z']))

def points_to_string(points):
	string = ''
	for point in points:
		string += point_to_string(point) + '\n'

	return string

def pitch_rev_radius_mm_to_cm(pitch_rev):
	for item in pitch_rev:
		item['pitch1'] = item['pitch1'] / 10
		item['pitch2'] = item['pitch2'] / 10
		item['radius1'] = item['radius1'] / 10
		item['radius2'] = item['radius2'] / 10

# Some functions to help with defining a variable pitch/variable radius spring

# A spring consisting of an end section, a transition section, a main section, a second transition section, and a second end section
# The end section pitch would be just greater than the wire diameter
# The pitch of the transition section transitions between the end pitch and the main pitch
def calculate_main_pitch(length, end_pitch, end_revs, transition_revs, main_revs):
	return (length - 2 * end_pitch * end_revs - end_pitch * transition_revs) / (transition_revs + main_revs)

def pitch_rev_radius_taper(pitch_rev_radius, radius1, radius2):
	# Get the total number of revolutions
	revs = 0
	for item in pitch_rev_radius:
		revs += item['revs']

	r1 = radius1
	rev = 0
	for item in pitch_rev_radius:
		rev += item['revs']
		r2 = radius1 + (radius2 - radius1) * rev / revs
		item['radius1'] = r1
		item['radius2'] = r2
		r1 = r2

def define_variable_pitch_spring(length, radius, end_pitch, end_revs, transition_revs, main_revs):
	main_pitch = calculate_main_pitch(length, end_pitch, end_revs, transition_revs, main_revs)

	pitch_rev_radius = [
		{'revs':end_revs, 'pitch1':end_pitch, 'pitch2':end_pitch, 'radius1':radius, 'radius2':radius},
		{'revs':transition_revs, 'pitch1':end_pitch, 'pitch2':main_pitch, 'radius1':radius, 'radius2':radius},
		{'revs':main_revs, 'pitch1':main_pitch, 'pitch2':main_pitch, 'radius1':radius, 'radius2':radius},
		{'revs':transition_revs, 'pitch1':main_pitch, 'pitch2':end_pitch, 'radius1':radius, 'radius2':radius},
		{'revs':end_revs, 'pitch1':end_pitch, 'pitch2':end_pitch, 'radius1':radius, 'radius2':radius},
	]

	return pitch_rev_radius

def define_variable_pitch_variable_radius_spring(length, radius1, radius2, end_pitch, end_revs, transition_revs, main_revs):
	main_pitch = calculate_main_pitch(length, end_pitch, end_revs, transition_revs, main_revs)

	pitch_rev_radius = [
		{'revs':end_revs, 'pitch1':end_pitch, 'pitch2':end_pitch},
		{'revs':transition_revs, 'pitch1':end_pitch, 'pitch2':main_pitch},
		{'revs':main_revs, 'pitch1':main_pitch, 'pitch2':main_pitch},
		{'revs':transition_revs, 'pitch1':main_pitch, 'pitch2':end_pitch},
		{'revs':end_revs, 'pitch1':end_pitch, 'pitch2':end_pitch},
	]

	pitch_rev_radius_taper(pitch_rev_radius, radius1, radius2)

	return pitch_rev_radius

def pitch_rev_radius_to_string(pitch_rev_radius):
	string = ''
	for item in pitch_rev_radius:
		string += 'revs:' + str(item['revs'])
		string += ', pitch1:' + str(item['pitch1'])
		string += ', pitch2:' + str(item['pitch2'])
		string += ', radius1:' + str(item['radius1'])
		string += ', radius2:' + str(item['radius2'])
		string += '\n'

	return string
