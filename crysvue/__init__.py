#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

from typing import Literal


_CANVAS_DEFAULTS = {
    'app': {'keys': 'interactive', 'show': True},
    'jupyter': {'keys':'interactive', 'bgcolor':'white', 'size': (500, 400), 'show': True, 'resizable': True},
    'qml': {}
}



class Canvas:
    def __init__(self, display: Literal['app'] = None, **kwargs):

        self._canvas = None
        if display is None:
            display = 'app'

        display = display.lower()

        if display in ['app', 'jupyter']:
            from vispy import app
            from crysvue.canvases.vispy import CrystalCanvas
            self.app = app
            opts = _CANVAS_DEFAULTS[display].copy()
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

    def add_element(self, element):
        if self._canvas is not None:
            visual_element = element._LABEL
            if visual_element not in self._canvas.components:
                raise ValueError(f"Element {visual_element} not in canvas")
            visual_cls = self._canvas.components[visual_element]
            self._canvas.add_element(visual_element.lower(), element._generate_visual(visual_cls))
        else:
            raise NotImplementedError(f"Display mode {self.mode} not implemented")

    def run(self):
        if self.mode == 'app':
            self.app.run()
        elif self.mode == 'jupyter':
            return self._canvas
        else:
            raise NotImplementedError(f"Display mode {self.mode} not implemented")
