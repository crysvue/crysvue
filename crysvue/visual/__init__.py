#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

from vispy.scene.visuals import create_visual_node
from .unit_cell import UnitCellVisual
from .atoms import AtomsVisual
#
Atoms = create_visual_node(AtomsVisual)
UnitCell = create_visual_node(UnitCellVisual)
