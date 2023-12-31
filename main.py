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
from light import DirectionalLight, SpotLight, PointLight

camera = Camera()
scene = Scene()

# Texture filepaths
textureList = ['textures/img.png']

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
    global camera, scenes
    camera.lookAt(camPosition, Vector3(0, 0, 0), camUpAxis)

    parser = ObjParser()
    if len(sys.argv) > 1:
        parser.parse(sys.argv[1])
        obj_attr = parser.get_attribute_list()

        """
        obj = Object(attr.vertices, vertex_shader_file='vertexShader.glsl',
                     fragment_shader_file='fragmentShader.glsl', faces=attr.faces, normals=attr.normals,
                     uv=attr.uv, face_normals=attr.faces_normal, face_uvs=attr.faces_uv)
        """
        #obj = Object.create_from_obj_attributes(attr, 'vertexShader.glsl', fragment_shader='fragmentShader.glsl')
        for o in obj_attr:
            obj = Object.create_from_obj_attributes(o, 'shaders/vertexShaderBlinn-Phong.glsl',
                                                    fragment_shader='shaders/fragmentShaderLight.glsl', texture=textureList)
            scene.add_obj_to_scene(obj)
    else:
        print("Expected .obj arugment")
        exit()

    point_light = PointLight(lightPosition=[-3.0, 0.0, -3.0], lightColor=[1.0, 1.0, 1.0])
    directional_light = DirectionalLight(lightDir=[0.0, 0.0, 1.0], lightColor=[1.0, 1.0, 1.0])
    spot_light = SpotLight(lightPosition=[0.0, 100.0, -100.0], lightDir=[0.0, -1.0, 1.0], lightColor=[1.0, 1.0, 1.0],
                           cutoff=70.0)

    scene.add_light_to_scene(point_light)
    scene.add_light_to_scene(directional_light)
    scene.add_light_to_scene(spot_light)

    point_light.set_uniform("pointLight")
    directional_light.set_uniform("directionalLight")
    spot_light.set_uniform("spotLight")

# Initialize the OpenGL environment
def init():
    global programID
    print_instructions()
    SceneInitiliazer()

def changeBlendFactor():
    global blendFactor, programID
    glUseProgram(programID)
    blendFactorLocation = glGetUniformLocation(programID, "blendFactor")
    glUniform1f(blendFactorLocation, blendFactor)
    glUseProgram(0)

# Called to update the display.
# Because we are using double-buffering, glutSwapBuffers is called at the end
# to write the rendered buffer to the display.
def display():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDepthFunc(GL_LESS)  # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)  # Enables Depth Testing
    camera.render_wireframe()

    scene.draw_scene(camera.get_view_matrix().to_numpy_array(),
                      Matrix4.getProjMatrix(camNear, camFar, camAspect, camFov).to_numpy_array())



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

    elif ord(key) == ord('v'):
        for light in scene.lights:
            if isinstance(light, PointLight):
                if light.animation is None:
                    light.animation = PointLight.cyclical_move_by_frame
                else:
                    light.animation = None

    elif ord(key) == ord('b'):
        for obj in scene.objects:
            obj.toggle_blinn_phong()


    elif ord(key) == ord('1'):
        for light in scene.lights:
            if isinstance(light, PointLight):
                light.toggle()

    elif ord(key) == ord('2'):
        for light in scene.lights:
            if isinstance(light, DirectionalLight):
                light.toggle()

    elif ord(key) == ord('3'):
        for light in scene.lights:
            if isinstance(light, SpotLight):
                light.toggle()

    """
    elif ord(key) == ord('b'):
        blendFactor = min(1.0, blendFactor + 0.1)
        changeBlendFactor()

    elif ord(key) == ord('v'):
        blendFactor = max(0.0, blendFactor - 0.1)
        changeBlendFactor()
    """

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

    width = 720;
    height = 720;
    glutInitWindowSize(width, height)

    glutInitWindowPosition(300, 200)

    window = glutCreateWindow("OpenGL Renderer")

    init()
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(specialKeyPressed)

    glutMainLoop()


if __name__ == '__main__':
    main()
