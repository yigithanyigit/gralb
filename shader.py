from OpenGL.GL import *
from OpenGL.GLUT import *
from definitions import Definitions
import numpy


class Shader:
    def __init__(self, obj):
        self.VBO = None
        self.VAO = None
        self.VBOData = None
        self.nVertices = 0
        self.vertexDim = Definitions.Vector3Dimension

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

        self.VBOData = numpy.array(finalVertexPositions + finalVertexColors, dtype='float32')

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
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.VBOData) * elementSize,
                     self.VBOData,
                     GL_STATIC_DRAW
                     )

        # setup vertex attributes
        offset = 0

        # location 0
        glVertexAttribPointer(0, self.vertexDim, GL_FLOAT, GL_FALSE, elementSize * self.vertexDim,
                              ctypes.c_void_p(offset))
        glEnableVertexAttribArray(0)

        # define colors which are passed in location 1 - they start after all positions and has four floats consecutively
        offset += elementSize * self.vertexDim * self.nVertices
        glVertexAttribPointer(1, self.vertexDim, GL_FLOAT, GL_FALSE, elementSize * self.vertexDim,
                              ctypes.c_void_p(offset))
        glEnableVertexAttribArray(1)


        """
        # define uvs which are passed in location 2 - they start after all positions and colors and has two floats per vertex
        offset += elementSize * self.vertexDim * self.nVertices
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, elementSize * 2, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(2)
        """

        # reset array buffers
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)


    def get_nVertices(self):
        return self.nVertices

    def get_VAO(self):
        return self.VAO

