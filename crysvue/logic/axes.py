#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"

from typing import List

import numpy as np


class AxesLogic:

    def __init__(self, labels: List[str], positions: np.array = None, matrix: np.array = None):
        self._labels = labels
        if positions is None:
            positions = np.eye(3)
        if matrix is None:
            matrix = np.eye(3)

        star_abc = np.matmul(positions, matrix)
        rotation_angles = []
        for i in range(3):
            a, b, c = star_abc[i, :]
            theta, phi = self._xyz_to_sphere(a, b, c)
            rotation_angles.append([theta, phi])
        self._rotation_angles = np.array(rotation_angles)


    @staticmethod
    def _xyz_to_sphere(X, Y, Z):
        if Z > 0:
            theta = np.arctan2(np.sqrt(X ** 2 + Y ** 2), Z)
        elif Z < 0:
            theta = np.pi + np.arctan2(np.sqrt(X ** 2 + Y ** 2), Z)
        elif Z == 0 and X != 0 and Y != 0:
            theta = np.pi / 2
        else:
            theta = np.pi / 2
        if X > 0:
            phi = np.arctan2(Y, X)
        elif X < 0 <= Y:
            phi = np.pi + np.arctan2(Y, X)
        elif X < 0 and Y < 0:
            phi = -np.pi + np.arctan2(Y, X)
        elif X == 0 and Y > 0:
            phi = np.pi / 2
        elif X == 0 and Y < 0:
            phi = -np.pi / 2
        else:
            phi = 0
        return theta, phi

