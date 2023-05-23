#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>
from __future__ import annotations


class VisualBase:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def _generate_visual(self, visual_cls):
        return visual_cls(*self._args, **self._kwargs)
