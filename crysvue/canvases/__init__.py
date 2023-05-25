#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

from __future__ import annotations

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"

from typing import Protocol, Dict

class VisualCanvas(Protocol):
    def add_element(self, key: str, element):
        pass

    def remove_element(self, key: str, element):
        pass

    @property
    def components(self) -> Dict[str, type]:
        pass

    def create_component(self, component_key: str, *args, **kwargs):
        pass