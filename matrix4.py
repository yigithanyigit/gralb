# CENG 487 Assignment 1 by Yigithan Yigit
# Erdem Taylan # StudentId: 310201112
# 10/23

from vector import *
import math


class Matrix4:
    @classmethod
    def create_from_array(cls, arr, transpose=False):
        if len(arr) != 16:
            raise Exception("Arr should be 16")
        if transpose:
            return cls(Vector4.create_from_array(arr[0:4]),
                       Vector4.create_from_array(arr[4:8]),
                       Vector4.create_from_array(arr[8:12]),
                       Vector4.create_from_array(arr[12:16]))
        else:
            return cls(Vector4.create_from_array([arr[0], arr[4], arr[8], arr[12]]),
                       Vector4.create_from_array([arr[1], arr[5], arr[9], arr[13]]),
                       Vector4.create_from_array([arr[2], arr[6], arr[10], arr[14]]),
                       Vector4.create_from_array([arr[3], arr[7], arr[11], arr[15]]))

    """
    @classmethod
    def create_from_array_row_major(cls, arr):
        if len(arr) != 16:
            raise Exception("Arr should be 16")
        return cls(Vector4.create_from_array(arr[0:4]),
                   Vector4.create_from_array(arr[4:8]),
                   Vector4.create_from_array(arr[8:12]),
                   Vector4.create_from_array(arr[12:16]))
    """

    def __init__(self, *rows):
        if len(rows) == 0:
            self.rows = Matrix4.identity().rows
            return
        elif len(rows) != 4:
            raise Exception
        for r in rows:
            if not isinstance(r, Vector4):
                raise TypeError

        self.rows = [row for row in rows]

        self.stack = []





    def __add__(self, other):
        return Matrix4(*((x + y) for x, y in zip(self.rows, other.rows)))

    def __sub__(self, other):
        return Matrix4(*((x - y) for x, y in zip(self.rows, other.rows)))

    def __mul__(self, scalar):
        for idx, r in enumerate(self.rows):
            self.rows[idx] = self.rows[idx] * scalar
        return Matrix4(*self.rows)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __str__(self):
        return f"{self.rows[0]}\n{self.rows[1]}\n{self.rows[2]}\n{self.rows[3]}"

    def __repr__(self):
        return f"{self.rows[0]}\n{self.rows[1]}\n{self.rows[2]}\n{self.rows[3]}"

    def asList(self):
        temp = []
        for x in self.rows:
            for e in x:
                temp.append(e)
        return temp

    def dot_product(self, other):
        arr = []
        other = other.transpose()
        for srow in self.rows:
            for orow in other.rows:
                arr.append(srow.dot_product(orow))
        return Matrix4.create_from_array(arr, transpose=True)

    def transpose(self):
        temp_matrix = []
        for j in range(len(self.rows[0])):
            temp_vector = []
            for i in range(len(self.rows)):
                temp_vector.append(self.rows[i][j])
            temp_matrix.append(Vector4(*temp_vector))
        return Matrix4(*temp_matrix)

    @staticmethod
    def zeros():
        temp_matrix = []
        for i in range(4):
            temp_matrix.append(Vector4.zeros())
        return Matrix4(*temp_matrix)

    @staticmethod
    def identity():
        matrix = Matrix4.zeros()
        for i in range(4):
            matrix.rows[i][i] = 1
        return matrix

    def rotate_x(self, x):
        temp = Matrix4.Rx(x).dot_product(self)
        self.rows = temp.rows
        return self

    def rotate_y(self, x):
        temp = Matrix4.Ry(x).dot_product(self)
        self.rows = temp.rows
        return self

    def rotate_z(self, x):
        temp = Matrix4.Rz(x).dot_product(self)
        self.rows = temp.rows
        return self

    def translate(self, x, y, z):
        temp = Matrix4.T(x, y, z).dot_product(self)
        self.rows = temp.rows
        return self

    def copy(self):
        return Matrix4.create_from_array(self.asList(), transpose=False)

    def scale(self, scalar):
        temp = Matrix4.S(scalar).dot_product(self)
        self.rows = temp.rows
        return self


    @staticmethod
    def Rx(x):
        return Matrix4.create_from_array(
            [1.0, 0.0, 0.0, 0.0, 0.0, math.cos(x), -math.sin(x), 0.0, 0.0, math.sin(x), math.cos(x), 0.0, 0.0, 0.0, 0.0,
             1.0])

    @staticmethod
    def Ry(x):
        return Matrix4.create_from_array(
            [math.cos(x), 0.0, math.sin(x), 0.0, 0.0, 1.0, 0.0, 0.0, -math.sin(x), 0.0, math.cos(x), 0.0, 0.0, 0.0, 0.0,
             1.0])

    @staticmethod
    def Rz(x):
        return Matrix4.create_from_array(
            [math.cos(x), -math.sin(x), 0.0, 0.0, math.sin(x), math.cos(x), 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0,
             1.0])

    @staticmethod
    def S(scalar):
        return Matrix4.create_from_array(
            [scalar, 0.0, 0.0, 0.0, 0.0, scalar, 0.0, 0.0, 0.0, 0.0, scalar, 0.0, 0.0, 0.0, 0.0, 1.0])

    @staticmethod
    def T(x, y, z):
        return Matrix4.create_from_array([1.0, 0.0, 0.0, x, 0.0, 1.0, 0.0, y, 0.0, 0.0, 1.0, z, 0.0, 0.0, 0.0, 1.0])


if __name__ == "__main__":
    m1 = Matrix4.create_from_array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
    m2 = Matrix4.create_from_array([1, 0, 0, -1, 0, 1, 0, 0, 0, 0, 1, -12, 0, 0, 0, 1])
    m3 = Matrix4.create_from_array(
        [math.cos(30), -math.sin(30), 0.0, 0.0, math.sin(30), math.cos(30), 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0,
         1.0])
    m2 = m2.dot_product(m1)
    m2 = m2.dot_product(m3)
    print(m1.translate(1, 0, -12))
