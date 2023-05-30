#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>
from __future__ import annotations

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"

from typing import List, Optional, Dict

import numpy as np
from vispy.scene.visuals import Compound, Text
from vispy.visuals.markers import MarkersVisual
from vispy.color import Color

from crysvue.visual.vispy.components import Arrow3D
from crysvue.logic.axes import AxesLogic


_COLORS = {
    'red':   Color('red'),
    'green': Color('green'),
    'blue':  Color('blue'),
    'black': Color('black'),
}


def _default_colors():
    """
    Return the default colors for the 3 axes
    """
    return [_COLORS['red'],
            _COLORS['green'],
            _COLORS['blue']]


class XYZAxis(Compound, AxesLogic):
    """
    A class to represent the XYZ axis in 3D space
    """

    def __init__(self, *args, radius: float = 0.1, labels: Optional[List[str]] = None, **kwargs):

        if labels is None:
            labels = ['X', 'Y', 'Z']
        _kwargs = {}
        if 'matrix' in kwargs:
            _kwargs['matrix'] = kwargs.pop('matrix')
        if 'positions' in kwargs:
            _kwargs['positions'] = kwargs.pop('positions')

        AxesLogic.__init__(self, labels=labels, **_kwargs)

        self._colors = _default_colors()
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
            arr = Arrow3D([0, 0, 0], self._rotation_angles[arrow_index], color=arrow_color, rotate_xy=True)
            self._arrows.append(arr)
            text = Text(self._labels[arrow_index], color=_COLORS['black'])
            text.font_size = 40
            text.pos = arr.calculate_end_point(4 * radius)
            self._texts.append(text)
            visual_objs.append(arr)
            visual_objs.append(text)
        super().__init__(visual_objs, *args, **kwargs)

    @property
    def arrows(self) -> Dict[str, Arrow3D]:
        """
        Return the arrows as a dictionary with the axis labels as keys
        """
        return {label: arrow_obj for label, arrow_obj in zip(self._labels, self._arrows)}

    @property
    def labels(self) -> Dict[str, Text]:
        """
        Return the label text object as a dictionary with the axis labels as keys
        """
        return {label: text_obj for label, text_obj in zip(self._labels, self._texts)}


class ABCAxis(XYZAxis):
    """
    A class to represent the ABC crystallographic axis in 3D space
    """

    def __init__(self, lattice_matrix: np.ndarray, *args, **kwargs):
        """
        Initialise the ABC axis with a lattice matrix
        """
        super().__init__(*args, matrix=lattice_matrix, labels=['a', 'b', 'c'], **kwargs)
