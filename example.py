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