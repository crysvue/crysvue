#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

from __future__ import annotations

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"


from vispy.scene.visuals import create_visual_node as _create_visual_node
from .unit_cell import UnitCellVisual as _UnitCellVisual
from .atoms import AtomsVisual as _AtomsVisual
from .axes import XYZAxis, ABCAxis
#
Atoms = _create_visual_node(_AtomsVisual)
UnitCell = _create_visual_node(_UnitCellVisual)