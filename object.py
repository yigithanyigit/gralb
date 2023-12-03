import random
from typing import List

from Assigment3.parser import ObjParser
from matrix4 import Matrix4
from vector import Vector3, Vector4, Edge
from OpenGL.GL import *
from adjacencyList import AdjacencyList
import random


class Object:
    def __init__(self, vertices: List[Vector3], colors: Vector4 = None, faces=None):

        if faces is None:
            faces = []

        self.vertices = vertices
        self.faces = faces

        if colors is None:
            colors = self.make_random_color()

        self.adjacency_list = AdjacencyList(self.vertices, self.faces)

        self.colors = colors
        self.model = Matrix4.identity()
        self.T = Matrix4().identity()
        self.R = Matrix4().identity()
        self.S = Matrix4().identity()

        self.subdivision = 0
        self.subdivision_initial = self.subdivision
        self.subdivision_func = self.subdivision_surface
        self.subdivision_state = False

        # This Stack For Matrix Tranformations
        self.stack = []
        self.calculated_stack = False

        # This Stack for model matrix stack
        self.model_stack = []
        self.calculated_model_stack = False
        self.model_stack.append(self.model)

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

    # Quad Triangulazation
    # Triangle Fan can be used for bigger 4+ vertices shapes
    def triangulate_face(self, faces):
        temp_faces = []
        for q, face in enumerate(faces):
            if len(face) == 3:
                temp_faces.append(face)
                continue
            first_tri = face[0:3]
            second_tri = [face[2], face[3], face[0]]
            temp_faces.append(first_tri)
            temp_faces.append(second_tri)
        return temp_faces

    def get_model_matrix(self):
        return self.model_stack[-1]

    def make_random_color(self):
        color = []
        for _ in self.faces:
            r = random.randrange(0, 256) / 255
            g = random.randrange(0, 256) / 255
            b = random.randrange(0, 256) / 255
            color.append(Vector3(r, g, b))
        return color

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

    def draw(self, camera=None):
        if not self.calculated_stack:
            self.calculate()

        # faces = self.triangulate_face(self.faces)
        glBegin(GL_QUADS)
        for f, color in zip(self.faces, self.colors):
            glColor3f(color.x(), color.y(), color.z())
            #glColor3f(1, 0, 0)
            for v in f:
                i = self.vertices[v]

                glVertex3f(i.x(), i.y(), i.z())
        glEnd()

        """
        glBegin(GL_QUADS)
        for f in self.faces:
            for v in f:
                i = self.vertices[v]
                glVertex3f(i.x(), i.y(), i.z())
        glEnd()
        """
        self.load_matrix_into_modelview_stack(camera.get_view_matrix())

    def _find_face_points(self):
        face_points = []
        for face in self.faces:
            face_point = Vector3()
            for v in face:
                face_point = face_point + self.vertices[v]
            face_point = face_point / len(face)
            face_points.append(face_point)
        return face_points

    def _find_edge_points(self, face_point):
        edge_points = []
        for edge in self.adjacency_list.edges:
            edge_point = Vector3()
            neighbour_faces = self.adjacency_list.get_neighbour_faces_of_edge(self.adjacency_list.get_index_of_edge(edge))
            edge_point = face_point[neighbour_faces[0]] + face_point[neighbour_faces[1]]
            for v in edge:
                edge_point = edge_point + self.vertices[v]
            edge_point = edge_point / 4
            edge_points.append(edge_point)
        return edge_points

    def subdivision_surface(self):
        pass

    def catmull_clark_sub(self):
        face_points = self._find_face_points()
        edge_points = self._find_edge_points(face_points)

        # new_edges = [[] for _ in range(len(self.faces) * 4 - (len(self.faces) - 1))]
        # new_faces = [[] for _ in  self.faces]
        new_edges = []
        new_faces = []

        new_vertices = [*face_points, *edge_points]
        face_points_offset = len(face_points)
        edge_points_offset = len(edge_points) + face_points_offset
        vertex_offset = face_points_offset + edge_points_offset

        for v_i, v in enumerate(self.vertices):
            valence = len(self.adjacency_list.get_adjacent_edges_of_vertex(v_i))
            touching_faces = self.adjacency_list.get_adjacent_faces_of_vertex(v_i)
            touching_edges = self.adjacency_list.get_adjacent_edges_of_vertex(v_i)
            F = Vector3()  # Average of surroinding face points
            R = Vector3()  # Average of Surrounding edge points
            P = v  # Control Point (Current Vertice)

            for t_f in touching_faces:
                F = F + face_points[t_f]
            F = F / (valence * len(touching_faces))

            for t_e in touching_edges:
                R = R + edge_points[t_e]
            R = (R * 2) / (valence * len(touching_edges))

            P = (P * (valence - 3)) / valence

            new_vertex = F + R + P
            new_vertices.append(new_vertex)

        faces = []
        for f_i, vertices in enumerate(self.faces):
            temp_vertices = [*vertices]
            for i in range(len(vertices)):
                adjacent_edges = self.adjacency_list.get_adjacent_edges_of_vertex(vertices[i])
                for edge in adjacent_edges:
                    e = self.adjacency_list.edges[edge]
                    e2 = Edge(vertices[i], vertices[((i + 1) % 4)])
                    e2_r = Edge(vertices[((i + 1) % 4)], vertices[i])
                    if e == e2 or e == e2_r:
                        temp_vertices.append(edge)
                        continue
            temp_vertices.append(f_i)

            # First 4 of temp_vertices is control_points, the other 4 is Edge_points the last one is Face_point

            """
            temp_faces = ([new_vertices[edge_points_offset + temp_vertices[0]], new_vertices[face_points_offset + temp_vertices[4]], new_vertices[temp_vertices[8]], new_vertices[face_points_offset + temp_vertices[7]]],
                    [new_vertices[face_points_offset + temp_vertices[4]], new_vertices[edge_points_offset + temp_vertices[1]], new_vertices[face_points_offset + temp_vertices[5]], new_vertices[temp_vertices[8]]],
                    [new_vertices[temp_vertices[8]], new_vertices[face_points_offset + temp_vertices[5]], new_vertices[edge_points_offset + temp_vertices[2]], new_vertices[face_points_offset + temp_vertices[6]]],
                    [new_vertices[face_points_offset + temp_vertices[7]], new_vertices[temp_vertices[8]], new_vertices[face_points_offset + temp_vertices[6]], new_vertices[edge_points_offset + temp_vertices[3]]])
            """
            temp_faces = (
                [edge_points_offset + temp_vertices[0], face_points_offset + temp_vertices[4],
                 temp_vertices[8], face_points_offset + temp_vertices[7]],
                [face_points_offset + temp_vertices[4], edge_points_offset + temp_vertices[1],
                 face_points_offset + temp_vertices[5], temp_vertices[8]],
                [temp_vertices[8], face_points_offset + temp_vertices[5],
                 edge_points_offset + temp_vertices[2], face_points_offset + temp_vertices[6]],
                [face_points_offset + temp_vertices[7], temp_vertices[8],
                 face_points_offset + temp_vertices[6], edge_points_offset + temp_vertices[3]])

            for i in temp_faces:
                faces.append(i)

            """
            print()
            print()
            print()
            for i in temp_vertices[0:4]:
                print(self.vertices[i])
            print()
            for i in temp_vertices[4:8]:
                print(edge_points[i])
            print()
            for i in temp_vertices[8:9]:
                print(face_points[i])
            print()
            """

        self.faces = faces
        self.vertices = new_vertices
        self.adjacency_list = AdjacencyList(self.vertices, self.faces)
        self.colors = self.make_random_color()

        """
        # face_points + edge_points + vertices
        for f_i, edges in enumerate(self.adjacency_list.f_e):
            for edge in edges:
                new_edges.append(Edge(f_i, face_points_offset + edge))

        for v_i, edges in enumerate(self.adjacency_list.v_e):
            for edge in edges:
                new_edges.append(Edge(edge_points_offset + v_i, face_points_offset + edge))

        new_edges = self.adjacency_list.remove_duplicates(new_edges)
        print(new_edges, len(new_edges))
        """

    def loop_subdivision(self):
        pass

    def increase_subdivision(self):
        self.subdivision += 1

    def decrease_subdivision(self):
        if self.subdivision - 1 >= self.subdivision_initial:
            self.subdivision -= 1


"""
class Square(Object):
    def __init__(self, vertices=(
            Vector3(-1.0, -1.0, 1),  # Bottom Left Of The Quad (Front)
            Vector3(1.0, -1.0, 1),  # Bottom Right Of The Quad (Front)
            Vector3(1.0, 1.0, 1),  # Top Right Of The Quad (Front)
            Vector3(-1.0, 1.0, 1),  # Top Left Of The Quad (Front)

    ), color=(Vector3(0, 0, 0))):
        super().__init__(vertices, color)
        self.subdivision = 0

    def draw(self, camera=None):
        if self.subdivision_state:
            self.subdivision_state = False
            self.vertices = self.subdivision_func(self.subdivision)
        if not self.calculated_stack:
            self.calculate()
        glBegin(GL_QUADS)
        for i in self.vertices:
            glVertex3f(i.x(), i.y(), i.z())
        glEnd()
        self.load_matrix_into_modelview_stack(camera.get_view_matrix())

    def subdivision_surface(self, subdivision):
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

                quads.append(f0)
                quads.append(f1)
                quads.append(f2)
                quads.append(f3)

            return quads

    def catmull_clark_sub(self, subdivision):
        pass

    
class Cube(Square):
    def __init__(self,vertices = (
    Vector3(1.0, 1.0, -1.0),  # Face 1
    Vector3(1.0, -1.0, -1.0),
    Vector3(1.0, -1.0, 1.0),
    Vector3(1.0, 1.0, 1.0),

    Vector3(1.0, 1.0, -1.0),  # Face 2
    Vector3(1.0, 1.0, 1.0),
    Vector3(-1.0, 1.0, 1.0),
    Vector3(-1.0, 1.0, -1.0),

    Vector3(1.0, 1.0, 1.0),  # Face 3
    Vector3(1.0, -1.0, 1.0),
    Vector3(-1.0, -1.0, 1.0),
    Vector3(-1.0, 1.0, 1.0),

    Vector3(-1.0, 1.0, 1.0),  # Face 4
    Vector3(-1.0, -1.0, 1.0),
    Vector3(-1.0, -1.0, -1.0),
    Vector3(-1.0, 1.0, -1.0),

    Vector3(-1.0, -1.0, -1.0),  # Face 5
    Vector3(-1.0, -1.0, 1.0),
    Vector3(1.0, -1.0, 1.0),
    Vector3(1.0, -1.0, -1.0),

    Vector3(-1.0, -1.0, -1.0),  # Face 6
    Vector3(1.0, -1.0, -1.0),
    Vector3(1.0, 1.0, -1.0),
    Vector3(-1.0, 1.0, -1.0)
                 ), color=(Vector3(0, 0, 0))):
        self.subdivision = 0
        super().__init__(vertices, color)


    def draw(self, camera=None):
        if not self.calculated_stack:
            self.calculate()
        glBegin(GL_QUADS)
        for i in self.vertices:
            glVertex3f(i.x(), i.y(), i.z())
        glEnd()
        self.load_matrix_into_modelview_stack(camera.get_view_matrix())
"""

if "__main__" == __name__:
    obj_parser = ObjParser()
    obj_parser.parse("ecube.obj")

    obj = Object(obj_parser.vertices, faces=obj_parser.faces)
    print(obj_parser.vertices)
    print(obj_parser.faces)
    print(obj.adjacency_list.edges)
    print(obj.adjacency_list.f_e)
    print(obj.adjacency_list.v_e)
    """
    print(l.faces)
    print(l.edges, len(l.edges))
    print(l.f_e)
    """
    obj.catmull_clark_sub()
