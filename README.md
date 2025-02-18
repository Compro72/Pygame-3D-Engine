# 2024 - 2025
# pygame3D Documentation

----------------------------------------------------------------------------------------------------

## `Scene` Class

The `Scene` class is a high level class that consists of a collection of objects. The class provides methods to add, remove, and render objects in the scene.

### Constructor

#### `__init__()`
Initializes a new `Scene` instance with an empty list of objects.

### Methods

#### `add_group(faces, origin_point, collision_radius)`
- **Purpose:** Adds a group class containing the specified faces of to the scene at the specified origin point.
- **Parameters:**
	- `faces`: List of faces to be added.
	- `origin_point`: The origin point for the group.

#### `add_child(parent, child)`
- **Purpose:** Removes a group from the scene and adds it to a parent group.
- **Parameters:**
	- `parent`: The parent group to which the child group will be added.
	- `child`: The child group to be added to the parent group.

#### `add_obj(file_path, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), colour="random", thickness=None, is_static=True, collision_radius=0)`
- **Purpose:** Loads an OBJ file and adds its contents to the scene given the specified parameters.
- **Parameters:**
	- `file_path`: Path to the OBJ file to be loaded.
	- `position`: Tuple representing the (x, y, z) position to place the group. Default is (0, 0, 0).
	- `rotation`: Tuple representing the (x, y, z) rotation angles in radians. Default is (0, 0, 0).
	- `scale`: Tuple representing the scaling factors for the x, y, and z axes. Default is (1, 1, 1).
	- `colour`: Colour of the group. Can be "random" or a number between 0 and 1. Default is "random".
	- `thickness`: Thickness of the groups's faces. Can be None for filling faces. Default is None.
	- `is_static`: Boolean indicating whether the object is static. Default is True.
	- `collision_radius`: Radius of the group's collision sphere. Default is 0.
- **Returns:** If `is_static` is False, returns a reference to the added group.

#### `remove_object(scene_object)`
- **Purpose:** Removes a group from the scene.
- **Parameters:**
	- `scene_object`: The group to be removed from the scene.

#### `draw(camera)`
- **Purpose:** Draws the scene using the specified camera.
- **Parameters:**
	- `camera`: The camera class used to render the scene.


----------------------------------------------------------------------------------------------------


## `Camera` Class

The `Camera` class represents a camera in 3D space. Used for viewing and projecting 3D objects onto a 2D screen.

### Constructor

#### `__init__(screen, position=(0, 0, 0), rotation_x=0, rotation_y=0, near_plane=0.1, view_factor=400)`
Initializes a new `Camera` instance.
- **Parameters:**
	- `screen`: The pygame screen on which the camera projects the scene.
	- `position`: Tuple representing the (x, y, z) position of the camera. Default is (0, 0, 0).
	- `rotation_x`: Rotation around the x-axis. Default is 0.
	- `rotation_y`: Rotation around the y-axis. Default is 0.
	- `near_plane`: Distance of the near clipping plane. Default is 0.1.
	- `view_factor`: Factor used for projection calculations. Higher value means lower FOV. Default is 400.

### Methods

#### `update_trig_values()`
- **Purpose:** Updates the trigonometric values for the camera's rotation angles.

#### `get_distance(point)`
- **Purpose:** Calculates the distance from the camera to the given point.
- **Parameters:**
	- `point`: The point to which the distance is calculated.
- **Returns:** The distance between the camera and the point.

#### `clip_2D_polygon(polygon)`
- **Purpose:** Clips a 2D polygon to fit within the screen boundaries.
- **Parameters:**
	- `polygon`: The 2D polygon to be clipped given as an array of 2D points.
- **Returns:** The clipped 2D polygon.

#### `get_screen_polygon(face)`
- **Purpose:** Projects a 3D face onto the 2D screen and clips it to fit within the screen boundaries.
- **Parameters:**
	- `face`: The 3D face to be projected.
- **Returns:** The projected and clipped 2D polygon.

#### `move(offset)`
- **Purpose:** Moves the camera by the given offset.
- **Parameters:**
	- `offset`: Tuple representing the (x, y, z) offset.

#### `rotate(rot_x, rot_y)`
- **Purpose:** Rotates the camera around the x and y axes.
- **Parameters:**
	- `rot_x`: Rotation around the x-axis.
	- `rot_y`: Rotation around the y-axis.


----------------------------------------------------------------------------------------------------


## `Group` Class

The `Group` class is a collection of objects that can be transformed and rendered together.

### Constructor

#### `__init__(objects, origin_point, collision_radius)`
Initializes a new `Group` instance.
- **Parameters:**
	- `objects`: List of objects to be grouped.
	- `origin_point`: Origin point of the group.

### Methods

#### `reset()`
- **Purpose:** Resets all objects in the group to their original transformations.

#### `move(offset)`
- **Purpose:** Moves the entire group by the given offset.
- **Parameters:**
	- `offset`: Tuple representing the (x, y, z) offset.

#### `rotate(offset, origin="self", rotation_axis_angles=(0, 0, 0))`
- **Purpose:** Rotates the group around the given origin.
- **Parameters:**
	- `offset`: Tuple representing the (x, y, z) rotation offset in radians. XYZ order.
	- `origin`: Origin of rotation. Default is "self".
	- `rotation_axis_angles`: Rotation angles of the local coordinate system.

#### `get_cam_distance(camera)`
- **Purpose:** Calculates the distance from the specified camera to the group's origin.
- **Parameters:**
	- `camera`: Camera class to calculate the distance from.
- **Returns:** The distance from the camera to the group's origin.

#### `colliding(group)`
- **Purpose** Checks if two collision spheres are colliding.
- **Parameters:**
	- `group`: Group class to check the collision with.
- **Returns:** Boolean value indicating if the groups are colliding.

#### `draw(camera)`
- **Purpose:** Draws all objects in the group using the specified camera.
- **Parameters:**
	- `camera`: Camera class used to render the group.


----------------------------------------------------------------------------------------------------


## `Face` Class

The `Face` class is a low level class that represents a face in 3D space. It includes methods for transforming and rendering the face.

### Constructor

#### `__init__(face_points, colour, normal, thickness=None)`
Initializes a new `Face` instance.
- **Parameters:**
	- `face_points`: List of points defining the face.
	- `colour`: Colour of the face.
	- `normal`: Normal vector of the face.
	- `thickness`: Thickness of the face. Can be None for filling faces. Default is None.

### Methods

#### `reset()`
- **Purpose:** Reloads the original transformations of the face.

#### `move(offset)`
- **Purpose:** Moves the face by the given offset.
- **Parameters:**
	- `offset`: Tuple representing the (x, y, z) offset.

#### `rotate(offset, origin="self", rotation_axis_angles=(0, 0, 0))`
- **Purpose:** Rotates the face around the given origin.
- **Parameters:**
	- `offset`: Tuple representing the (x, y, z) rotation offset in radians. XYZ order.
	- `origin`: Origin of rotation. Default is "self".
	- `rotation_axis_angles`: Rotation angles of the local coordinate system.

#### `get_center()`
- **Purpose:** Calculates the center point of the face.
- **Returns:** The center of the face.

#### `get_cam_distance(camera)`
- **Purpose:** Calculates the distance from the specified camera to the face center.
- **Parameters:**
	- `camera`: Camera class to calculate the distance from.
- **Returns:** The distance from the camera to the face center.

#### `check_backface(camera_pos, face_point, face_normal)`
- **Purpose:** Checks if the face is pointing towards the camera.
- **Parameters:**
	- `camera_pos`: Camera position.
	- `face_point`: A point on the face.
	- `face_normal`: Normal vector of the face.
- **Returns:** True if the face is pointing towards the camera.

#### `draw(camera)`
- **Purpose:** Draws the face using the specified camera.
- **Parameters:**
	- `camera`: Camera class used to render the face.


----------------------------------------------------------------------------------------------------


## Utility Functions

### `hsv_to_rgb(hue, saturation, value)`
- **Purpose:** Converts HSV to RGB.
- **Parameters:**
	- `hue`: Hue (0-1).
	- `saturation`: Saturation (0-1).
	- `value`: Value (0-1).
- **Returns:** Tuple representing (red, green, blue).

### `rotate_x(point, angle, origin=(0, 0, 0))`
- **Purpose:** Rotates a point around the x-axis.
- **Parameters:**
	- `point`: The point to rotate.
	- `angle`: Rotation angle in radians.
	- `origin`: The origin point for the rotation. Default is (0, 0, 0).
- **Returns:** The new rotated point.

### `rotate_y(point, angle, origin=(0, 0, 0))`
- **Purpose:** Rotates a point around the y-axis.
- **Parameters:**
	- `point`: The point to rotate.
	- `angle`: Rotation angle in radians.
	- `origin`: The origin point for the rotation. Default is (0, 0, 0).
- **Returns:** The new rotated point.

### `rotate_z(point, angle, origin=(0, 0, 0))`
- **Purpose:** Rotates a point around the z-axis.
- **Parameters:**
	- `point`: The point to rotate.
	- `angle`: Rotation angle in radians.
	- `origin`: The origin point for the rotation. Default is (0, 0, 0).
- **Returns:** The new rotated point.

### `rotate(point, angles, origin=(0, 0, 0), rotation_axis_angles=(0, 0, 0))`
- **Purpose:** Rotates a point.
- **Parameters:**
	- `point`: The point to rotate.
	- `angles`: The (x, y, z) rotation angles in radians.
	- `origin`: The origin point for the rotation. Default is (0, 0, 0).
	- `rotation_axis_angles`: Rotation angles of the local coordinate system.
- **Returns:** The new rotated point.

### `convert_from_cartesian(point, screen_size)`
- **Purpose:** Calculates the screen coordinate for the given 2D cartesian coordinate.
- **Parameters:**
	- `point`: The (x, y) cartesian point to convert.
	- `screen_size`: The (x, y) size of the screen.
- **Returns:** The (x, y) screen point.


----------------------------------------------------------------------------------------------------


## Example
### In this example we should see a randomly coloured cube rotating in front of the camera.`
```
#Import libraries
import pygame
from pygame3D import *

#Initialize pygame
pygame.init()
size = (800, 500)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False

#Initialize pygame3D
myScene = Scene()
myCamera = Camera(screen, position=(0, 0, -500))

#Add a cube to the scene
cube = myScene.add_obj("cube.obj", position=(0, 0, 0), scale=(100, 100, 100), is_static=False)

#Loop
while not done:
    #Rotate your cube
    cube.rotate(offset=(0, 0.01, 0.01))

    #Draw the frame
    screen.fill((0, 0, 0))
    myScene.draw(myCamera)

    #Update the frame
    pygame.display.flip()

    #Framerate
    clock.tick(60)

    #Exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

pygame.quit()
```
