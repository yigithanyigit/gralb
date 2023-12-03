from vector import Vector3


class ObjParser:
    def __init__(self):
        self.vertices = []
        self.normals = []
        self.faces = []

    def parse(self, filename):
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
                    #face = [tuple(map(int, vertex.split('/'))) for vertex in tokens[1:]]
                    face = [int(vertex.split('/')[0]) - 1 for vertex in tokens[1:]]
                    self.faces.append(face)
                """
                elif tokens[0] == 'vn':
                    # Normal
                    normal = list(map(float, tokens[1:]))
                    self.normals.append(normal)
                """


if __name__ == "__main__":
    obj_parser = ObjParser()
    obj_parser.parse("cube.obj")

    print("Vertices:")
    for vertex in obj_parser.vertices:
        print(vertex)

    """
    print("\nNormals:")
    for normal in obj_parser.normals:
        print(normal)
    """

    print("\nFaces:")
    for face in obj_parser.faces:
        print(face)
