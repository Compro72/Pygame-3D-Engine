# Umar Ahmed
# 2024 - 2025
#Read README.md for documentation
#Start at line 479

import pygame
import pygame.gfxdraw
import math
import random
import copy

#----------Utility Functions----------

def hsv_to_rgb(hue, saturation, value):
	if saturation == 0:
		value *= 255
		return (value, value, value)
	
	sector = math.floor(hue*6)
	fraction = (hue*6)-sector
	
	p = float(255 * value * (1 - saturation))
	q = float(255 * value * (1 - saturation * fraction))
	t = float(255 * value * (1 - saturation * (1 - fraction)))
	
	value *= 255
	sector = sector % 6

	if sector == 0:
		return (value, t, p)
	if sector == 1:
		return (q, value, p)
	if sector == 2:
		return (p, value, t)
	if sector == 3:
		return (p, q, value)
	if sector == 4:
		return (t, p, value)
	if sector == 5:
		return (value, p, q)
	
def rotate_x(point, angle, origin=(0, 0 ,0)):
	y = point[1]-origin[1]
	z = point[2]-origin[2]

	new_y = y * math.cos(angle) - z * math.sin(angle)
	new_z = y * math.sin(angle) + z * math.cos(angle)

	new_y += origin[1]
	new_z += origin[2]

	return [point[0], new_y, new_z]

def rotate_y(point, angle, origin=(0, 0 ,0)):
	x = point[0]-origin[0]
	z = point[2]-origin[2]

	new_x = x * math.cos(angle) + z * math.sin(angle)
	new_z = -x * math.sin(angle) + z * math.cos(angle)

	new_x += origin[0]
	new_z += origin[2]

	return [new_x, point[1], new_z]

def rotate_z(point, angle, origin=(0, 0 ,0)):
	x = point[0]-origin[0]
	y = point[1]-origin[1]

	new_x = x * math.cos(angle) - y * math.sin(angle)
	new_y = x * math.sin(angle) + y * math.cos(angle)

	new_x += origin[0]
	new_y += origin[1]

	return [new_x, new_y, point[2]]

def rotate(point, angles, origin=(0, 0, 0), rotation_axis_angles=(0, 0, 0)):
	#Rotate point into the local coordinate system
	new_point = rotate_z(point, -rotation_axis_angles[2], origin)
	new_point = rotate_y(new_point, -rotation_axis_angles[1], origin)
	new_point = rotate_x(new_point, -rotation_axis_angles[0], origin)
	
	#Rotate point in the local coordinate system
	new_point = rotate_x(new_point, angles[0], origin)
	new_point = rotate_y(new_point, angles[1], origin)
	new_point = rotate_z(new_point, angles[2], origin)

	#Rotate point back into the global coordinate system
	new_point = rotate_x(new_point, rotation_axis_angles[0], origin)
	new_point = rotate_y(new_point, rotation_axis_angles[1], origin)
	new_point = rotate_z(new_point, rotation_axis_angles[2], origin)

	#Return the new point
	return new_point

def convert_from_cartesian(point, screen_size):
	return [((screen_size[0]/2)+point[0]), ((screen_size[1]/2)-point[1])]

def normal_to_euler(normal):
	if normal[2]>1:
		normal = (normal[0], normal[1], 1)
	if normal[2]<-1:
		normal = (normal[0], normal[1], -1)
	return (math.asin(-normal[2]), math.atan2(normal[0], normal[2]), 0)


#----------Camera----------

class Camera:
	#Constructor initializes the class
	def __init__(self, screen, position=(0, 0, 0), rotation_x=0, rotation_y=0, near_plane=0.1, view_factor=400):
		self.position = position
		self.rotation_x = rotation_x
		self.rotation_y = rotation_y
		
		self.near_plane = near_plane
		self.view_factor = view_factor

		self.sin_cam_rot_x = 0
		self.sin_cam_rot_y = 0
		self.cos_cam_rot_x = 0
		self.cos_cam_rot_y = 0
		
		self.screen = screen
		self.faces_drawn = 0

	def update_trig_values(self):
		self.sin_cam_rot_x = math.sin(self.rotation_x)
		self.sin_cam_rot_y = math.sin(self.rotation_y)
		self.cos_cam_rot_x = math.cos(self.rotation_x)
		self.cos_cam_rot_y = math.cos(self.rotation_y)
		
	def get_distance(self, point):
		return math.sqrt((point[0] - self.position[0]) ** 2 + (point[1] - self.position[1]) ** 2 + (point[2] - self.position[2]) ** 2)
	
	def clip_2D_polygon(self, polygon):
		screen_size = self.screen.get_size()
		screen_x_min = -screen_size[0]/2
		screen_x_max = screen_size[0]/2
		
		screen_y_min = -screen_size[1]/2
		screen_y_max = screen_size[1]/2
		
		for edge in range(4):
			new_polygon = []
			for i in range(len(polygon)):
				p1 = polygon[i]
				p2 = polygon[(i + 1) % len(polygon)]
				if ((edge == 0 and p2[0] >= screen_x_min) or (edge == 1 and p2[0] <= screen_x_max) or (edge == 2 and p2[1] >= screen_y_min) or (edge == 3 and p2[1] <= screen_y_max)):
					if ((edge == 0 and p1[0] < screen_x_min) or (edge == 1 and p1[0] > screen_x_max) or (edge == 1 and p1[0] > screen_x_max) or (edge == 2 and p1[1] < screen_y_min) or (edge == 3 and p1[1] > screen_y_max)):
						if edge == 0:
							new_polygon.append([screen_x_min, p1[1] + (p2[1] - p1[1]) * (screen_x_min - p1[0]) / (p2[0] - p1[0])])
						elif edge == 1:
							new_polygon.append([screen_x_max, p1[1] + (p2[1] - p1[1]) * (screen_x_max - p1[0]) / (p2[0] - p1[0])])
						elif edge == 2:
							new_polygon.append([p1[0] + (p2[0] - p1[0]) * (screen_y_min - p1[1]) / (p2[1] - p1[1]), screen_y_min])
						elif edge == 3:
							new_polygon.append([p1[0] + (p2[0] - p1[0]) * (screen_y_max - p1[1]) / (p2[1] - p1[1]), screen_y_max])
					new_polygon.append(p2)
				elif ((edge == 0 and p1[0] >= screen_x_min) or (edge == 1 and p1[0] <= screen_x_max) or (edge == 2 and p1[1] >= screen_y_min) or (edge == 3 and p1[1] <= screen_y_max)):
					if edge == 0:
						new_polygon.append([screen_x_min, p1[1] + (p2[1] - p1[1]) * (screen_x_min - p1[0]) / (p2[0] - p1[0])])
					elif edge == 1:
						new_polygon.append([screen_x_max, p1[1] + (p2[1] - p1[1]) * (screen_x_max - p1[0]) / (p2[0] - p1[0])])
					elif edge == 2:
						new_polygon.append([p1[0] + (p2[0] - p1[0]) * (screen_y_min - p1[1]) / (p2[1] - p1[1]), screen_y_min])
					elif edge == 3:
						new_polygon.append([p1[0] + (p2[0] - p1[0]) * (screen_y_max - p1[1]) / (p2[1] - p1[1]), screen_y_max])
			polygon = new_polygon
			if len(polygon) == 0:
				return []
		return polygon

	#Main 3D projection script
	def get_screen_polygon(self, face):
		screen_polygon = []
	
		prev_x1, prev_y1, prev_z1 = face[0]
		cam_x, cam_y, cam_z = self.position
	
		#Pre-compute differences
		cam_x_diff = prev_x1 - cam_x
		cam_y_diff = prev_y1 - cam_y
		cam_z_diff = prev_z1 - cam_z
	
		#Initialize the starting point
		x2 = (cam_z_diff * self.sin_cam_rot_y) + (cam_x_diff * self.cos_cam_rot_y)
		y2 = (cam_y_diff * self.cos_cam_rot_x) - ((cam_z_diff * self.cos_cam_rot_y - cam_x_diff * self.sin_cam_rot_y) * self.sin_cam_rot_x)
		z2 = (cam_y_diff * self.sin_cam_rot_x) + ((cam_z_diff * self.cos_cam_rot_y - cam_x_diff * self.sin_cam_rot_y) * self.cos_cam_rot_x)
	
		for i in range(len(face)):
			prev_x2, prev_y2, prev_z2 = face[(i+1)%len(face)]
		
			#Set point 1 to point 2
			x1 = x2
			y1 = y2
			z1 = z2
		
			#Set point 2 to next point
			cam_x_diff = prev_x2 - cam_x
			cam_y_diff = prev_y2 - cam_y
			cam_z_diff = prev_z2 - cam_z
	
			x2 = (cam_z_diff * self.sin_cam_rot_y) + (cam_x_diff * self.cos_cam_rot_y)
			y2 = (cam_y_diff * self.cos_cam_rot_x) - ((cam_z_diff * self.cos_cam_rot_y - cam_x_diff * self.sin_cam_rot_y) * self.sin_cam_rot_x)
			z2 = (cam_y_diff * self.sin_cam_rot_x) + ((cam_z_diff * self.cos_cam_rot_y - cam_x_diff * self.sin_cam_rot_y) * self.cos_cam_rot_x)

			#Point 1 is in front of the near plane
			if z1 > self.near_plane:
			
				#Calculate and add the screen point for point 1
				screen_point_x = (self.view_factor * (x1 / z1))
				screen_point_y = (self.view_factor * (y1 / z1))
				screen_polygon.append((screen_point_x, screen_point_y))
				
				#Point 2 is behind the near plane
				if z2 < self.near_plane:
					#Calculate and add the intersection between the line p1 to p2 and the near plane
					percent = (self.near_plane - z1) / (z2 - z1)
					screen_point_x = (self.view_factor * ((x1 + ((x2 - x1) * percent)) / self.near_plane))
					screen_point_y = (self.view_factor * ((y1 + ((y2 - y1) * percent)) / self.near_plane))
					screen_polygon.append((screen_point_x, screen_point_y))
					
			#Point 2 is in front of the near plane. Assume point 1 is behind the near plane
			elif z2 > self.near_plane:
				
				#Calculate and add the intersection between the line p1 to p2 and the near plane
				percent = (self.near_plane - z1) / (z2 - z1)
				screen_point_x = (self.view_factor * ((x1 + ((x2 - x1) * percent)) / self.near_plane))
				screen_point_y = (self.view_factor * ((y1 + ((y2 - y1) * percent)) / self.near_plane))
				screen_polygon.append((screen_point_x, screen_point_y))
		
		#Clip the screen_polygon to fit the screen
		screen_polygon = self.clip_2D_polygon(screen_polygon)

		return screen_polygon

	def move(self, offset):
		self.position = (self.position[0]+offset[0], self.position[1]+offset[1], self.position[2]+offset[2])

	def rotate(self, rot_x, rot_y):
		self.rotation_x += rot_x
		self.rotation_y += rot_y


#----------Face----------

class Face:
	#Constructor initializes the class
	def __init__(self, face_points, colour, normal, thickness=None):
		self.points = face_points
		self.normal = normal
		self.colour = colour
		self.thickness = thickness

		#Save orignal state
		self.points_copy = copy.deepcopy(self.points)
		self.normal_copy = copy.deepcopy(self.normal)
		self.colour_copy = copy.deepcopy(self.colour)
		self.thickness_copy = copy.deepcopy(self.thickness)

	def reset(self):
		#Reload orignal state
		self.points = copy.deepcopy(self.points_copy)
		self.normal = copy.deepcopy(self.normal_copy)
		self.colour = copy.deepcopy(self.colour_copy)
		self.thickness = copy.deepcopy(self.thickness_copy)

	def move(self, offset):
		for i in range(len(self.points)):
			point = self.points[i]
			self.points[i] = (point[0]+offset[0], point[1]+offset[1], point[2]+offset[2])

	def rotate(self, offset, origin="self", rotation_axis_angles=(0, 0, 0)):
		if origin=="self":
			current_center = self.get_center()
			for i in range(len(self.points)):
				self.points[i] = rotate(self.points[i], offset, current_center, rotation_axis_angles)
			self.normal = rotate(self.normal, offset, (0, 0, 0), rotation_axis_angles)
		else:
			for i in range(len(self.points)):
				self.points[i] = rotate(self.points[i], offset, origin, rotation_axis_angles)
			self.normal = rotate(self.normal, offset, (0, 0, 0), rotation_axis_angles)

	def get_center(self):
		#Average (x, y, z) of all points
		center_x = sum(point[0] for point in self.points) / len(self.points)
		center_y = sum(point[1] for point in self.points) / len(self.points)
		center_z = sum(point[2] for point in self.points) / len(self.points)
		
		return (center_x, center_y, center_z)

	def get_cam_distance(self, camera):
		# Calculate the distance from the camera to the face center
		return camera.get_distance(self.get_center())

	def check_backface(self, camera_pos, face_point, face_normal):
		#Check if face if face is pointing towards the camera
		camera_to_face_normal = (face_point[0]-camera_pos[0], face_point[1]-camera_pos[1], face_point[2]-camera_pos[2])
		dot_product = camera_to_face_normal[0]*face_normal[0] + camera_to_face_normal[1]*face_normal[1] + camera_to_face_normal[2]*face_normal[2]
		
		return dot_product < 0

	def draw(self, camera):
		if(not self.check_backface(camera.position, self.get_center(), self.normal)):
			return
		
		#Get screen polygon
		screen_points = camera.get_screen_polygon(self.points)
		
		#Proceed if the screen polygon has more than 2 points
		if len(screen_points) > 2:
			#Convert screen points from cartesian to screen coordinates
			converted_points = []
			for point in screen_points:
				converted_points.append(convert_from_cartesian(point, camera.screen.get_size()))
			
			#Draw the face
			camera.faces_drawn += 1
			if self.thickness == None:
				pygame.gfxdraw.filled_polygon(camera.screen, converted_points, self.colour)
			else:
				pygame.draw.polygon(camera.screen, self.colour, converted_points, self.thickness)


#----------Group----------

class Group:
	#Constructor initializes the class
	def __init__(self, objects, origin_point, collision_radius):
		self.objects = objects
		self.origin_point = origin_point
		self.collision_radius = collision_radius

		self.origin_point_copy = self.origin_point

	def reset(self):
		for current_object in self.objects:
			current_object.reset()
		
		self.origin_point = copy.copy(self.origin_point_copy)

	def move(self, offset):
		self.origin_point = (self.origin_point[0]+offset[0], self.origin_point[1]+offset[1], self.origin_point[2]+offset[2])
		for current_object in self.objects:
			current_object.move(offset)

	def rotate(self, offset, origin="self", rotation_axis_angles=(0, 0, 0)):
		if origin == "self":
			for current_object in self.objects:
				current_object.rotate(offset, self.origin_point, rotation_axis_angles)
		else:
			self.origin_point = rotate(self.origin_point, offset, origin, rotation_axis_angles)
			for current_object in self.objects:
				current_object.rotate(offset, origin, rotation_axis_angles)

	def get_cam_distance(self, camera):
		return camera.get_distance(self.origin_point)
	
	def colliding(self, group):
		return math.sqrt((self.origin_point[0] - group.origin_point[0]) ** 2 + (self.origin_point[1] - group.origin_point[1]) ** 2 + (self.origin_point[2] - group.origin_point[2]) ** 2) < (self.collision_radius + group.collision_radius)

	def draw(self, camera):
		def sort_key(current_object):
			return current_object.get_cam_distance(camera)
		
		#Sort group objects
		sorted_objects = sorted(self.objects, key=sort_key, reverse=True)
		
		#Draw the furthest object first and the closest object last
		for i in range(len(sorted_objects)):
			sorted_objects[i].draw(camera)


#----------Scene----------

class Scene:
	#Constructor initializes the class
	def __init__(self):
		self.objects = []
	
	def add_group(self, faces, origin_point, collision_radius):
		self.objects.append(Group(faces, origin_point, collision_radius))

	def add_child(self, parent, child):
		parent.objects.append(self.objects.pop(self.objects.index(child)))
		
	def add_obj(self, file_path, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), colour="random", thickness=None, is_static=True, collision_radius=0):
		points = []
		normals = []

		obj_faces = []
		obj_normals = []
		
		file = open(file_path, "r")
		
		for line in file:
			if line[0:2] == "v ":
				point = line.split()
				calculated_point = [float(point[1])*scale[0], float(point[2])*scale[1], float(point[3])*scale[2]] #Apply scale
				calculated_point = rotate_x(rotate_y(rotate_z(calculated_point, rotation[2]), rotation[1]), rotation[0])
				calculated_point = [calculated_point[0]+position[0], calculated_point[1]+position[1], calculated_point[2]+position[2]] #Apply position
				
				points.append(calculated_point)

			if line[0:3] == "vn ":
				normal = line.split()
				calculated_point = [float(normal[1]), float(normal[2]), float(normal[3])]
				calculated_point = rotate_x(rotate_y(rotate_z(calculated_point, rotation[2]), rotation[1]), rotation[0])
				normals.append(calculated_point)

			elif line[0:2] == "f ":
				seprated = line.split()
				del seprated[0]

				face = []
				face_normals = []

				for i in range(len(seprated)):
					indices = seprated[i].split('/')
					
					if(indices[0] != ""):
						point_index = int(indices[0]) - 1

					if(indices[2] != ""):
						normal_index = int(indices[2]) - 1
					
					face.append(points[point_index])
					
					if(not len(normals)==0):
						face_normals.append(normals[normal_index])
					else:
						face_normals.append((0, 1, 0))
					
				sum_normal = [0, 0, 0]
				for normal in face_normals:
					sum_normal[0] += normal[0]
					sum_normal[1] += normal[1]
					sum_normal[2] += normal[2]

				sum_normal = (sum_normal[0]/3, sum_normal[1]/3, sum_normal[2]/3)

				obj_faces.append(face)
				obj_normals.append(sum_normal)
		
		faces = []

		for i in range(len(obj_faces)):
			if(colour=="random"):
				the_colour = (random.randrange(256), random.randrange(256), random.randrange(256))
			else:
				the_colour = normal_to_euler(obj_normals[i])
				the_colour = list(hsv_to_rgb(colour, 1-((round(abs(max(the_colour))*20)/100)+0.1), (round(abs(max(the_colour))*20)/100)+0.3))
				
				if(the_colour[0]>255):
					the_colour[0] = 255
				if(the_colour[1]>255):
					the_colour[1] = 255
				if(the_colour[2]>255):
					the_colour[2] = 255
			
			faces.append(Face(obj_faces[i], the_colour, obj_normals[i], thickness))
		
		if is_static:
			for face in faces:
				self.objects.append(face)
		else:
			self.add_group(faces, position, collision_radius)
			
			#Pass a reference of the object to the main file
			return self.objects[-1]
	
	def remove_object(self, scene_object):
		self.objects.remove(scene_object)
		
	#----------Main drawing code----------
	#Run every frame
	def draw(self, camera):
		camera.faces_drawn = 0

		#Update camera rotation trig values
		camera.update_trig_values()
		
		def sort_key(current_object):
			#Return the distance of the face from the camera
			return current_object.get_cam_distance(camera)
		
		#Sort all objects
		sorted_objects = sorted(self.objects, reverse=False, key=sort_key)
		
		#Draw the furthest object first and the closest object last
		for current_object in sorted_objects:
			current_object.draw(camera)