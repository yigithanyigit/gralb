from OpenGL.GL import *

from utils import BaseSingletonList


class ProgramList(BaseSingletonList):
    def __init__(self):
        super().__init__()


class Program:
    def __init__(self, shader_list: tuple):

        if ProgramList().check(shader_list) is True:
            self.id = ProgramList().get_from_value(shader_list)
            return

        self.id = glCreateProgram()
        self.shader_list = shader_list

        self.attach_shaders()

        glLinkProgram(self.id)

        status = glGetProgramiv(self.id, GL_LINK_STATUS)
        if status == GL_FALSE:
            strInfoLog = glGetProgramInfoLog(self.id)
            print(b"Linker failure: \n" + strInfoLog)

        self.detach_shaders()

        ProgramList().add_to_data(self.id, self.shader_list)

        self.delete_shaders()

    def attach_shaders(self):
        for shader in self.shader_list:
            glAttachShader(self.id, shader)

    def detach_shaders(self):
        for shader in self.shader_list:
            glDetachShader(self.id, shader)

    def delete_shaders(self):
        for shader in self.shader_list:
            glDeleteShader(shader)
