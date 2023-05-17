#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>
from dataclasses import dataclass, field

import numpy as np
from vispy.scene.visuals import Compound, Text
from vispy.visuals.markers import MarkersVisual
from vispy.color import Color

from crysvue.visual.vispy.components import Arrow3D

_COLORS = {
    'red':   Color('red'),
    'green': Color('green'),
    'blue':  Color('blue'),
    'black': Color('black'),
}


def _default_colors():
    return [_COLORS['red'],
            _COLORS['green'],
            _COLORS['blue']]


def _default_rotations():
    return np.array([[np.pi / 2, 0],
                     [np.pi / 2, np.pi / 2],
                     [0, 0]])


class XYZAxis(Compound):
    _labels = ['X', 'Y', 'Z']

    def __init__(self, *args, rotations=None, radius=0.1, **kwargs):
        self._colors = _default_colors()
        if rotations is None:
            rotations = _default_rotations()
        self.rotations = rotations
        visual_objs = [MarkersVisual(pos=np.array([[0, 0, 0], ]),
                                     size=[2 * radius],
                                     face_color=[Color('black')],
                                     antialias=0,
                                     spherical=True,
                                     edge_width=0,
                                     scaling=True)]
        self._arrows = []
        self._texts = []
        for arrow_index, arrow_color in enumerate(self._colors):
            arr = Arrow3D([0, 0, 0], self.rotations[arrow_index], color=arrow_color, rotate_xy=True)
            self._arrows.append(arr)
            text = Text(self._labels[arrow_index], color=_COLORS['black'])
            text.font_size = 40
            text.pos = arr.calculate_end_point(4 * radius)
            self._texts.append(text)
            visual_objs.append(arr)
            visual_objs.append(text)
        super().__init__(visual_objs, *args, **kwargs)

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

    @property
    def arrows(self):
        return {label: arrow_obj for label, arrow_obj in zip(self._labels, self._arrows)}

    @property
    def labels(self):
        return {label: text_obj for label, text_obj in zip(self._labels, self._texts)}


class ABCAxis(XYZAxis):
    _labels = ['a', 'b', 'c']

    def __init__(self, lattice_matrix, *args, **kwargs):
        positions = np.eye(3)
        star_abc = np.matmul(positions, lattice_matrix)
        rotation_angles = []
        for i in range(3):
            a, b, c = star_abc[i, :]
            theta, phi = self._xyz_to_sphere(a, b, c)
            rotation_angles.append([theta, phi])
        super().__init__(*args, rotations=np.array(rotation_angles), **kwargs)
