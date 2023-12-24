import math

from OpenGL.GL import *
from OpenGL.GLUT import *

from camera import Camera
from matrix4 import Matrix4
from object import Object
from parser import ObjParser
from program import Program
from scene import Scene
from shader import ShaderList
from texture import Texture
from utils import print_instructions
from vector import Vector3

camera = Camera()
scene = Scene()
obj = None

# Texture filepaths
textureList = ['textures/texture1.png', 'textures/texture2.png']

#
# GLOBALS
vertexDim = 3
nVertices = None

# Global variable to represent the compiled shader program, written in GLSL
programID = None

# Global variables for buffer objects
VAO = None

# Shader List
shaderList = ShaderList()

# Blend factor
blendFactor = 0.5

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
        obj = Object(parser.vertices, vertex_shader_file='shaders/vertexShader.glsl',
                     fragment_shader_file='shaders/fragmentShader.glsl', faces=parser.faces, normals=parser.normals,
                     uv=parser.uv, face_normals=parser.faces_normal, face_uvs=parser.faces_uv)

        scene.add_obj_to_scene(obj)
    else:
        print("Expected .obj arugment")
        exit()


# Initialize the OpenGL environment
def init():
    print_instructions()
    SceneInitiliazer()
    initProgram()
    initTextures(textureList)


# texture stuff
def initTextures(texFilePath):
    # we need to bind to the program to set texture related params
    global programID
    glUseProgram(programID)

    for idx, file_path in enumerate(texFilePath):
        # set shader stuff
        tex = Texture(file_path)
        texID = tex.id
        glUseProgram(programID)
        texLocation = glGetUniformLocation(programID, f"tex{texID}")

        # now activate texture units
        glActiveTexture(GL_TEXTURE0 + texID)
        glBindTexture(GL_TEXTURE_2D, texID)
        glUniform1i(texLocation, idx)
        # reset program
        glUseProgram(0)


def changeBlendFactor():
    global blendFactor, programID
    glUseProgram(programID)
    blendFactorLocation = glGetUniformLocation(programID, "blendFactor")
    glUniform1f(blendFactorLocation, blendFactor)
    glUseProgram(0)


# Set up the list of shaders, and call functions to compile them
def initProgram():
    global programID
    program = Program(shaderList.data)
    programID = program.id


# Called to update the display.
# Because we are using double-buffering, glutSwapBuffers is called at the end
# to write the rendered buffer to the display.
def display():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDepthFunc(GL_LESS)  # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)  # Enables Depth Testing

    camera.render_wireframe()

    # use our program
    glUseProgram(programID)

    scene.draw_scene(camera.get_view_matrix().to_numpy_array(),
                     Matrix4.getProjMatrix(camNear, camFar, camAspect, camFov).to_numpy_array(), programID)


# keyboard input handler: exits the program if 'esc' is pressed
def keyPressed(key, x, y):
    global scenes, camera, wireframe, blendFactor

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

    elif ord(key) == ord('z'):
        # Reset
        scene.objects[0].set_model_matrix(Matrix4.identity())

    elif ord(key) == ord('p'):
        # Wireframe
        camera.toggle_wireframe()

    elif ord(key) == ord('m'):
        scene.objects[0].rotate_z(math.radians(15))

    elif ord(key) == ord('n'):
        scene.objects[0].rotate_z(math.radians(-15))

    elif ord(key) == ord('b'):
        blendFactor = min(1.0, blendFactor + 0.1)
        changeBlendFactor()

    elif ord(key) == ord('v'):
        blendFactor = max(0.0, blendFactor - 0.1)
        changeBlendFactor()

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

    window = glutCreateWindow("OpenGL Renderer")

    init()
    glutDisplayFunc(display)
    # glutIdleFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(specialKeyPressed)
    glutSpecialFunc(specialKeyPressed)

    glutMainLoop()


if __name__ == '__main__':
    main()
