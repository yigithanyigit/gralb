from OpenGL.GL import *
from OpenGL.GLUT import *
from typing import List
from object import Object
from shader import Shader




class Scene:
    def __init__(self, objects: List[Object] = None):
        if objects is None:
            self.objects = []
        else:
            self.objects = objects



    def add_obj_to_scene(self, obj):
        self.objects.append(obj)

    # Not works in Core Profile
    """
    def draw_scene(self, camera=None):
        for obj in self.objects:
            obj.draw(camera)
    """

    def display(self, model, view, proj, programID, obj):

        # get matrices and bind them to vertex shader locations
        modelLocation = glGetUniformLocation(programID, "model")
        glUniformMatrix4fv(modelLocation, 1, GL_FALSE, model)
        viewLocation = glGetUniformLocation(programID, "view")
        glUniformMatrix4fv(viewLocation, 1, GL_FALSE, view)
        projLocation = glGetUniformLocation(programID, "proj")
        glUniformMatrix4fv(projLocation, 1, GL_FALSE, proj)

        obj.draw()

        glutSwapBuffers()

    def draw_scene(self, view, proj, programID):
        for obj in self.objects:
            self.display(obj.model.to_numpy_array(), view, proj, programID, obj)
