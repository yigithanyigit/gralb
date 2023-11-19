# This is a sample Python script.
# CENG487 Introduction To Computer Graphics
# Development Env Test Program
# Runs in python 3.x env
# with PyOpenGL and PyOpenGL-accelerate packages

# CENG 487 Assignment 1 by Yigithan Yigit
# Erdem Taylan # StudentId: 310201112
# 10/23

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from timeit import default_timer as timer
import time
from matrix4 import Matrix4
from vector import Vector3
from object import Object, Cube, Pyramid, Square, Cylinder, Sphere
from camera import Camera

# Number of the glut window.
window = 0

# Rotation angle for the triangle.
rtri = 0.0

# Rotation angle for the quadrilateral.
rquad = 0.0

fps = 60


camera = Camera()
camera.lookAt(Vector3(0, 0, -8), Vector3(0, 0, 0), Vector3(0, 1, 0))

obj_index = 0
obj_list = [Square(), Cube(), Cylinder(), Sphere()]
obj = Square()


def print_instructions():
    print("Instructions:")
    print("'m': Switch to the next object")
    print("'n': Switch to the previous object")
    print("'r': Rotate camera clockwise around the y-axis")
    print("'f': Rotate camera counterclockwise around the y-axis")
    print("'e': Rotate camera clockwise around the x-axis")
    print("'q': Rotate camera counterclockwise around the x-axis")
    print("'w': Move camera forward")
    print("'s': Move camera backward")
    print("'a': Move camera left")
    print("'d': Move camera right")
    print("'o': Increase subdivision level for the current object")
    print("'l': Decrease subdivision level for the current object")
    print("Press 'Esc' to exit the program.")

# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):  # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)  # This Will Clear The Background Color To Black
    glClearDepth(1.0)  # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)  # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)  # Enables Depth Testing
    glShadeModel(GL_SMOOTH)  # Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Reset The Projection Matrix4
    # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)

    print_instructions()

    glMatrixMode(GL_MODELVIEW)


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:  # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)  # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


# The main drawing function.
def DrawGLScene():
    start = timer()

    global rtri, rquad

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);  # Clear The Screen And The Depth Buffer

    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

    obj_list[obj_index].draw(camera)

    rtri = rtri + 0.01  # Increase The Rotation Variable For The Triangle

    #  since this is double buffered, swap the buffers to display what just got drawn.

    glutSwapBuffers()
    end = timer()
    render_time = end - start
    #print(f"FPS: {(100 / render_time)}")


# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(key, x, y):
    global obj_index


    # If escape is pressed, kill everything.
    # ord() is needed to get the keycode
    if ord(key) == 27:
        # Escape key = 27
        glutDestroyWindow(window)
        return

    if ord(key) == ord('m'):

        if obj_index + 1 < len(obj_list):
            obj_index += 1
        return

    if ord(key) == ord('n'):

        if obj_index - 1 >= 0:
            obj_index -= 1
        return


    if ord(key) == ord('r'):
        camera.rotate_y_cw()
        camera.calculate()
        return

    if ord(key) == ord('f'):
        camera.rotate_y_ccw()
        camera.calculate()
        return

    if ord(key) == ord('e'):
        camera.rotate_x_cw()
        camera.calculate()
        return

    if ord(key) == ord('q'):
        camera.rotate_x_ccw()
        camera.calculate()
        return

    if ord(key) == ord('w'):
        camera.move_forward()
        camera.calculate()
        return

    if ord(key) == ord('s'):
        camera.move_backward()
        camera.calculate()
        return

    if ord(key) == ord('a'):
        camera.move_left()
        camera.calculate()
        return

    if ord(key) == ord('d'):
        camera.move_right()
        camera.calculate()
        return

    if ord(key) == ord('o'):
        obj_list[obj_index].increase_subdivision()
        return

    if ord(key) == ord('l'):
        obj_list[obj_index].decrease_subdivision()
        return






def main():
    global window
    glutInit(sys.argv)

    # Select type of Display mode:
    #  Double buffer
    #  RGBA color
    #  Alpha components supported
    #  Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # get a 640 x 480 window
    glutInitWindowSize(640, 480)

    # the window starts at the upper left corner of the screen
    glutInitWindowPosition(0, 0)

    # Okay, like the C version we retain the window id to use when closing, but for those of you new
    # to Python (like myself), remember this assignment would make the variable local and not global
    # if it weren't for the global declaration at the start of main.
    window = glutCreateWindow("CENG487 Development Env Test")

    # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
    # set the function pointer and invoke a function to actually register the callback, otherwise it
    # would be very much like the C version of the code.
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    # glutFullScreen()

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)

    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc(keyPressed)

    # Initialize our window.
    InitGL(640, 480)

    # Start Event Processing Engine
    glutMainLoop()


# Print message to console, and kick off the main to get it rolling.
print("Hit ESC key to quit.")
main()
