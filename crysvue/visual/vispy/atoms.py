#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

from __future__ import annotations

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"

import brille
import numpy as np

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import numpy.typing as npt

from vispy.color import Color
from vispy.visuals.markers import MarkersVisual
from crysvue.logic.atoms import AtomsLogic


class AtomsVisual(MarkersVisual, AtomsLogic):
    def __init__(self, position, size, color, symmetry_str, extent: npt.ArrayLike = (1, 1, 1),
                 center: Optional[npt.ArrayLike] = None, frac_to_abc: np.ndarray = None, **kwargs):
        AtomsLogic.__init__(self, position, size, color, symmetry_str)

        if frac_to_abc is None:
            frac_to_abc = np.eye(3)
        frac_to_abc = np.asarray(frac_to_abc)

        if center is None:
            center = np.asarray(extent) / 2
        center = np.asarray(center)
        extent = np.asarray(extent)

        dataset = self.generate_full_dataset(extent)
        positions = np.matmul(dataset['positions'] - center, frac_to_abc)
        sizes = dataset['sizes']
        colors = [Color(c) for c in dataset['colors']]

        MarkersVisual.__init__(self, pos=positions,
                               size=sizes,
                               face_color=colors,
                               antialias=0,
                               spherical=True,
                               edge_color='white',
                               edge_width=0,
                               scaling=True,
                               **kwargs)
