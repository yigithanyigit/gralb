import numpy
from OpenGL.GL import *
from OpenGL.GLUT import *

from definitions import Definitions
from utils import BaseSingletonList


class ShaderList(BaseSingletonList):
    def __init__(self):
        super().__init__()

    @staticmethod
    # Function that creates and compiles shaders according to the given type (a GL enum value) and
    # shader program (a string containing a GLSL program).
    def createShaderStatic(shaderType, shaderCode):
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

    # Function that creates and compiles shaders according to the given type (a GL enum value) and
    # shader program (a string containing a GLSL program).
    def createShader(self, shaderType, shaderCode):
        if hash(shaderCode) in self.data_dict:
            return self.data_dict[hash(shaderCode)]

        shaderID = ShaderList.createShaderStatic(shaderType, shaderCode)

        self.data.append(shaderID)
        self.data_dict[hash(shaderCode)] = shaderID

        return shaderID


class Shader:
    def __init__(self, obj, vertex_shader_precompiled, fragment_shader_precompiled):
        self.VBO = None
        self.VAO = None
        self.VBOData = None
        self.nVertices = 0
        self.vertexDim = Definitions.Vector3Dimension

        self.vertex_shader_precompiled = vertex_shader_precompiled
        self.fragment_shader_precompiled = fragment_shader_precompiled

        self.vertex_shader_idx = ShaderList().createShader(GL_VERTEX_SHADER, self.vertex_shader_precompiled)
        self.fragment_shader_idx = ShaderList().createShader(GL_FRAGMENT_SHADER, self.fragment_shader_precompiled)

        """
        self.shader_list = []
        self.shader_files = self.open_shader_files()
        self.shader_list.append(self.createShader(GL_VERTEX_SHADER, self.shader_files[0]))
        self.shader_list.append(self.createShader(GL_FRAGMENT_SHADER, self.shader_files[1]))
        """

        self.obj = obj
        self.initVertexBufferData()
        self.initVertexBuffer()

    def initVertexBufferData(self):

        finalVertexPositions = []
        finalVertexColors = []
        finalVertexUvs = []

        self.nVertices = 0
        for idx, face in enumerate(self.obj.faces):
            self.nVertices += len(face)
            finalVertexColors.extend(self.obj.colors[idx].elements * len(face))
            for v_idx in face:
                finalVertexPositions.extend(self.obj.vertices[v_idx])
        # Full Object Mapping
        """
        for idx, uv in enumerate(self.obj.face_uvs):
            for v_idx in uv:
                finalVertexUvs.extend(self.obj.uv[v_idx])
        """
        # Per face mapping
        flag = False
        for face in self.obj.faces:
            if flag is False:
                finalVertexUvs.extend([1.0, 1.0, 0.0, 1.0, 0.0, 0.0, ])
            else:
                finalVertexUvs.extend([1.0, 1.0, 0.0, 0.0, 1.0, 0.0, ])
            flag = not flag

        """   
        # go over faces and assemble an array for all vertex data
        faceID = 0
        for face in faces:
            for vertex in face:
                finalVertexPositions.extend(vertexPositions[vertex])
                finalVertexColors.extend(faceColors[faceID])
                finalVertexUvs.extend(vertexUVs[vertex])
            faceID += 1

        self.self.VBOData = numpy.array(finalVertexPositions + finalVertexColors + finalVertexUvs, dtype='float32')
        """

        self.VBOData = numpy.array(finalVertexPositions + finalVertexColors + finalVertexUvs, dtype='float32')

        # Set up the vertex buffer that will store our vertex coordinates for OpenGL's access

    def initVertexBuffer(self):

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

        # bind to our self.VAO
        glBindVertexArray(self.VAO)

        # now change the state - it will be recorded in the self.VAO
        # set array buffer to our ID
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        # set data
        elementSize = numpy.dtype(numpy.float32).itemsize

        # third argument is criptic - in c_types if you multiply a data type with an integer you create an array of that type
        glBufferData(GL_ARRAY_BUFFER, len(self.VBOData) * elementSize, self.VBOData, GL_STATIC_DRAW)

        # setup vertex attributes
        offset = 0

        # location 0
        glVertexAttribPointer(0, self.vertexDim, GL_FLOAT, GL_FALSE, elementSize * self.vertexDim,
                              ctypes.c_void_p(offset))
        glEnableVertexAttribArray(0)

        # define colors which are passed in location 1 - they start after all positions and has four floats consecutively
        offset += elementSize * self.vertexDim * self.nVertices
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, elementSize * 4, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(1)

        # define uvs which are passed in location 2 - they start after all positions and colors and has two floats per vertex
        offset += elementSize * 4 * self.nVertices
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, elementSize * 2, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(2)

        # reset array buffers
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def get_nVertices(self):
        return self.nVertices

    def get_VAO(self):
        return self.VAO

    @staticmethod
    def open_shader_files(vertex_shader_path, fragment_shader_path):
        try:
            # String containing vertex shader program written in GLSL
            with open(vertex_shader_path, 'r') as fVertexShader:
                strVertexShader = fVertexShader.read()

            # String containing fragment shader program written in GLSL
            with open(fragment_shader_path, 'r') as fFragmentShader:
                strFragmentShader = fFragmentShader.read()

            return (strVertexShader, strFragmentShader)
        except FileNotFoundError:
            print("File Not Found")
            exit()
