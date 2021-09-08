import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import os
import time
from win32api import GetSystemMetrics
from PIL import Image

def line_animation(x,y):
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glTranslatef(0, y, 0)
    glColor3f(1 ,1, 1)
    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex3f(-x ,0.0 , 0.0)
    glVertex3f(x, 0.0 ,0.0)
    glEnd()
    glPopMatrix()
    glFlush()
def main():
    # initializing glfw library
    pygame.init()
 
    fps = 60
    fpsClock = pygame.time.Clock()
    
    width , height = [int(GetSystemMetrics(i)) for i in range(2)]
    scale = 0.75
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Derpo 0.0.0c')
    screen = pygame.display.set_mode((int(800*scale), int(800*scale)),DOUBLEBUF|OPENGL)
    os.environ["SDL_VIDEO_CENTERED"]= '1'
    glClearColor(15/255, 32/255, 43/255, 1)
    # Game loop.
    run = True
    x= 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        glClear(GL_COLOR_BUFFER_BIT)
        if x >= 0.5: 
            x += 0.1
            if x >=0.8:
                x = 0.8
                glPointSize(25)
                glBegin(GL_POINTS)
                glVertex3f(0, 0, 0)
                glEnd()
        else:
            x += 0.02
        y = x
        line_animation(x,y)
        glRotatef(180,0.5,.5,0)
        line_animation(x,-y)
        line_animation(x,y)
        glRotatef(180,0.5,.5,0)
        line_animation(x,-y)
        glFlush()
        pygame.display.flip()
        fpsClock.tick(fps)
    sys.exit()
    
    # Update.
    
    # Draw.
    


if __name__ == "__main__":
    main()