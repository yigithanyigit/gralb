import typing
from vector import Vector4, Vector3
from OpenGL.GL import *
import numpy


class BaseLight:
    def __init__(self, programID = None):
        self.type = None
        self.program_id = programID
        self.uniform_name = None
        self.enabled = False

    def set_uniform(self, uniform_name):
        self.uniform_name = uniform_name

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def toggle(self):

        self.enabled = not self.enabled

    def set_program_id(self, programID):
        self.program_id = programID

    def set_light_uniforms(self):
        pass

    def use_program(self):
        glUseProgram(self.program_id)

    def reset_program(self):
        glUseProgram(0)


class DirectionalLight(BaseLight):
    def __init__(self, lightDir: Vector4, lightColor: Vector4, programID = None):
        super().__init__(programID)
        self.type = 1
        self.light_dir = lightDir
        self.light_color = lightColor

    def set_light_uniforms(self):
        self.use_program()
        glUniform3fv(glGetUniformLocation(self.program_id, f"{self.uniform_name}.direction"), 1, self.light_dir)
        glUniform3fv(glGetUniformLocation(self.program_id, f"{self.uniform_name}.color"), 1, self.light_color)
        glUniform1i(glGetUniformLocation(self.program_id, f"{self.uniform_name}.enabled"), self.enabled)
        self.reset_program()


class PointLight(BaseLight):
    def __init__(self, lightPosition: Vector3,  lightColor: Vector4, programID = None,):
        super().__init__(programID)
        self.type = 0
        self.light_position = lightPosition
        self.light_color = lightColor

        self.animation = None

        self.constant = 1.0
        self.linear = 0.09
        self.quadratic = 0.032

    def set_light_uniforms(self):
        self.use_program()
        glUniform3fv(glGetUniformLocation(self.program_id, f"{self.uniform_name}.position"), 1, self.light_position)
        glUniform3fv(glGetUniformLocation(self.program_id, f"{self.uniform_name}.color"), 1, self.light_color)
        glUniform1f(glGetUniformLocation(self.program_id, f"{self.uniform_name}.constant"),  self.constant)
        glUniform1f(glGetUniformLocation(self.program_id, f"{self.uniform_name}.linear"),  self.linear)
        glUniform1f(glGetUniformLocation(self.program_id, f"{self.uniform_name}.quadratic"), self.quadratic)
        glUniform1i(glGetUniformLocation(self.program_id, f"{self.uniform_name}.enabled"), self.enabled)
        self.reset_program()

    def cyclical_move_by_frame(self, frame, total_frame):

        radius = numpy.linalg.norm(self.light_position[0:3])
        delta = numpy.pi * 2 * frame / total_frame
        self.light_position[2] = radius * numpy.sin(delta)
        self.light_position[0] = radius * numpy.cos(delta)
        #print(numpy.sin(delta), numpy.cos(delta), delta, numpy.deg2rad(delta))
        #print(self.light_position)



class SpotLight(BaseLight):
    def __init__(self,lightPosition: Vector3, lightDir: Vector4, lightColor: Vector4, cutoff: float, programID = None):
        super().__init__(programID)
        self.type = 2
        self.light_position = lightPosition
        self.light_dir = lightDir
        self.light_color = lightColor
        self.cutoff = cutoff

    def set_light_uniforms(self):
        self.use_program()
        glUniform3fv(glGetUniformLocation(self.program_id, f"{self.uniform_name}.position"), 1, self.light_position)
        glUniform3fv(glGetUniformLocation(self.program_id, f"{self.uniform_name}.direction"), 1, self.light_dir)
        glUniform3fv(glGetUniformLocation(self.program_id, f"{self.uniform_name}.color"), 1, self.light_color)
        glUniform1f(glGetUniformLocation(self.program_id, f"{self.uniform_name}.cutoff"), numpy.cos(numpy.radians(self.cutoff)))
        glUniform1i(glGetUniformLocation(self.program_id, f"{self.uniform_name}.enabled"), self.enabled)
        self.reset_program()