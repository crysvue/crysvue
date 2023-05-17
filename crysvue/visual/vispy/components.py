from __future__ import annotations
#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"

from typing import Optional, TYPE_CHECKING, Union

import numpy as np
if TYPE_CHECKING:
    import numpy.typing as npt
from vispy.geometry import create_cone
from vispy.scene.visuals import Compound, Tube, Mesh
from vispy.color import Color


def Rx(theta):
    """
    Rotation matrix about the x-axis.
    Args:
        theta: Rotation angle in radians.
    Returns: Rotation matrix.
    """
    return np.array([[1, 0, 0],
                      [0, np.cos(theta), -np.sin(theta)],
                      [0, np.sin(theta), np.cos(theta)]])


def Ry(theta):
    """
    Rotation matrix about the y-axis.
    Args:
        theta: Rotation angle in radians.
    Returns: Rotation matrix.
    """
    return np.array([[np.cos(theta), 0, np.sin(theta)],
                      [0, 1, 0],
                      [-np.sin(theta), 0, np.cos(theta)]])


def Rz(theta):
    """
    Rotation matrix about the z-axis.
    Args:
        theta: Rotation angle in radians.
    Returns: Rotation matrix.
    """
    return np.array([[np.cos(theta), -np.sin(theta), 0],
                      [np.sin(theta), np.cos(theta), 0],
                      [0, 0, 1]])


class Arrow3D(Compound):

    """
    A 3D arrow visual, with a cone at the end. The arrow points in the direction of the z-axis, with the given position
    being the base of the tube. It can be rotated using spherical angles (theta, phi) to point in any direction. Theta
    and phi are defined to ISO 80000-2:2019 (https://www.iso.org/standard/80000-2.html). Note that for vispy the
    rotate_xy flag is needed as it's geometry is defined in the x-y plane.
    """
    def __init__(self, position: Optional[npt.ArrayLike] = None, direction: Optional[npt.ArrayLike] = None,
                 length: float = 0.75, radius: float = 0.1, cone_length: float = 0.25, cone_radius: float = 0.2,
                 color: Union[str, Color] = 'black', centered: bool = False, rotate_xy: bool = False, **kwargs):

        if direction is None:
            direction = [0, 0]
        if position is None:
            position = [0, 0, 0]

        self._position = np.asarray(position)
        self._direction = np.asarray(direction)
        self._length = length
        self._radius = radius
        self._cone_length = cone_length
        self._cone_radius = cone_radius
        if isinstance(color, str):
            color = Color(color)
        self._color = color

        if self._direction.shape == (3, 3):
            self._rotation = self._direction
        else:
            theta, phi = self._direction
            self._rotation = np.matmul(Rx(theta), Rz(-phi))
        if rotate_xy:
            self._rotation = np.matmul(self._rotation, Rz(np.pi/2))

        offset = 0
        if centered:
            offset = -self._length/2

        points = np.matmul(np.array([[0, 0, offset], [0, 0, offset + self._length]]), self._rotation) + self._position
        _cone = create_cone(50, self._cone_radius, self._cone_length)

        self._tube = Tube(points, radius=self._radius, color=self._color)
        self._cone_mesh = Mesh(np.matmul(_cone._vertices, self._rotation) + points[1, :], _cone._faces, shading='smooth', color=self._color)

        super().__init__([self._cone_mesh, self._tube], **kwargs)

    @property
    def total_length(self):
        return self._length + self._cone_length

    def calculate_end_point(self, extra_length: float = 0):
        return np.matmul(np.array([0, 0, self.total_length + extra_length]), self._rotation) + self._position