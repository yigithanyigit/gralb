import math

import numpy
from OpenGL.GLU import *
from vector import Vector3
from matrix4 import Matrix4
import typing


class Camera:
    def __init__(self):
        self.matrix = Matrix4().identity()

        self.stack = []
        self.calculated_stack = False

        self.eye_default = Vector3(0, 0, -5)
        self.target_default = Vector3(0, 0, 0)
        self.up_default = Vector3(0,1,0)
        self.direction = Vector3(0,0,1)

        self.pitch = 0
        self.yaw = 0
        self.roll = 0
        self.constant = 0.174


    def _add_matrix_to_stack(self, op):
        self.stack.append(op)
        self.calculated_stack = False

    def _pop_matrix_from_stack(self):
        if len(self.stack) != 0:
            self.stack.pop()

    def _stack_head(self):
        if len(self.stack) > 0:
            return self.stack[-1]
        return None

    """
    def calculate(self):
        m = self.matrix
        while self._stack_head() is not None:
            m = m.dot_product(self._stack_head())
            self._pop_matrix_from_stack()
        self.matrix.rows = m.rows
        self.calculated_stack = True
        return self
    """
    def lookAt(self, eye, target, upDir = Vector3(0,1,0)):

        self.eye_default = eye
        self.target_default = target
        self.up_default = upDir

        forward = eye - target

        forward = forward.normalize()

        left = upDir.cross_product(forward)
        left = left.normalize()

        up = forward.cross_product(left)

        self.matrix.rows[0][0] = left.x()
        self.matrix.rows[1][0] = left.y()
        self.matrix.rows[2][0] = left.z()
        self.matrix.rows[0][1] = up.x()
        self.matrix.rows[1][1] = up.y()
        self.matrix.rows[2][1] = up.z()
        self.matrix.rows[0][2] = forward.x()
        self.matrix.rows[1][2] = forward.y()
        self.matrix.rows[2][2] = forward.z()

        self.matrix.rows[3][0] = -left.x() * eye.x() - left.y() * eye.y() - left.z() * eye.z();
        self.matrix.rows[3][1] = -up.x() * eye.x() - up.y() * eye.y() - up.z() * eye.z();
        self.matrix.rows[3][2] = -forward.x() * eye.x() - forward.y() * eye.y() - forward.z() * eye.z();

        return self.matrix

    def get_view_matrix(self):
        return self.matrix

    def set_view_matrix(self, matrix: typing.List):
        self.matrix = matrix.copy()

    def get_x(self):
        return self.matrix.rows[3][0]

    def get_y(self):
        return self.matrix.rows[3][1]

    def get_z(self):
        return self.matrix.rows[3][2]

    def set_x(self, x):
        self.matrix.rows[3][0] = x

    def set_y(self, y):
        self.matrix.rows[3][1] = y

    def set_z(self, z):
        self.matrix.rows[3][2] = z

    def set_position(self, x, y, z):
        self.set_x(x)
        self.set_y(x)
        self.set_z(z)

    def rotate_y_ccw(self):
        self.pitch -= self.constant
        self.calculate()

    def rotate_y_cw(self):
        self.pitch += self.constant
        self.calculate()

    def rotate_x_ccw(self):
        self.yaw += self.constant
        self.calculate()

    def rotate_x_cw(self):
        self.yaw -= self.constant
        self.calculate()

    def move_forward(self):
        self.eye_default += self.direction

    def move_backward(self):
        self.eye_default -= self.direction

    def move_left(self):
        self.eye_default -= self.direction.cross_product(self.up_default)

    def move_right(self):
        self.eye_default += self.direction.cross_product(self.up_default)


    def calculate(self):

        # Ortbital Camera
        """
        x = math.sin(self.yaw) * math.cos(self.pitch) * self.get_z()
        y = math.sin(self.pitch) * self.get_z()
        z = math.cos(self.yaw) * math.cos(self.pitch) * self.get_z()
        self.lookAt(Vector3(x, y, z), Vector3(0, 0, 0), Vector3(0, 1, 0))
        """

        x = math.sin(self.yaw) * math.cos(self.pitch)
        y = math.sin(self.pitch)
        z = math.cos(self.yaw) * math.cos(self.pitch)
        self.direction = Vector3(x, y, z).normalize()
        self.lookAt(self.eye_default, self.direction + self.eye_default, Vector3(0, 1, 0))