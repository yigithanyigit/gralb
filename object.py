import copy
import random
from typing import List

from parser import ObjParser
from matrix4 import Matrix4
from vector import Vector3, Vector4, Edge
from OpenGL.GL import *
from adjacencyList import AdjacencyList
from utils import remove_duplicates
from definitions import Definitions
from shader import Shader


class Object:
    def __init__(self, vertices: List[Vector3], colors: List[Vector3] = None, faces=None, edges=None,
                 adjacency_list=None, normals=None, uv=None, face_normals=None, face_uvs=None):

        if faces is None:
            faces = []

        if normals is None:
            normals = []

        if uv is None:
            uv = []

        if face_normals is None:
            face_normals = []

        if face_uvs is None:
            face_uvs = []

        self.vertices = vertices
        self.faces = faces
        self.quad_faces = None

        self.normals = normals
        self.face_normals = face_normals

        self.uv = uv
        self.face_uvs = face_uvs

        self.min_vertex_per_face = 9999999

        for face in self.faces:
            self.min_vertex_per_face = min(len(face), self.min_vertex_per_face)

        if self.min_vertex_per_face == 4:
            self.quad_faces = faces
            self.quad_edges = []
            self.quad_edges = Object.make_quad_edges(self.quad_faces)
            self.faces = self.triangle_fan(self.faces)
        elif self.min_vertex_per_face == 3:
            self.quad_faces = []
            for f in self.faces:
                if len(f) == 4:
                    self.quad_faces.append(f)
            self.quad_edges = []
            self.quad_edges = Object.make_quad_edges(self.quad_faces)
            self.faces = self.triangle_fan(self.faces)

        if edges is None:
            self.edges = []
            self.edges = Object.make_triangle_edges(self.faces)
        else:
            self.edges = edges

        self.subdivision_state = []

        if colors is None:
            colors = Object.make_random_color(self.faces)

        if adjacency_list is None and self.min_vertex_per_face == 4:
            self.quad_adjacency_list = AdjacencyList(self.vertices, self.quad_faces, self.quad_edges)
        else:
            self.quad_adjacency_list = adjacency_list

        self.colors = colors
        self.model = Matrix4.identity()
        self.T = Matrix4().identity()
        self.R = Matrix4().identity()
        self.S = Matrix4().identity()

        self.subdivision = 0
        self.subdivision_initial = self.subdivision
        self.subdivision_func = self.subdivision_surface

        # This Stack For Matrix Tranformations
        self.stack = []
        self.calculated_stack = False

        # This Stack for model matrix stack
        self.model_stack = []
        self.calculated_model_stack = False
        self.model_stack.append(self.model)

        # Shaders
        self.shader = Shader(self)

        # Load after Initialized all the things
        self.subdivision_state.append(self.copy())

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

    def get_x(self):
        return self.model.rows[3][0]

    def get_y(self):
        return self.model.rows[3][1]

    def get_z(self):
        return self.model.rows[3][2]

    def get_middle_point(self):
        point = Vector3()
        index = 0
        for idx, f in enumerate(self.faces):
            for v in f:
                point = point + self.vertices[v]
            index = idx
        point = point / (index + 1)
        return point

    # it is not a proper function
    def go_to(self, x, y, z):
        # current_loc = Vector3(self.get_x(), self.get_y(), self.get_z())
        current_loc = self.get_middle_point()
        destination = Vector3(-x, -y, -z)
        if current_loc == destination:
            return

        new_loc = Vector3()
        xdiff = x - current_loc.x()
        ydiff = y - current_loc.y()
        zdiff = z - current_loc.z()

        new_loc.set_x(current_loc.x() + xdiff)
        new_loc.set_y(current_loc.y() + ydiff)
        new_loc.set_z(current_loc.z() + zdiff)

        print(new_loc)
        self._add_matrix_to_stack(Matrix4.T(-new_loc.x(), -new_loc.y(), -new_loc.z()))
        self.calculated_stack = False

    @staticmethod
    def triangle_fan_cut(face):
        temp_edges = []
        for idx in range(1, len(face), 1):
            temp_edges.append(Edge(face[0], face[idx]))
        return temp_edges

    def triangle_fan(self, faces):
        temp_faces = []
        for q, face in enumerate(faces):
            if len(face) == 3:
                temp_faces.append(face)
                continue
            for idx in range(2, len(face), 1):
                temp_faces.append([face[0], face[idx - 1], face[idx]])
        return temp_faces

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

    def copy(self):
        return copy.deepcopy(self)

    @staticmethod
    def make_random_color(faces):
        color = []
        for _ in faces:
            r = random.randrange(0, 256) / 255
            g = random.randrange(0, 256) / 255
            b = random.randrange(0, 256) / 255
            color.append(Vector3(r, g, b))
        return color

    @staticmethod
    def make_face_normals(vertices):
        pass

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
        return Vector3(self.model[12], self.model.rows[13], self.model.rows[14])

    def load_matrix_into_modelview_stack(self, view: Matrix4):
        if view is not None:
            glLoadMatrixf(view.dot_product(self.model).asList())

    def get_model_matrix(self):
        if not self.calculated_stack:
            self.calculate()
            self.calculated_stack = True
        return self.model

    # Core profile Draw Mode
    def draw(self):

        # bind to our VAO
        glBindVertexArray(self.shader.VAO)

        # draw stuff
        glDrawArrays(GL_TRIANGLES, 0, self.shader.get_nVertices())

        # reset to defaults
        glBindVertexArray(0)
        glUseProgram(0)

    def _find_face_points(self, faces):
        face_points = []
        for face in faces:
            face_point = Vector3()
            for v in face:
                face_point = face_point + self.vertices[v]
            face_point = face_point / len(face)
            face_points.append(face_point)
        return face_points

    def _find_edge_points(self, face_point):
        edge_points = []
        for edge in self.quad_edges:
            edge_point = Vector3()
            neighbour_faces = self.quad_adjacency_list.get_neighbour_faces_of_edge(
                self.quad_adjacency_list.get_index_of_edge(edge))
            edge_point = face_point[neighbour_faces[0]] + face_point[neighbour_faces[1]]
            for v in edge:
                edge_point = edge_point + self.vertices[v]
            edge_point = edge_point / 4
            edge_points.append(edge_point)
        return edge_points

    def subdivision_surface(self):
        pass

    def catmull_clark_sub(self):

        face_points = self._find_face_points(self.quad_faces)
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
            valence = len(self.quad_adjacency_list.get_adjacent_edges_of_vertex(v_i))
            touching_faces = self.quad_adjacency_list.get_adjacent_faces_of_vertex(v_i)
            touching_edges = self.quad_adjacency_list.get_adjacent_edges_of_vertex(v_i)
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
        for f_i, vertices in enumerate(self.quad_faces):
            temp_vertices = [*vertices]
            for i in range(len(vertices)):
                adjacent_edges = self.quad_adjacency_list.get_adjacent_edges_of_vertex(vertices[i])
                for edge in adjacent_edges:
                    e = self.quad_edges[edge]
                    e2 = Edge(vertices[i], vertices[((i + 1) % 4)])
                    e2_r = Edge(vertices[((i + 1) % 4)], vertices[i])
                    if e == e2 or e == e2_r:
                        temp_vertices.append(edge)
                        continue
            temp_vertices.append(f_i)

            # First 4 of temp_vertices is control_points, the other 4 is Edge_points the last one is Face_point

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

        self.quad_faces = faces
        self.vertices = new_vertices
        self.quad_edges = Object.make_quad_edges(self.quad_faces)
        self.quad_adjacency_list = AdjacencyList(self.vertices, self.quad_faces, self.quad_edges)

        self.edges = self.make_triangle_edges(self.quad_faces)
        self.faces = self.triangle_fan(self.quad_faces)
        self.colors = Object.make_random_color(self.faces)

        self.shader = Shader(self)

        self.subdivision_state.append(self.copy())

    def loop_subdivision(self):
        pass

    def increase_subdivision(self):
        if self.subdivision + 1 < 7:
            if self.subdivision + 1 <= len(self.subdivision_state) - 1:
                obj = self.subdivision_state[self.subdivision + 1]
                """
                self.vertices = obj.vertices
                self.quad_faces = obj.quad_faces
                self.quad_edges = obj.quad_edges
                self.faces = obj.faces
                self.edges = obj.edges
                self.colors = obj.colors
                self.quad_adjacency_list = obj.quad_adjacency_list
                self.shader = obj.shader
                """
                self.override_object(obj)
                self.subdivision += 1
            else:
                if self.min_vertex_per_face == 3:
                    return
                self.catmull_clark_sub()
                self.subdivision += 1

    def decrease_subdivision(self):
        if self.subdivision - 1 >= 0:
            obj = self.subdivision_state[self.subdivision - 1]
            """
            self.vertices = obj.vertices
            self.quad_faces = obj.quad_faces
            self.quad_edges = obj.quad_edges
            self.faces = obj.faces
            self.edges = obj.edges
            self.colors = obj.colors
            self.quad_adjacency_list = obj.quad_adjacency_list
            self.shader = obj.shader
            """
            self.override_object(obj)
            self.subdivision -= 1

    @staticmethod
    def make_quad_edges(faces):
        # Find all the edges in a face
        edges = []
        for q, face in enumerate(faces):
            es = (Edge(face[0], face[1]),
                  Edge(face[1], face[2]),
                  Edge(face[2], face[3]),
                  Edge(face[3], face[0]),
                  )
            for e in es:
                edges.append(e)
        return remove_duplicates(edges)

    @staticmethod
    def make_triangle_edges(faces):
        # Find all the edges in a face
        edges = []
        for q, face in enumerate(faces):
            temp_edges = Object.triangle_fan_cut(face)
            for e in temp_edges:
                edges.append(e)
        return remove_duplicates(edges)

    def override_object(self, obj):
        # https://stackoverflow.com/questions/11637293/iterate-over-object-attributes-in-python
        attributes = [attr for attr in dir(self) if not attr.startswith('__') and not callable(getattr(obj, attr)) and attr != 'subdivision'
                      and attr != 'subdivision_state']
        for attr in attributes:
            setattr(self, attr, getattr(obj, attr))

if "__main__" == __name__:
    obj_parser = ObjParser()
    obj_parser.parse("ecube.obj")

    obj = Object(obj_parser.vertices, faces=obj_parser.faces)
    print(obj_parser.vertices)
    print(obj_parser.faces)
    print(obj.quad_adjacency_list.edges)
    print(obj.quad_adjacency_list.f_e)
    print(obj.quad_adjacency_list.v_e)
    """
    print(l.faces)
    print(l.edges, len(l.edges))
    print(l.f_e)
    """
    obj.catmull_clark_sub()
