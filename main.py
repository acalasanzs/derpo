import glfw
from OpenGL.GL import *
import OpenGL_accelerate
import os
from win32api import GetSystemMetrics
from PIL import Image

def main():
    # initializing glfw library
    if not glfw.init():
        raise Exception("glfw can not be initialized")

    scale = 0.75
    os.environ["SDL_VIDEO_CENTERED"]= '1'

    black, white = (5, 6, 6), (230, 230, 230)

    width , height = [int(GetSystemMetrics(i)) for i in range(2)]

    win = glfw.create_window(int(width*scale),int(height*scale),"Derpo 0.0.0a",None,None)

    if not win:
        glfw.terminate()
        raise Exception("glfw window can not be created")
    # set pos at center
    glfw.set_window_pos(win,int(width//2-(width*scale)/2),int(height//2-(height*scale)/2))

    # make the context current

    glfw.make_context_current(win)
    
    glClearColor(15/255, 32/255, 43/255, 1)

    # set icon
    icon = Image.open("icon.ico")
    glfw.set_window_icon(win, 1 ,icon)
    # main loop
    while not glfw.window_should_close(win):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        glfw.swap_buffers(win)
        
    glfw.terminate()
if __name__ == "__main__":
    main()