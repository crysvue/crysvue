#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"

import numpy as np

from crysvue import Canvas
from crysvue.visual.generic import UnitCell, Atoms

# Generate a Unit Cell
# Unit-cell is 5x5x5 Angstroms, with an alpha angle of 90 degrees
lattice_matrix = 5 * np.eye(3)

unit_cell_visual = UnitCell(lattice_matrix=lattice_matrix)

# Generate a set of atoms
lattice_symmetry = 'P 1'

atom_positions = np.array([[0.0, 0.0, 0.0],
                           [0.5, 0.5, 0.5]])
atom_sizes = np.array([0.3, 0.3])
atom_colors = np.array([[1.0, 0.0, 0.0],
                        [0.0, 0.0, 1.0]])  # Red and Blue

atoms_visual = Atoms(positions=atom_positions,
                     sizes=atom_sizes,
                     colors=atom_colors,
                     symmetry_str=lattice_symmetry,
                     lattice_matrix=lattice_matrix)

# Create a canvas
canvas = Canvas(display='app')

# Add the visual to the canvas
canvas.add_visual(unit_cell_visual)
canvas.add_visual(atoms_visual)

# Show the canvas
canvas.run()
