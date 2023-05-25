#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

from __future__ import annotations

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"

from typing import Literal, Optional, Dict, TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    from crysvue.visual import V, VC
    from crysvue.canvases import VisualCanvas

_CANVAS_DEFAULTS = {
    'app': {
        'keys': 'interactive',
        'show': True
    },
    'jupyter': {
        'keys': 'interactive',
        'bgcolor': 'white',
        'size': (500, 400),
        'show': True,
        'resizable': True
    },
    'qml': {
    }
}


class Canvas:
    """
    This class is a wrapper around the various canvases that can be used to display the crystal.
    """
    def __init__(self, display: Optional[Literal['app', 'jupyter', 'qml']] = None, **kwargs):
        """
        Initialise the canvas and set the display mode. The display mode can be one of:
        - app: A standalone application
        - jupyter: A jupyter notebook
        - qml: A qml application

        :param display: The display mode
        :param kwargs: Additional arguments to pass to the canvas
        """

        self._canvas: Optional[VisualCanvas] = None

        if display is None:
            display = 'app'
        display = display.lower()
        if display not in _CANVAS_DEFAULTS.keys():
            raise ValueError(f"Display mode {display} not recognised")

        # We use vispy for the application and jupyter modes
        if display in ['app', 'jupyter']:
            from vispy import app
            from crysvue.canvases.vispy import CrystalCanvas
            self.app = app
            opts = _CANVAS_DEFAULTS[display].copy()
            opts.update(kwargs)
            self._canvas = CrystalCanvas(**opts)
        elif display == 'qml':
            raise NotImplementedError(f"Display mode {display} not implemented")
        self.mode = display

    @property
    def base_components(self) -> Dict[str, VC]:
        """
        Returns the base components of the canvas
        Returns:

        """
        if self._canvas is not None:
            return self._canvas.components
        else:
            raise NotImplementedError(f"Display mode {self.mode} not implemented")

    def add_element(self, element: V) -> NoReturn:
        """
        Adds a visual element to the canvas
        """
        if self._canvas is not None:
            visual_element = element._LABEL
            if visual_element not in self._canvas.components:
                raise ValueError(f"Element {visual_element} not in canvas")
            visual_cls = self._canvas.components[visual_element]
            self._canvas.add_element(visual_element.lower(), element._generate_visual(visual_cls))
        else:
            raise NotImplementedError(f"Display mode {self.mode} not implemented")

    def run(self) -> Optional[VisualCanvas]:
        """
        Run the canvas. This will either start the application or return the canvas object
        Returns:
            The canvas object if in jupyter mode
        """

        if self.mode == 'app':
            self.app.run()
        elif self.mode == 'jupyter':
            return self._canvas
        else:
            raise NotImplementedError(f"Display mode {self.mode} not implemented")
