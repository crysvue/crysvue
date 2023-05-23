#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"


import numpy as np

class UnitCellLogic:

    def __init__(self, extent=(1, 1, 1), center=None, frac_to_abc=None):
        if frac_to_abc is None:
            frac_to_abc = np.eye(3)
        if center is None:
            center = np.array(extent)/2
        points = self.generate_unit_cell(extent=extent, center=center)
        self._unit_cell_points = np.matmul(points, frac_to_abc)

    def generate_unit_cell(self, extent=(1, 1, 1), center=(0.5, 0.5, 0.5)):
        points = []

        # Add major lattice points
        for z in np.arange(extent[2]):
            for y in np.arange(extent[1]):
                for x in np.arange(extent[0]):
                    points.append([x, y, z])
                    points.append([x + 1, y, z])
                    points.append([None, None, None])

                    points.append([x, y, z])
                    points.append([x, y + 1, z])
                    points.append([None, None, None])

                    points.append([x, y, z])
                    points.append([x, y, z + 1])
                    points.append([None, None, None])

                    points.append([x + 1, y + 1, z + 1])
                    points.append([x + 1, y, z + 1])
                    points.append([None, None, None])

                    points.append([x + 1, y + 1, z + 1])
                    points.append([x + 1, y + 1, z])
                    points.append([None, None, None])

                    points.append([x + 1, y + 1, z + 1])
                    points.append([x, y + 1, z + 1])
                    points.append([None, None, None])

        # Draw x lines
        for x in np.arange(extent[0]):
            y = extent[1]
            z = 0
            points.append([x, y, z])
            points.append([x + 1, y, z])
            points.append([None, None, None])
            z = extent[2]
            y = 0
            points.append([x, y, z])
            points.append([x + 1, y, z])
            points.append([None, None, None])

        # Draw y lines
        for y in np.arange(extent[1]):
            x = 0
            z = extent[2]
            points.append([x, y, z])
            points.append([x, y + 1, z])
            points.append([None, None, None])
            x = extent[0]
            z = 0
            points.append([x, y, z])
            points.append([x, y + 1, z])
            points.append([None, None, None])

        # Draw z lines
        for z in np.arange(extent[2]):
            x = 0
            y = extent[1]
            points.append([x, y, z])
            points.append([x, y, z + 1])
            points.append([None, None, None])
            x = extent[0]
            y = 0
            points.append([x, y, z])
            points.append([x, y, z + 1])
            points.append([None, None, None])

        return np.array(points, dtype=np.float32) - np.array(center, dtype=np.float32)