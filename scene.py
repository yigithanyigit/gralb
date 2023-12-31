from typing import List

from OpenGL.GL import *
from OpenGL.GLUT import *

from object import Object
from light import BaseLight, PointLight


class Scene:
    def __init__(self, lights:List[BaseLight] = None, objects: List[Object] = None):
        if objects is None:
            self.objects = []
        else:
            self.objects = objects

        if lights is None:
            self.lights = []
        else:
            self.lights = lights

        self.frame = 0
        self.frame_limit = 144

    def selected_objects(self):
        pass

    def add_obj_to_scene(self, obj):
        self.objects.append(obj)

    def add_light_to_scene(self, light):
        self.lights.append(light)

    # Not works in Core Profile
    """
    def draw_scene(self, camera=None):
        for obj in self.objects:
            obj.draw(camera)
    """

    # Naive Approach
    def reset_frame(self):
        if self.frame % self.frame_limit == 0:
            self.frame = 0

    def increase_frame(self):
        self.frame += 1
        self.reset_frame()

    def display(self, model, view, proj, programID, obj):

        glUseProgram(programID)
        # get matrices and bind them to vertex shader locations
        modelLocation = glGetUniformLocation(programID, "model")
        glUniformMatrix4fv(modelLocation, 1, GL_FALSE, model)
        viewLocation = glGetUniformLocation(programID, "view")
        glUniformMatrix4fv(viewLocation, 1, GL_FALSE, view)
        projLocation = glGetUniformLocation(programID, "proj")
        glUniformMatrix4fv(projLocation, 1, GL_FALSE, proj)

        obj.draw()

        for light in self.lights:
            light.set_program_id(programID)
            light.set_light_uniforms()
            if isinstance(light, PointLight) is True and light.animation is not None:
                self.frame_limit = 1200
                light.cyclical_move_by_frame(self.frame, 50)

        self.increase_frame()
        glutSwapBuffers()
        glUseProgram(0)

    def draw_scene(self, view, proj):
        for obj in self.objects:
            self.display(obj.get_model_matrix().to_numpy_array(), view, proj, obj.program.id, obj)
