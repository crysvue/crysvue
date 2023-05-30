#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

from __future__ import annotations

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"

from typing import TypeVar, Type, TYPE_CHECKING


class VisualBase:
    """
    Base class for all visuals, acts as a storage wrapper for arguments, so that they can be passed to the visual
    """
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def _generate_visual(self, visual_cls):
        return visual_cls(*self._args, **self._kwargs)


if TYPE_CHECKING:
    VC = Type[VisualBase]
    V = TypeVar('V', bound=VisualBase)
