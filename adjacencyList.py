from parser import ObjParser
from vector import Edge, Vector3
from collections import OrderedDict
from utils import remove_duplicates


class AdjacencyList:
    def __init__(self, vertices, faces, edges):
        self.vertices = vertices
        self.faces = faces  # Default Triangular
        self.edges = edges

        # For faster findings
        self.edges_map = OrderedDict()

        self.make_edges_map()

        self.v_e = [[] for v in self.vertices]
        self.v_f = [[] for v in self.vertices]
        self.f_e = [[] for f in self.faces]

        self.e_v = [[] for e in range(3 * len(self.faces))]
        self.e_f = [[] for _ in self.edges]

        self.neighbour_faces_of_edges = [[] for _ in self.edges]

        self.map_vertices_to_edges()
        self.map_vertices_to_faces()
        self.map_faces_to_edges()

    """
    def make_edges(self):
        # Find all the edges in a face
        for q, face in enumerate(self.faces):
            face_edges = []
            for v in range(len(face)):
                for v2 in range(v + 1, len(face), 1):
                    edge = Edge(face[v], face[v2])
                    face_edges.append(edge)
                    self.edges.add(edge)
            self.f_e[q] = face_edges
    """

    """
    def _remove_duplicates(self, input_list):
        seen = set()
        result = []

        for item in input_list:
            if item not in seen:
                seen.add(item)
                result.append(item)

        return result
    """

    """
    # Quad Triangulazation
    # Triangle Fan can be used for bigger 4+ vertices shapes
    def triangulate_face(self, faces):
        for q, face in enumerate(faces):
            first_tri = face[0:3]
            second_tri = [face[2], face[3], face[0]]
            self.faces.append(first_tri)
            self.faces.append(second_tri)
            self.quad_faces.append(face)
    """

    """
    def make_edges(self):
        for q, face in enumerate(self.faces):
            edges = (Edge(face[0], face[1]),
                     Edge(face[1], face[2]),
                     Edge(face[2], face[0]))
            for edge in edges:
                self.edges.append(edge)
        self.edges = self._remove_duplicates(self.edges)
    """

    def map_vertices_to_edges(self, edges=None, vertex_count=None):
        # Map all vertices to a belonged edge
        flag = False
        if edges is None and vertex_count is None:
            edges = self.edges
            vertex_count = len(self.vertices)
            flag = True

        v_e = [[] for _ in range(vertex_count)]
        for i, edge in enumerate(edges):
            v_e[edge[0]].append(i)
            v_e[edge[1]].append(i)

        if flag:
            self.v_e = v_e.copy()
            return
        else:
            return v_e

    def map_vertices_to_faces(self):
        for q, face in enumerate(self.faces):
            for v in face:
                self.v_f[v].append(q)

    # TODO function is very naive optimize it
    def map_faces_to_edges(self):
        for q, face in enumerate(self.faces):
            for face_i, v in enumerate(face):
                v_e_list = self.v_e[v]
                for i in v_e_list:
                    edge = self.edges[i]
                    if edge[0] in face and edge[1] in face:
                        self.f_e[q].append(i)
                        self.e_f[i].append(q)
            self.f_e[q] = remove_duplicates(self.f_e[q])

        for idx, e_f in enumerate(self.e_f):
            self.e_f[idx] = remove_duplicates(self.e_f[idx])

    def get_index_of_vertex(self, vertex):
        for i, v in enumerate(self.vertices):
            if vertex == v:
                return i
        return None

    def get_index_of_edge(self, edge):
        return self.edges_map[edge]

    def get_adjacent_vertices_of_vertex(self, vertex_index):
        adjacency_edges = self.v_e[vertex_index]
        result = []
        for edge_idx in adjacency_edges:
            edge = self.v_e[edge_idx]
            if edge[0] == vertex_index:
                result.append(edge[1])
            else:
                result.append(edge[0])
        return result

    def get_adjacent_faces_of_vertex(self, vertex_index):
        adjacency_face = self.v_f[vertex_index]
        return adjacency_face

    def get_adjacent_edges_of_vertex(self, vertex_index):
        adjacency_edges = self.v_e[vertex_index]
        return adjacency_edges

    def get_neighbour_faces_of_edge(self, edge_index):
        return self.e_f[edge_index]
        """
        neighbour_faces = []
        for f_i, face in enumerate(self.f_e):
            for e in face:
                if e == edge_index:
                    neighbour_faces.append(f_i)
                if len(neighbour_faces) == 2:
                    break
        return neighbour_faces
        """

    """
    # For Triangulated
    
    def get_adjacenies_of_vertex(self, vertex_index):
        adjacency_edges = self.v_e[vertex_index]
        result = []
        for edge_idx in adjacency_edges:
            edge = self.edges[edge_idx]
            if edge[0] == vertex_index:
                result.append(edge[1])
            else:
                result.append(edge[0])
        return result
    """

    def make_edges_map(self):
        for i, e in enumerate(self.edges):
            self.edges_map[e] = i


if "__main__" == __name__:
    obj_parser = ObjParser()
    obj_parser.parse("ecube.obj")

    l = AdjacencyList(obj_parser.vertices, obj_parser.faces)
    print(l.faces)
    print(l.get_adjacent_faces_of_vertex(0))
    print(l.edges)
    print(l.get_adjacent_edges_of_vertex(0))
    print(l.e_f)
    """
    print(l.faces)
    print(l.edges, len(l.edges))
    print(l.f_e)
    """

# print(l.quad_v_e)
