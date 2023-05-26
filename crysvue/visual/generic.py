#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

from __future__ import annotations

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"


import numpy as np


from crysvue.visual import VisualBase
from crysvue.logic.atoms import AtomsLogic
from crysvue.logic.unit_cell import UnitCellLogic


class UnitCell(VisualBase, UnitCellLogic):
    _LABEL = 'UnitCell'

    def __init__(self, lattice_matrix: np.ndarray, extent=(1, 1, 1), center=None, color=(0.5, 0.5, 0.5, 1)):
        VisualBase.__init__(self, extent, center, color, frac_to_abc=lattice_matrix)


class Atoms(VisualBase):
    _LABEL = 'Atoms'

    def __init__(self, positions, sizes, colors, symmetry_str, lattice_matrix, extent=(1, 1, 1), center=None, **kwargs):
        VisualBase.__init__(self, positions, sizes, colors, symmetry_str,
                         extent=extent, center=center, frac_to_abc=lattice_matrix, **kwargs)