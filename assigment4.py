from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math

from matrix4 import Matrix4
from vector import Vector3
from object import Object
from camera import Camera
from scene import Scene
from parser import ObjParser
from utils import print_instructions

camera = Camera()
scene = Scene()
obj = None
wireframe = False

#
# GLOBALS
vertexDim = 3
nVertices = None

# Global variable to represent the compiled shader program, written in GLSL
programID = None

# Global variables for buffer objects
VAO = None

# String containing vertex shader program written in GLSL
with open('vertexShader.glsl', 'r') as fVertexShader:
    strVertexShader = fVertexShader.read()

# String containing fragment shader program written in GLSL
with open('fragmentShader.glsl', 'r') as fFragmentShader:
    strFragmentShader = fFragmentShader.read()

# camera globals
camPosition = Vector3(0.0, 0.0, -3.0)
camUpAxis = Vector3(0.0, 1.0, 0.0)
camNear = 1.0
camFar = 100.0
camAspect = 1.0
camFov = 60.0


def SceneInitiliazer():
    global camera, scenes, obj
    camera.lookAt(camPosition, Vector3(0, 0, 0), camUpAxis)

    parser = ObjParser()
    if len(sys.argv) > 1:
        parser.parse(sys.argv[1])
        obj = Object(parser.vertices, faces=parser.faces, normals=parser.normals, uv=parser.uv,
                     face_normals=parser.faces_normal,
                     face_uvs=parser.faces_uv)

        scene.add_obj_to_scene(obj)
    else:
        exit()


# Function that accepts a list of shaders, compiles them, and returns a handle to the compiled program
def createProgram(shaderList):
    programID = glCreateProgram()

    for shader in shaderList:
        glAttachShader(programID, shader)

    glLinkProgram(programID)

    status = glGetProgramiv(programID, GL_LINK_STATUS)
    if status == GL_FALSE:
        strInfoLog = glGetProgramInfoLog(programID)
        print(b"Linker failure: \n" + strInfoLog)

    # important for cleanup
    for shaderID in shaderList:
        glDetachShader(programID, shaderID)

    return programID


# Function that creates and compiles shaders according to the given type (a GL enum value) and
# shader program (a string containing a GLSL program).
def createShader(shaderType, shaderCode):
    shaderID = glCreateShader(shaderType)
    glShaderSource(shaderID, shaderCode)
    glCompileShader(shaderID)

    status = None
    glGetShaderiv(shaderID, GL_COMPILE_STATUS, status)
    if status == GL_FALSE:
        # Note that getting the error log is much simpler in Python than in C/C++
        # and does not require explicit handling of the string buffer
        strInfoLog = glGetShaderInfoLog(shaderID)
        strShaderType = ""
        if shaderType is GL_VERTEX_SHADER:
            strShaderType = "vertex"
        elif shaderType is GL_GEOMETRY_SHADER:
            strShaderType = "geometry"
        elif shaderType is GL_FRAGMENT_SHADER:
            strShaderType = "fragment"

        print(b"Compilation failure for " + strShaderType + b" shader:\n" + strInfoLog)

    return shaderID


# Initialize the OpenGL environment
def init():
    print_instructions()
    initProgram()
    SceneInitiliazer()


# Set up the list of shaders, and call functions to compile them
def initProgram():
    shaderList = []

    shaderList.append(createShader(GL_VERTEX_SHADER, strVertexShader))
    shaderList.append(createShader(GL_FRAGMENT_SHADER, strFragmentShader))

    global programID
    programID = createProgram(shaderList)

    for shader in shaderList:
        glDeleteShader(shader)


# Called to update the display.
# Because we are using double-buffering, glutSwapBuffers is called at the end
# to write the rendered buffer to the display.
def display():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDepthFunc(GL_LESS)  # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)  # Enables Depth Testing

    global wireframe
    if wireframe is True:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # use our program
    glUseProgram(programID)

    scene.draw_scene(camera.get_view_matrix().to_numpy_array(),
                     Matrix4.getProjMatrix(camNear, camFar, camAspect, camFov)
                     .to_numpy_array(), programID)


# keyboard input handler: exits the program if 'esc' is pressed
def keyPressed(key, x, y):
    global scenes, camera, wireframe

    # If escape is pressed, kill everything.
    # ord() is needed to get the keycode
    if ord(key) == 27:
        # Escape key = 27
        glutLeaveMainLoop()

    elif ord(key) == ord('r'):
        camera.rotate_y_cw()
        camera.calculate()

    elif ord(key) == ord('f'):
        camera.rotate_y_ccw()
        camera.calculate()

    elif ord(key) == ord('e'):
        camera.rotate_x_cw()
        camera.calculate()

    elif ord(key) == ord('q'):
        camera.rotate_x_ccw()
        camera.calculate()

    elif ord(key) == ord('w'):
        camera.move_forward()
        camera.calculate()

    elif ord(key) == ord('s'):
        camera.move_backward()
        camera.calculate()

    elif ord(key) == ord('a'):
        camera.move_left()
        camera.calculate()

    elif ord(key) == ord('d'):
        camera.move_right()
        camera.calculate()

    elif ord(key) == ord('o'):
        scene.objects[0].increase_subdivision()

    elif ord(key) == ord('l'):
        scene.objects[0].decrease_subdivision()

    elif ord(key) == ord('u'):
        # UV MODE ON OFF
        # When UV Mode on, subdivision not possible !!!!
        pass

    elif ord(key) == ord('z'):
        # Reset
        scene.objects[0].set_model_matrix(Matrix4.identity())

    elif ord(key) == ord('p'):
        # Wireframe
        wireframe = not wireframe

    elif ord(key) == ord('m'):
        # Wireframe
        scene.objects[0].rotate_z(math.radians(15))
    elif ord(key) == ord('n'):
        # Wireframe
        scene.objects[0].rotate_z(math.radians(-15))
    display()
    return


def specialKeyPressed(*args):
    global scene
    if args[0] == GLUT_KEY_LEFT:
        scene.objects[0].rotate_y(math.radians(15))
    elif args[0] == GLUT_KEY_RIGHT:
        scene.objects[0].rotate_y(math.radians(-15))
    elif args[0] == GLUT_KEY_UP:
        scene.objects[0].rotate_x(math.radians(15))
    elif args[0] == GLUT_KEY_DOWN:
        scene.objects[0].rotate_x(math.radians(-15))
    display()
    return


# Called whenever the window's size changes (including once when the program starts)
def reshape(w, h):
    glViewport(0, 0, w, h)


# The main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH | GLUT_3_2_CORE_PROFILE)

    width = 500;
    height = 500;
    glutInitWindowSize(width, height)

    glutInitWindowPosition(300, 200)

    window = glutCreateWindow("CENG488 Hello Triangle")

    init()
    glutDisplayFunc(display)
    # glutIdleFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(specialKeyPressed)

    glutMainLoop();


if __name__ == '__main__':
    main()
