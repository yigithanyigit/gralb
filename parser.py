from vector import Vector3


class ObjParser:
    def __init__(self):
        self.vertices = []
        self.normals = []
        self.uv = []
        self.faces = []
        self.faces_uv = []
        self.faces_normal = []

    def parse(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    tokens = line.strip().split()
                    if not tokens:
                        continue

                    if tokens[0] == 'v':
                        # Vertex
                        vertex = list(map(float, tokens[1:]))
                        vertex = Vector3(vertex[0], vertex[1], vertex[2])
                        self.vertices.append(vertex)
                    elif tokens[0] == 'f':
                        # Face
                        face_vertex = [tuple(map(int, vertex.split('/'))) for vertex in tokens[1:]]
                        # face = [int(vertex.split('/')[0]) - 1 for vertex in tokens[1:]]
                        temp_faces = []
                        temp_faces_uv = []
                        temp_faces_normal = []

                        for vd in face_vertex:
                            temp_faces.append(int(vd[0]) - 1)
                            if len(vd) > 1:
                                temp_faces_uv.append(int(vd[1]) - 1)
                            elif len(vd) > 2:
                                temp_faces_normal.append(int(vd[2]) - 1)

                        self.faces.append(temp_faces)
                        if len(temp_faces_uv) > 1:
                            self.faces_uv.append(temp_faces_uv)
                        elif len(temp_faces_normal) > 1:
                            self.faces_normal.append(temp_faces_normal)

                    elif tokens[0] == 'vn':
                        # Normal
                        normal = list(map(float, tokens[1:]))
                        self.normals.append(normal)
                    elif tokens[0] == 'vt':
                        # UV
                        uv = list(map(float, tokens[1:]))
                        self.uv.append(uv)
        except FileNotFoundError:
            print("There is no file that you entered")
            exit()


if __name__ == "__main__":
    obj_parser = ObjParser()
    obj_parser.parse("cube.obj")

    print("Vertices:")
    for vertex in obj_parser.vertices:
        print(vertex)

    print("\nNormals:")
    for normal in obj_parser.normals:
        print(normal)

    print("\nFaces:")
    for face in obj_parser.faces:
        print(face)
