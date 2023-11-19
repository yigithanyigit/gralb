import random
from typing import List
from matrix4 import Matrix4
from vector import Vector3, Vector4
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math


class Object:
    def __init__(self, vertices: List[Vector3], colors: List[Vector4] = None):
        self.vertices = vertices
        self.colors = colors
        self.model = Matrix4.identity()
        self.T = Matrix4().identity()
        self.R = Matrix4().identity()
        self.S = Matrix4().identity()
        self.subdivision = 0
        self.subdivision_initial = self.subdivision
        self.subdivision_state = False

        # This Stack For Matrix Tranformations
        self.stack = []
        self.calculated_stack = False

        # This Stack for model matrix stack
        self.model_stack = []
        self.calculated_model_stack = False
        self.model_stack.append(self.model)

        # Subdivided object list
        self.subdivided = []

    def _add_matrix_to_model_stack(self):
        self.model_stack.append(self.model)
        self.model = self.model.copy()

    def _pop_matrix_from_model_stack(self):
        if len(self.model_stack) != 0:
            self.model_stack.pop()

    def _model_stack_head(self):
        if len(self.model_stack) > 0:
            return self.model_stack[-1]
        return None

    def _add_matrix_to_stack(self, op):
        self.stack.append(op)

    def _pop_matrix_from_stack(self):
        if len(self.stack) != 0:
            self.stack.pop()

    def _stack_head(self):
        if len(self.stack) > 0:
            return self.stack[-1]
        return None

    def calculate(self):
        m = self.model
        while self._stack_head() is not None:
            m = m.dot_product(self._stack_head())
            self._pop_matrix_from_stack()
        self.model.rows = m.rows
        self.calculated_stack = True
        return self

    def get_model_matrix(self):
        return self.model_stack[-1]

    def rotate_x(self, x):
        self._add_matrix_to_stack(Matrix4.Rx(x))
        self.calculated_stack = False

    def rotate_y(self, x):
        self._add_matrix_to_stack(Matrix4.Ry(x))
        self.calculated_stack = False

    def rotate_z(self, x):
        self._add_matrix_to_stack(Matrix4.Rz(x))
        self.calculated_stack = False

    def translate(self, x, y, z):
        self._add_matrix_to_stack(Matrix4.T(x, y, z))
        self.calculated_stack = False

    def scale(self, scalar):
        self._add_matrix_to_stack(Matrix4.S(scalar))
        self.calculated_stack = False

    # Returns X Y Z position of Object
    def get_object_position(self):
        return Vector3(self.model[12], self.model[13], self.model[14])

    def load_matrix_into_modelview_stack(self, view: Matrix4):
        if view is not None:
            glLoadMatrixf(view.dot_product(self.model).asList())

    def draw(self):
        pass

    def increase_subdivision(self):
        self.subdivision += 1
        self.subdivision_state = True

    def decrease_subdivision(self):
        if self.subdivision - 1 >= self.subdivision_initial:
            self.subdivision -= 1
            self.subdivision_state = False


class Square(Object):
    def __init__(self, vertices=(
            Vector3(-1.0, -1.0, 1),  # Bottom Left Of The Quad (Front)
            Vector3(1.0, -1.0, 1),  # Bottom Right Of The Quad (Front)
            Vector3(1.0, 1.0, 1),  # Top Right Of The Quad (Front)
            Vector3(-1.0, 1.0, 1),  # Top Left Of The Quad (Front)

    )):
        super().__init__(vertices)
        self.subdivision = 0


    def draw(self, camera=None):
        if self.subdivision_state == True:
            self.subdivision_state = False
            self.vertices = self.divide_square(subdivision=self.subdivision)
        if not self.calculated_stack:
            self.calculate()
        glBegin(GL_QUADS)
        for i in self.vertices:
            glVertex3f(i.x(), i.y(), i.z())
        glEnd()
        self.load_matrix_into_modelview_stack(camera.get_view_matrix())
        """
        for quad in quads:
            q = Square(quad)
            q.stack = self.stack.copy()
            q.draw(camera)
        """


    def divide_square(self, subdivision=0):
        # TODO FIX THIS
        self.vertices = (
            Vector3(-1.0, -1.0, 1),  # Bottom Left Of The Quad (Front)
            Vector3(1.0, -1.0, 1),  # Bottom Right Of The Quad (Front)
            Vector3(1.0, 1.0, 1),  # Top Right Of The Quad (Front)
            Vector3(-1.0, 1.0, 1),  # Top Left Of The Quad (Front)

        )

        quads = []
        width = abs(self.vertices[0].x() - self.vertices[1].x()) / (2 ** subdivision)
        height = abs(self.vertices[0].y() - self.vertices[2].y()) / (2 ** subdivision)
        # depth = abs(self.vertices[0].z() - self.vertices[2].z()) / (2 ** subdivision)

        for i in range(2 ** subdivision):
            for j in range(2 ** subdivision):
                # Makes Vertex in CCW order
                c0 = self.vertices[0].x() + i * width
                c1 = self.vertices[0].x() + (i + 1) * width
                v0 = self.vertices[0].y() + j * height
                v1 = self.vertices[0].y() + (j + 1) * height

                # Front Square
                f0 = Vector3(c0, v0, 1)
                f1 = Vector3(c1, v0, 1)
                f2 = Vector3(c1, v1, 1)
                f3 = Vector3(c0, v1, 1)

                # Back Square
                b0 = Vector3(c0, v0, -1)
                b1 = Vector3(c1, v0, -1)
                b2 = Vector3(c1, v1, -1)
                b3 = Vector3(c0, v1, -1)

                # Left Square

                l0 = Vector3(-1, c0, v0)
                l1 = Vector3(-1, c1, v0)
                l2 = Vector3(-1, c1, v1)
                l3 = Vector3(-1, c0, v1)

                # Right Square

                r0 = Vector3(1, c0, v0)
                r1 = Vector3(1, c1, v0)
                r2 = Vector3(1, c1, v1)
                r3 = Vector3(1, c0, v1)

                # Top Square

                t0 = Vector3(c0, 1, v0)
                t1 = Vector3(c1, 1, v0)
                t2 = Vector3(c1, 1, v1)
                t3 = Vector3(c0, 1, v1)

                # Bottom Square

                bo0 = Vector3(c0, -1, v0)
                bo1 = Vector3(c1, -1, v0)
                bo2 = Vector3(c1, -1, v1)
                bo3 = Vector3(c0, -1, v1)

                """
                new_vertices = [
                    f0,
                    f1,
                    f2,
                    f3,
                ]
                quads.append(new_vertices)
                """

                quads.append(f0)
                quads.append(f1)
                quads.append(f2)
                quads.append(f3)


        return quads


class Cube(Object):
    def __init__(self, vertices=(
            Vector3(-1.0, -1.0, 1),  # Bottom Left Of The Quad (Front)
            Vector3(1.0, -1.0, 1),  # Bottom Right Of The Quad (Front)
            Vector3(1.0, 1.0, 1),  # Top Right Of The Quad (Front)
            Vector3(-1.0, 1.0, 1),  # Top Left Of The Quad (Front)

    )):
        self.subdivision = 0
        super().__init__(vertices)


    def draw(self, camera=None):

        quads = self.divide_quad(camera, self.subdivision)

        for quad in quads:
            q = Square(quad)
            q.stack = self.stack.copy()
            q.draw(camera)

    def divide_quad(self, matView, subdivision=0):
        # TODO Same as Square Fix That
        self.vertices = (
            Vector3(-1.0, -1.0, 1),  # Bottom Left Of The Quad (Front)
            Vector3(1.0, -1.0, 1),  # Bottom Right Of The Quad (Front)
            Vector3(1.0, 1.0, 1),  # Top Right Of The Quad (Front)
            Vector3(-1.0, 1.0, 1),  # Top Left Of The Quad (Front)

        )

        quads = []
        width = abs(self.vertices[0].x() - self.vertices[1].x()) / (2 ** subdivision)
        height = abs(self.vertices[0].y() - self.vertices[2].y()) / (2 ** subdivision)
        # depth = abs(self.vertices[0].z() - self.vertices[2].z()) / (2 ** subdivision)

        for i in range(2 ** subdivision):
            for j in range(2 ** subdivision):
                # Makes Vertex in CCW order
                c0 = self.vertices[0].x() + i * width
                c1 = self.vertices[0].x() + (i + 1) * width
                v0 = self.vertices[0].y() + j * height
                v1 = self.vertices[0].y() + (j + 1) * height

                # Front Square
                f0 = Vector3(c0, v0, 1)
                f1 = Vector3(c1, v0, 1)
                f2 = Vector3(c1, v1, 1)
                f3 = Vector3(c0, v1, 1)

                # Back Square
                b0 = Vector3(c0, v0, -1)
                b1 = Vector3(c1, v0, -1)
                b2 = Vector3(c1, v1, -1)
                b3 = Vector3(c0, v1, -1)

                # Left Square

                l0 = Vector3(-1, c0, v0)
                l1 = Vector3(-1, c1, v0)
                l2 = Vector3(-1, c1, v1)
                l3 = Vector3(-1, c0, v1)

                # Right Square

                r0 = Vector3(1, c0, v0)
                r1 = Vector3(1, c1, v0)
                r2 = Vector3(1, c1, v1)
                r3 = Vector3(1, c0, v1)

                # Top Square

                t0 = Vector3(c0, 1, v0)
                t1 = Vector3(c1, 1, v0)
                t2 = Vector3(c1, 1, v1)
                t3 = Vector3(c0, 1, v1)

                # Bottom Square

                bo0 = Vector3(c0, -1, v0)
                bo1 = Vector3(c1, -1, v0)
                bo2 = Vector3(c1, -1, v1)
                bo3 = Vector3(c0, -1, v1)

                new_vertices = [
                    f0,
                    f1,
                    f2,
                    f3,
                    b0,
                    b1,
                    b2,
                    b3,
                    l0,
                    l1,
                    l2,
                    l3,
                    r0,
                    r1,
                    r2,
                    r3,
                    t0,
                    t1,
                    t2,
                    t3,
                    bo0,
                    bo1,
                    bo2,
                    bo3,

                ]
                quads.append(new_vertices)

        """
        for quad in quads:
            q = Square(quad)
            q.stack = self.stack.copy()
            q.draw(matView)
        """
        return quads

class Cylinder(Object):
    def __init__(self, radius=1, origin_vertex=Vector3(0, 0, 0), num_segments=3, length=2):
        self.num_segments = num_segments
        self.origin_vertex = origin_vertex
        self.length = length
        self.radius = radius
        self.side_indices = []
        self.top_indices = []
        self.bottom_indices = []
        self.base_top_vertex = Vector3
        self.base_bottom_vertex = Vector3
        super().__init__(self._vertex_generator(radius, origin_vertex))

    def increase_subdivision(self):
        self.num_segments += 1
        self = Cylinder(self.radius, self.origin_vertex, self.num_segments+1, self.length)
        return self

    def decrease_subdivision(self):
        if self.num_segments - 1 >= 3:
            self.num_segments -= 1


    def _vertex_generator(self, radius, origin_vertex):
        vertices = []
        upper_circle = []
        lower_circle = []
        for i in range(self.num_segments):
            theta = 2.0 * math.pi * float(i) / float(self.num_segments)
            v1 = radius * math.cos(theta)
            v2 = radius * math.sin(theta)
            upper_circle.append(Vector3(v1, origin_vertex.y() + self.length / 2, v2))
            lower_circle.append(Vector3(v1, origin_vertex.y() - self.length / 2, v2))
            # vertices = upper_circle + lower_circle
        self.side_indices = self._side_indices(upper_circle, lower_circle)
        self.top_indices = self._side_indices(upper_circle, lower_circle)
        self.bottom_indices = self._side_indices(upper_circle, lower_circle)
        self.base_top_vertex = Vector3(origin_vertex.x(), origin_vertex.y() + self.length / 2, origin_vertex.z())
        self.base_bottom_vertex = Vector3(origin_vertex.x(), origin_vertex.y() - self.length / 2, origin_vertex.z())
        return lower_circle + upper_circle

    def _side_indices(self, upper_circle, lower_circle):
        offset = len(lower_circle)
        side_vertices = []

        for i in range(offset - 1):
            side_vertices.append(i)
            side_vertices.append(i + 1)
            side_vertices.append(offset + i)

            side_vertices.append(offset + i)
            side_vertices.append(offset + i + 1)
            side_vertices.append(i + 1)

        side_vertices.append(len(lower_circle) - 1)
        side_vertices.append(0)
        side_vertices.append(len(lower_circle) + len(upper_circle) - 1)

        side_vertices.append(len(lower_circle) + len(upper_circle) - 1)
        side_vertices.append(offset)
        side_vertices.append(0)

        return side_vertices

    def _top_indices(self, lower_circle, upper_circle):
        top_indices = []
        for i in range(len(upper_circle) - 1):
            top_indices.append(len(lower_circle) + i)
        return top_indices

    def _bottom_indices(self, lower_circle, upper_circle):
        bottom_indices = []
        for i in range(len(lower_circle) - 1):
            bottom_indices.append(i)
        return bottom_indices

    def draw(self, camera=None, subdivision=3):
        self.vertices = self._vertex_generator(self.radius, self.origin_vertex)
        self.draw_side(camera)
        #self.draw_top(camera)
        #self.draw_bottom(camera)

    def draw_side(self, camera=None):
        if not self.calculated_stack:
            self.calculate()

        glBegin(GL_TRIANGLES)
        for e in self.side_indices:
            glVertex3f(self.vertices[e].x(), self.vertices[e].y(), self.vertices[e].z())
        glEnd()

        self.load_matrix_into_modelview_stack(camera.get_view_matrix())

    def draw_top(self, camera=None):
        if not self.calculated_stack:
            self.calculate()

        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(self.base_top_vertex.x(), self.base_top_vertex.y(), self.base_top_vertex.z())
        for e in self.top_indices:
            glVertex3f(self.vertices[e].x(), self.vertices[e].y(), self.vertices[e].z())
        glEnd()

        self.load_matrix_into_modelview_stack(camera.get_view_matrix())

    def draw_bottom(self, camera=None):
        if not self.calculated_stack:
            self.calculate()

        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(self.base_bottom_vertex.x(), self.base_bottom_vertex.y(), self.base_bottom_vertex.z())
        for e in self.bottom_indices:
            glVertex3f(self.vertices[e].x(), self.vertices[e].y(), self.vertices[e].z())
        glEnd()

        self.load_matrix_into_modelview_stack(camera.get_view_matrix())

    def divide(self, subdivision, matView=None):
        pass

class Pyramid(Object):
    pass

class Sphere(Object):

    def __init__(self, radius = 1, origin_vertex=Vector3(0,0,0), num_segments = 10):
        self.radius = radius
        self.origin_vertex = origin_vertex
        self.num_segments = num_segments
        self.top_center = Vector3(0,0,0)
        self.bottom_center = Vector3(0,0,0)
        self.mid_center = Vector3(0,0,0)
        super().__init__([self.top_center, self.bottom_center] + self._vertex_generator())

    # TODO
    # Some Error Happening If I Change name of the sum_segments to subdivision
    def increase_subdivision(self):
        self.num_segments += 1
        self.vertices = [self.top_center, self.bottom_center] + self._vertex_generator()


    def decrease_subdivision(self):
        if self.num_segments - 1 >= 5:
            self.num_segments -= 1
            self.vertices = [self.top_center, self.bottom_center] + self._vertex_generator()

    def circle_vertex_generator(self, origin_vertex, radius):
        vertices = []
        for i in range(self.num_segments):
            theta = 2.0 * math.pi * float(i) / float(self.num_segments)
            v1 = radius * math.cos(theta)
            v2 = radius * math.sin(theta)
            vertices.append(Vector3(v1, origin_vertex.y(), v2))
        return vertices
    def _vertex_generator(self):
        self.top_center = self.origin_vertex + Vector3(0,self.radius,0)
        self.bottom_center = self.origin_vertex - Vector3(0, self.radius, 0)
        self.mid_center = self.bottom_center + Vector3(0,self.radius,0)

        step = 2 * self.radius / (self.num_segments + 1)

        center_vertices = []
        vertices = []

        for i in range(1, self.num_segments + 1):
            theta_step = 180 / self.num_segments


            center_vertex = Vector3(0, i * step, 0) + self.bottom_center
            center_vertices.append(center_vertex)



            temp_vertices = self.circle_vertex_generator(center_vertex, self.radius * math.cos(math.radians(90 + (i - 1) * theta_step)))

            for v in temp_vertices:
                vertices.append(v)
        return vertices

    def _side_indices(self, upper_circle, lower_circle, offset):
        side_vertices = []

        for i in range(len(lower_circle)  - 1):
            side_vertices.append(i + offset)
            side_vertices.append(i + 1 + offset)
            side_vertices.append(len(lower_circle)  + i + offset)

            side_vertices.append(len(lower_circle)  + i + offset)
            side_vertices.append(len(lower_circle)  + i + 1 + offset)
            side_vertices.append(i + 1 + offset)

        side_vertices.append(len(lower_circle) - 1 + offset)
        side_vertices.append(0 + offset)
        side_vertices.append(len(lower_circle) + len(upper_circle) - 1 + offset)

        side_vertices.append(len(lower_circle) + len(upper_circle) - 1 + offset)
        side_vertices.append(len(lower_circle) + offset)
        side_vertices.append(0 + offset)

        return side_vertices

    def _draw_side(self, camera):
        # Ignoring Base And Bottom Vertices
        side_vertices = self.vertices[2:]
        side_indices = []
        offset = 2
        for i in range(self.num_segments * 2, len(self.vertices),self.num_segments):
            lower_circle = side_vertices[i-self.num_segments * 2:i-self.num_segments]
            upper_circle = side_vertices[i-self.num_segments:i]
            side_indices = self._side_indices(lower_circle, upper_circle, offset)
            offset += self.num_segments
            glBegin(GL_TRIANGLES)
            for e in side_indices:
                glVertex3f(self.vertices[e].x(), self.vertices[e].y(), self.vertices[e].z())
            glEnd()
            self.load_matrix_into_modelview_stack(camera.get_view_matrix())



    def draw(self, camera, subdivision=0):
        if not self.calculated_stack:
            self.calculate()
        self._draw_side(camera)

        """
        glBegin(GL_TRIANGLES)
        for e in self.side_indices:
            glVertex3f(self.vertices[e].x(), self.vertices[e].y(), self.vertices[e].z())
        glEnd()
        """

        """
        glBegin(GL_POINTS)
        for e in self.vertices:
            glVertex3f(e.x(), e.y(), e.z())
        glEnd()


        self.load_matrix_into_modelview_stack(camera.get_view_matrix())
        """
