#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

from typing import Literal


class Canvas:
    def __init__(self, display: Literal['app'] = None, **kwargs):

        self._canvas = None
        if display is None:
            display = 'app'

        display = display.lower()

        if display == 'app':
            from vispy import app
            from crysvue.canvases.vispy import CrystalCanvas
            self.app = app
            opts = {'keys': 'interactive', 'show': True}
            opts.update(kwargs)
            self._canvas = CrystalCanvas(**opts)
        elif display == 'jupyter':
            raise NotImplementedError(f"Display mode {display} not implemented")
        elif display == 'qml':
            raise NotImplementedError(f"Display mode {display} not implemented")
        self.mode = display

    @property
    def base_components(self):
        if self._canvas is not None:
            return self._canvas.components
        else:
            raise NotImplementedError(f"Display mode {self.mode} not implemented")

    def create_component(self, name, component):
        if self._canvas is not None:
            self._canvas.create_component(name, component)
        else:
            raise NotImplementedError(f"Display mode {self.mode} not implemented")

    def add_element(self, name, element):
        if self._canvas is not None:
            self._canvas.add_element(name, element)
        else:
            raise NotImplementedError(f"Display mode {self.mode} not implemented")

    def run(self):
        if self.mode == 'app':
            self.app.run()
        else:
            raise NotImplementedError(f"Display mode {self.mode} not implemented")
