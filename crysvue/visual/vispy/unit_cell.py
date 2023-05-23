#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

import os

import numpy as np
from vispy import gloo, visuals


with open(os.path.join(os.path.dirname(__file__), 'gloo', 'unit_cell.glv')) as f:
    _UNIT_CELL_VERT = f.read()

with open(os.path.join(os.path.dirname(__file__), 'gloo', 'unit_cell.glf')) as f:
    _UNIT_CELL_FRAG = f.read()

from crysvue.logic.unit_cell import UnitCellLogic


class UnitCellVisual(visuals.Visual, UnitCellLogic):
    """Example of a very simple GL-line visual.
    This shows the minimal set of methods that need to be reimplemented to
    make a new visual class.
    """

    def __init__(self, extent=(1, 1, 1), center=None, color=(0.5, 0.5, 0.5, 1), frac_to_abc: np.ndarray = None):
        UnitCellLogic.__init__(self, extent=extent, center=center, frac_to_abc=frac_to_abc)
        visuals.Visual.__init__(self, vcode=_UNIT_CELL_VERT, fcode=_UNIT_CELL_FRAG)

        self.pos_buf = gloo.VertexBuffer()

        # The Visual superclass contains a MultiProgram, which is an object
        # that behaves like a normal shader program (you can assign shader
        # code, upload values, set template variables, etc.) but internally
        # manages multiple ModularProgram instances, one per view.

        # The MultiProgram is accessed via the `shared_program` property, so
        # the following modifications to the program will be applied to all
        # views:
        self.shared_program['a_pos'] = self.pos_buf
        self.shared_program.frag['color'] = color

        self._need_upload = False

        # Visual keeps track of draw mode, index buffer, and GL state. These
        # are shared between all views.
        self._draw_mode = 'line_strip'
        self.set_gl_state('translucent', depth_test=False)

        self.set_data(self._unit_cell_points)

    def set_data(self, pos):
        self._pos = pos
        self._need_upload = True

    def _prepare_transforms(self, view=None):
        view.view_program.vert['transform'] = view.transforms.get_transform()

    def _prepare_draw(self, view=None):
        """This method is called immediately before each draw.
        The *view* argument indicates which view is about to be drawn.
        """
        if self._need_upload:
            # Note that pos_buf is shared between all views, so we have no need
            # to use the *view* argument in this example. This will be true
            # for most visuals.
            self.pos_buf.set_data(self._pos.astype(np.float32))
            self._need_upload = False
