# CENG 487 Assignment 1 by Yigithan Yigit
# Erdem Taylan # StudentId: 310201112
# 10/23

import math


class Vector:

    def __init__(self, *elements):
        self.elements = list(elements)

    def __getitem__(self, index):
        return self.elements[index]

    def __setitem__(self, index, value):
        self.elements[index] = value

    def __str__(self):
        return f"{self.elements}"

    def __repr__(self):
        return f"{self.elements}"

    def __add__(self, other):
        return type(self)(*(x + y for x, y in zip(self.elements, other.elements)))

    def __sub__(self, other):
        return type(self)(*(x - y for x, y in zip(self.elements, other.elements)))

    def __mul__(self, scalar):
        if isinstance(scalar, int) or isinstance(scalar, float):
            temp = []
            for x in self.elements:
                temp.append(scalar * x)
            return type(self)(*temp)
        else:
            raise TypeError("Values Must Be Scalar")

    def __truediv__(self, scalar):
        if isinstance(scalar, int) or isinstance(scalar, float):
            temp = []
            for x in self.elements:
                temp.append(x / scalar)
            return type(self)(*temp)
        else:
            raise TypeError("Values Must Be Scalar")


    def __hash__(self):
        return hash(tuple(self.elements))

    def __eq__(self, other):
        zipped = zip(self.elements, other.elements)
        for a, b in zipped:
            if a != b:
                return False
        return True

    def __ne__(self, other):
        zipped = zip(self.elements, other.elements)
        for a, b in zipped:
            if a != b:
                return True
        return False


    def normalize(self):
        multp = 0
        for a, b in zip(self.elements, self.elements):
            multp += a * b

        invLength = 1.0 / math.sqrt(multp)

        for i in range(len(self.elements)):
            self.elements[i] *= invLength


    def __len__(self):
        return len(self.elements)

    def sqrlen(self):
        return float(self.dot_product(self))

    def len(self):
        return math.sqrt(self.sqrlen())

    def dot_product(self, other):
        sum = 0
        for x, y in zip(self.elements, other.elements):
            sum += x * y
        return sum

    def angle_between_two_vector(self):
        pass

    def calculate_projection(self):
        pass

class Vector2(Vector):
    def __init__(self, x=None, y=None):
        if x is None and y is None:
            x, y = 0, 0
        super().__init__(x, y)

    def __str__(self):
        return f"{self.elements[0:2]}"

    def x(self):
        return float(self.elements[0])

    def y(self):
        return float(self.elements[1])

class Edge(Vector2):
    def __init__(self, x, y):
        super().__init__(x,y)

    def __hash__(self):
        self.elements.sort()
        return hash(tuple(self.elements))

    def add_new_vertex(self, vertex):
        return Edge(self.x, vertex), Edge(vertex, self.y)


class Vector3(Vector):
    def __init__(self, x=None, y=None, z=None):
        if x is None and y is None and z is None:
            x, y, z = 0, 0, 0
        super().__init__(x, y, z)

    def __str__(self):
        return f"{self.elements[0:3]}"

    def cross_product(self, other):
        result = Vector3(self.elements[1] * other.elements[2] - self.elements[2] * other.elements[1],
                        self.elements[2] * other.elements[0] - self.elements[0] * other.elements[2],
                        self.elements[0] * other.elements[1] - self.elements[1] * other.elements[0]
                        )
        return result

    def x(self):
        return float(self.elements[0])

    def y(self):
        return float(self.elements[1])

    def z(self):
        return float(self.elements[2])


    def normalize(self):
        xxyyzz = self.x() * self.x() + self.y() * self.y() + self.z() * self.z()

        invLength = 1.0 / math.sqrt(xxyyzz)
        self.elements[0] *= invLength
        self.elements[1] *= invLength
        self.elements[2] *= invLength

        return self


class Vector4(Vector):
    @classmethod
    def create_from_array(cls, arr):
        if len(arr) != 4:
            raise Exception("Array Length Should be 4")
        return cls(arr[0], arr[1], arr[2], arr[3])

    def __init__(self, x, y, z, w):
        super().__init__(x, y, z, w)

    def __repr__(self):
        return f"Vector4({self.elements})"

    @staticmethod
    def zeros():
        return Vector4(0, 0, 0, 0)

    def x(self):
        return float(self.elements[0])

    def y(self):
        return float(self.elements[1])

    def z(self):
        return float(self.elements[2])

    def w(self):
        return float(self.elements[2])




if __name__ == "__main__":
    a = Vector4(1, 2, 3, 0)
    print(a)
    b = Vector4(3, 4, 5, 0)
    q = a * 3
    print(type(q.elements))
    c = Vector3(*[1, 2, 3])
    print(c)
