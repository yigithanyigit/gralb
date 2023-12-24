from typing import List

from OpenGL.GL import *
from OpenGL.GLUT import *

from object import Object


class Scene:
    def __init__(self, objects: List[Object] = None):
        if objects is None:
            self.objects = []
        else:
            self.objects = objects

    def selected_objects(self):
        pass

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
            self.display(obj.get_model_matrix().to_numpy_array(), view, proj, programID, obj)
